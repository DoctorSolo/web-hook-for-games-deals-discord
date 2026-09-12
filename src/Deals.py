from src.steam_deals import SteamDeals
from src.epic_deals import EpicDeals
from src.bot.bot import Bot
import asyncio

class Deals:
    def __init__(self):
        self.bot = Bot()
        self.steam_deals = SteamDeals()
        self.epic_deals = EpicDeals()
    
    async def run_all(self):
        # 1. Limpa o canal com o bot
        print("Iniciando limpeza do canal...")
        await self.bot.start()
        
        # 2. Envia promoções Steam
        print("Enviando promoções Steam...")
        self.steam_deals.Run()
        
        # 3. Envia promoções Epic
        print("Enviando promoções Epic...")
        self.epic_deals.Run()
        
        print("Tudo concluído!")
