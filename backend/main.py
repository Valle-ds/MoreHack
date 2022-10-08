import uuid

import pandas as pd
import transformers

import uvicorn
from fastapi import File
from fastapi import FastAPI
from fastapi import UploadFile
import numpy as np
from PIL import Image

# import config
# import inference
import inference


app = FastAPI()

def prepare():
    df = pd.read_csv('lenta-ru-news.csv')

    tokenizer = transformers.AutoTokenizer.from_pretrained('cointegrated/rubert-tiny2')
    model = transformers.AutoModel.from_pretrained('cointegrated/rubert-tiny2')

    
    text_encoding = tokenizer(
                list(df['text'].values[:1024]),
                max_length=128,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                add_special_tokens=True,
                return_tensors="pt")
    
    return tokenizer, model , text_encoding, df

tokenizer, model , text_encoding, df = prepare()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.get("/predict")
def get_image(profession: str):
    posts = inference.inference(profession, tokenizer, model , text_encoding, df)

    return {"posts": posts}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080) # , host="0.0.0.0"