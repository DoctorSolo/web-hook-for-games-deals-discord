from src.Deals import Deals
import asyncio

if __name__ == "__main__":
    deals = Deals()
    asyncio.run(deals.run_all())