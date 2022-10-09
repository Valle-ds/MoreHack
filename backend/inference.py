import transformers
import pandas as pd
import torch
from datetime import datetime, timedelta

def get_cos(a, b):
    return a / a.norm(dim=-1, keepdim=True) @ (b / b.norm(dim=-1, keepdim=True)).T

def inference(profession, task, n, tokenizer, model , text_encoding, df, out1_1):
    task = int(task)
    print('start')
    text_encoding2 = tokenizer(
                profession, # !!!
                max_length=32,
                padding="max_length",
                truncation=True,
                return_attention_mask=True,
                add_special_tokens=True,
                return_tensors="pt")

    out2_1 = model(input_ids=text_encoding2['input_ids'].to('cpu'),
                        attention_mask=text_encoding2['attention_mask'].to('cpu'))['last_hidden_state'][:, 0, :]

    if task == 0 or task == 2:
        coses = get_cos(out1_1, out2_1).flatten()
        t = min(sorted(list(coses.detach().numpy()))[-5], 0.55)

        coses2 = coses > t#0.45
        # coses = coses[:4]
        profs = []
        for i in range(len(coses)):
            if coses2[i]:
                if task == 0:
                    profs.append(df.iloc[i]['text'].replace("\\", ""))
                elif task == 2:
                    profs.append(df.iloc[i]['title'].replace("\\", ""))

        return profs
    elif task == 1:
        trends = []
        indexes = []
        for i in range(len(out1_1) - 1):
            if i in indexes:
                continue
            coses = get_cos(out1_1[i:], out2_1).flatten()
            t = min(sorted(list(coses.detach().numpy()))[max(-5, -len(coses))], 0.45)
            if coses[0] < t:
                continue
            coses_t = get_cos(out1_1[i + 1:], out1_1[i]).flatten() > 0.9
            trends_add = [df['text'].iloc[i].replace("\\", "")]
            for j in range(len(coses_t)):
                c_i = i + 1 + j
                if coses_t[j] and c_i not in indexes:
                    indexes.append(c_i)
                    trends_add.append(df['text'].iloc[c_i].replace("\\", ""))
            if len(trends_add) > 1:
                trends.append(trends_add)
        return trends