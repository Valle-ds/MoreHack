import transformers
import pandas as pd
import torch

def get_cos(a, b):
    return a / a.norm(dim=-1, keepdim=True) @ (b / b.norm(dim=-1, keepdim=True)).T

def inference(profession, tokenizer, model , text_encoding, df):
    text_encoding2 = tokenizer(
                profession, # !!!
                max_length=32,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                add_special_tokens=True,
                return_tensors="pt")

    out1_1 = []
    for i in range(len(text_encoding['input_ids']) // 128 + len(text_encoding['input_ids']) % 128):
        with torch.no_grad():
            out1 = model(input_ids=text_encoding['input_ids'][i * 128: (i + 1) * 128].to('cpu'),
                        attention_mask=text_encoding['attention_mask'][i * 128: (i + 1) * 128].to('cpu'))['last_hidden_state'][:, 0, :]
            out1_1 += list(out1)

    out2_1 = model(input_ids=text_encoding2['input_ids'].to('cpu'),
                        attention_mask=text_encoding2['attention_mask'].to('cpu'))['last_hidden_state'][:, 0, :]
    out1_1 = torch.stack(out1_1)

    coses = get_cos(out1_1, out2_1).flatten()
    coses2 = coses > 0.45
    # coses = coses[:4]
    profs = []
    for i in range(len(coses)):
        if coses2[i]:
            profs.append(df.iloc[i]['text'])
    
    return profs