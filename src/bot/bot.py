import discord
from discord.ext import commands, tasks
from config import BOT_TOKEN, CHANNEL_ID


class Bot:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=self.intents)
        self.ID_DO_CANAL = CHANNEL_ID
        self._setup_events()
    # END
        
    def _setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'Bot conectado como {self.bot.user}')
            limpeza_automatica.start()
        
        @tasks.loop(count=20)  # Roda apenas UMA vez
        async def limpeza_automatica():
            try:
                canal = await self.bot.fetch_channel(self.ID_DO_CANAL)
                
                print(f"Iniciando limpeza automática no canal: {canal.name}")
                apagadas = await canal.purge(limit=None)
                
                await canal.send(
                    f"🧹 **Limpeza Automática:** {len(apagadas)} mensagens foram limpas!", 
                    delete_after=10
                )
                print("Limpeza concluída.")
                
                # Desliga o bot após limpar
                await self.bot.close()
                
            except discord.NotFound:
                print("Erro: Canal não encontrado.")
                await self.bot.close()
            except Exception as e:
                print(f"Erro: {e}")
                await self.bot.close()
    # END
    
    async def start(self):
        await self.bot.start(BOT_TOKEN)
    # END

