from src.steam_deals import SteamDeals
from src.epic_deals import EpicDeals

class Deals:
    def __init__(self):
        self.steam_deals = SteamDeals()
        self.epic_deals = EpicDeals()