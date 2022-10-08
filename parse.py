from datetime import datetime
from telethon.sync import TelegramClient
import asyncio
import time
from telethon import functions, types
import datetime
from telethon import TelegramClient, events, sync
import pandas as pd

name = 'anon' 
api_id = '11138523'
api_hash = "5367efd9710fc92a6e346ba9d75fd358" 

chats_buh = ['t.me/tass_agency', 't.me/rian_ru','t.me/bbbreaking', 't.me/netipichniy_buh', 't.me/buhflash',
            't.me/tot115fz', 't.me/FizAndYur', 't.me/mytar_rf', 't.me/klerkonline', 't.me/centralbank_russia']

chats_business = ['t.me/tass_agency', 't.me/rian_ru','t.me/bbbreaking', 't.me/denissexy', 't.me/rkn_tg', 't.me/tbite', 't.me/exploitex', 't.me/d_code', 't.me/thebell_io', 't.me/Bell_daily',
                't.me/economika', 't.me/finkrolik', 't.me/rt_russian', 't.me/e_magic', 't.me/cbrstocks', 't.me/fineconomics', 't.me/dohod', 't.me/government_rus', 't.me/mcx_ru',
                't.me/papagaz', 't.me/oil_capital', 't.me/neftegram', 't.me/mintsifry', 't.me/MID_Russia', 't.me/mintrudrf', 't.me/minfin', 't.me/minpromtorg_ru', 't.me/minstroyrf']

async def parse_tg(chat, days=0, years=0):
    data = []
    async with TelegramClient(name, api_id, api_hash) as client:
        async for message in client.iter_messages(chat, reverse = True,  offset_date=datetime.datetime.now() - datetime.timedelta(days=(days + (years * 365)))):
            # print(message.text, message.date)
            data.append([message.text, message.date])
    return data

async def main(api_id, api_hash, chats, csv_path='output.csv'):
    all_data = []
    for chat in chats:
        print(f'Parsing: {chat}')
        d = await parse_tg(chat, years=3)
        all_data.extend(d)
        print(f'Done Parsing: {chat}')

    pd.DataFrame(all_data, columns=['text', 'date']).to_csv(csv_path)


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main(api_id, api_hash, chats_buh, 'buhgalters.csv'))
    t2 = time.time()
    print(t2-t1)
