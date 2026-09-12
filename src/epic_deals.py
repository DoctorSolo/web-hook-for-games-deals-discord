from datetime import datetime, timezone
import os
import requests
from config import YOUR_DISCORD_WEBHOOK_URL_HERE


class EpicDeals:
    def __init__(self):
        self.EPIC_API_URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"
        self.WEBHOOK_URL = os.environ.get(
            'WEBHOOK_URL',
            YOUR_DISCORD_WEBHOOK_URL_HERE  # Substitua pelo seu webhook do Discord
        )
        
        
        self.enviar_webhook()
    # END


    def obter_jogos_gratis(self):
        params = {"locale": "pt-BR", "country": "BR", "allowCountries": "BR"}
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(self.EPIC_API_URL, params=params, headers=headers)
        response.raise_for_status()

        dados = response.json()
        elementos = dados["data"]["Catalog"]["searchStore"]["elements"]

        jogos_gratuitos = []
        agora = datetime.now(timezone.utc)

        for item in elementos:
            # Preço original precisa ser maior que zero (para ignorar jogos que já são free-to-play)
            preco_base = item.get("price", {}).get("totalPrice", {}).get("originalPrice", 0)
            promocoes = item.get("promotions")

            if not promocoes:
                continue

            ofertas_ativas = promocoes.get("promotionalOffers", [])

            if ofertas_ativas and preco_base > 0:
                for oferta_grupo in ofertas_ativas:
                    for oferta in oferta_grupo.get("promotionalOffers", []):
                        # Valida se o desconto é de 100% (preço 0)
                        desconto = (
                            oferta.get("discountSetting", {}).get("discountPercentage")
                        )

                        # Validação do período da oferta
                        data_inicio = datetime.fromisoformat(
                            oferta["startDate"].replace("Z", "+00:00")
                        )
                        data_fim = datetime.fromisoformat(
                            oferta["endDate"].replace("Z", "+00:00")
                        )

                        if (
                            data_inicio <= agora <= data_fim
                            and (
                                desconto == 0
                                or item["price"]["totalPrice"]["discountPrice"] == 0
                            )
                        ):
                            # Pega a imagem de capa horizontal/thumbnail
                            imagem = None
                            for img in item.get("keyImages", []):
                                if img.get("type") in [
                                    "Thumbnail",
                                    "OfferImageWide",
                                    "DieselStoreFrontWide",
                                ]:
                                    imagem = img.get("url")
                                    break

                            # Determina o link da página do jogo
                            slug = (
                                item.get("productSlug")
                                or (item.get("catalogNs", {}).get("mappings", [{}])[0].get("pageSlug"))
                                or item.get("urlSlug")
                            )
                            link = f"https://store.epicgames.com/pt-BR/p/{slug}"

                            jogos_gratuitos.append(
                                {
                                    "titulo": item.get("title"),
                                    "descricao": item.get("description"),
                                    "link": link,
                                    "imagem": imagem,
                                    "data_fim": data_fim.strftime("%d/%m/%Y às %H:%M"),
                                }
                            )

        return jogos_gratuitos
    # END


    def enviar_webhook(self):
        
        embeds = []
        jogos = self.obter_jogos_gratis()
        for jogo in jogos:
            embeds.append(
                {
                   "title": f"🎮 Epic Games: {jogo['titulo']}",
                    #"description": jogo["descricao"],
                    "description": "💰 Free Game!",
                    "url": jogo["link"],
                    "color": 3092790,  # Cor cinza escuro/preto
                    "fields": [
                        {
                            "name": "Disponível até",
                            "value": jogo["data_fim"],
                            "inline": True,
                        }
                    ],
                    "image": {"url": jogo["imagem"]} if jogo["imagem"] else {},
                    "footer": {
                        "text": f"Free Game Promotion",
                        "icon_url": "https://github.com/DoctorSolo/web-hook-steam-deals-discord/blob/main/.github/assets/Epic-Games.svg?raw=true",
                    }, 
                }
            )
        
        if self.WEBHOOK_URL:
            requests.post(self.WEBHOOK_URL, json={"embeds": embeds}, timeout=10)
    # END