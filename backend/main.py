import pandas as pd
import transformers

import uvicorn
from fastapi import FastAPI
import numpy as np
import torch

import inference


app = FastAPI()

def prepare():
    df = pd.read_csv('test.csv')

    tokenizer = transformers.AutoTokenizer.from_pretrained('cointegrated/rubert-tiny2')
    model = transformers.AutoModel.from_pretrained('cointegrated/rubert-tiny2')

    
    text_encoding = tokenizer(
                list(df['text'].values),
                max_length=256,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                add_special_tokens=True,
                return_tensors="pt")
    out1_1 = []
    res = 0 if len(text_encoding['input_ids']) % 128 == 0 else 1
    for i in range(len(text_encoding['input_ids']) // 128 + res):
        with torch.no_grad():
            out1 = model(input_ids=text_encoding['input_ids'][i * 128: (i + 1) * 128].to('cpu'),
                        attention_mask=text_encoding['attention_mask'][i * 128: (i + 1) * 128].to('cpu'))['last_hidden_state'][:, 0, :]
            out1_1 += list(out1)

    out1_1 = torch.stack(out1_1)
    df['date'] = pd.to_datetime(df['date'])
    return tokenizer, model, text_encoding, df, out1_1

tokenizer, model , text_encoding, df, out1_1 = prepare()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

# task: 0 - инсайты, 1 - тренды, 2 - дайджесты
@app.get("/predict")
def get_image(profession, task=0, n=5):
    posts = inference.inference(profession, task, n, tokenizer, model , text_encoding, df, out1_1)

    return {"posts": posts}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080)
