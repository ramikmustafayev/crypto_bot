from database.repo.requests import RequestsRepo
from client_api.bybit_api import BybitClient
import asyncio

async def track_target_prices(message,repo:RequestsRepo,config,user):
    base_url=config.api.url
    bybit_client=BybitClient(base_url)
    while all_tokens:=await repo.watchlist.get_all_by_user_id(user_id=user.id):
        
        for token in all_tokens:
            try:
                token_price=await bybit_client.fetch_token_price(token.ticker)
            except Exception as e:
                print('Connection error')
                await bybit_client.close()

            if token.direction =='+':
                if token_price>=token.target_price:
                    await message.answer(f'{token.ticker} торгуется выше {token.target_price}')
                    await repo.watchlist.delete({'ticker':token.ticker, 'target_price':token.target_price,'direction':token.direction})
            else:
                if token_price<=token.target_price:
                    await message.answer(f'{token.ticker} торгуется ниже {token.target_price}')
                    await repo.watchlist.delete({'ticker':token.ticker, 'target_price':token.target_price,'direction':token.direction})
            

        await asyncio.sleep(2)
    
    await bybit_client.close()