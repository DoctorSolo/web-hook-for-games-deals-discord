import discord
from discord.ext import commands, tasks
from config import CHANNEL_ID, BOT_TOKEN


class Bot:
    def __init__(self):
        # Configuração das intents necessárias
        self.intents = discord.Intents.default()
        self.intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', intents=self.intents)

        # ID do canal de texto que você deseja limpar automaticamente
        self.ID_DO_CANAL = CHANNEL_ID
        
        # Registra os eventos e tarefas
        self._setup_events()
        
    def _setup_events(self):
        """Configura eventos e tarefas"""
        
        @self.bot.event
        async def on_ready():
            print(f'Bot conectado como {self.bot.user}')
            # Inicia a tarefa repetitiva assim que o bot estiver pronto
            self.limpeza_automatica.start()
        
        # Define a tarefa para rodar a cada 6 horas
        @tasks.loop(hours=6.0)
        async def limpeza_automatica():
            canal = self.bot.get_channel(self.ID_DO_CANAL)
            
            if canal is not None:
                print(f"Iniciando limpeza automática no canal: {canal.name}")
                try:
                    # O purge() sem limite apaga todas as mensagens que conseguir encontrar
                    apagadas = await canal.purge(limit=None)
                    
                    # Envia um aviso e apaga o próprio aviso após 10 segundos
                    await canal.send(
                        f"🧹 **Limpeza Automática:** {len(apagadas)} mensagens foram limpas!", 
                        delete_after=10
                    )
                    print("Limpeza concluída com sucesso.")
                except Exception as e:
                    print(f"Erro ao tentar apagar as mensagens: {e}")
            else:
                print("Erro: Canal não encontrado. Verifique se o ID está correto.")
    
    def run(self):
        """Inicia o bot"""
        self.bot.run(BOT_TOKEN)
