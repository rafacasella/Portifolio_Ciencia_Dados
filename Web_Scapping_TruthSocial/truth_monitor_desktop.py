import customtkinter as ctk
import asyncio
import threading
import re
import os
import sys
from datetime import datetime
from urllib.parse import urljoin
from playwright.async_api import async_playwright

# Configuração de Aparência e Identidade Visual (Tema Escuro + Azul Digital)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TruthMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela Desktop
        self.title("📢 Geopolitical Monitor - Truth Social Extraction Pipeline")
        self.geometry("1100x650")

        # Variáveis de Estado Operacional
        self.bot_loop = None
        self.bot_thread = None
        self.bot_rodando = False
        self.ultimo_id_visto = None

        # Configuração das Grades de Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------------------
        # BARRA LATERAL DE CONFIGURAÇÕES (PAINEL DE CONTROLE)
        # ---------------------------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.lbl_titulo = ctk.CTkLabel(self.sidebar, text="⚙️ CONFIGURAÇÕES", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_titulo.pack(padx=20, pady=(20, 10))

        self.lbl_user = ctk.CTkLabel(self.sidebar, text="Perfil Monitorado (Username):", anchor="w")
        self.lbl_user.pack(fill="x", padx=20, pady=(10, 2))
        self.txt_username = ctk.CTkEntry(self.sidebar)
        self.txt_username.insert(0, "realDonaldTrump")
        self.txt_username.pack(fill="x", padx=20, pady=5)

        self.lbl_termos = ctk.CTkLabel(self.sidebar, text="Termos de Alerta (vírgula):", anchor="w")
        self.lbl_termos.pack(fill="x", padx=20, pady=(10, 2))
        self.txt_termos = ctk.CTkEntry(self.sidebar)
        self.txt_termos.insert(0, "Iran, conflict, Hormuz, oil, taxes, tariffs")
        self.txt_termos.pack(fill="x", padx=20, pady=5)

        self.lbl_intervalo = ctk.CTkLabel(self.sidebar, text="Intervalo de Checagem (segundos):", anchor="w")
        self.lbl_intervalo.pack(fill="x", padx=20, pady=(10, 2))
        self.txt_intervalo = ctk.CTkEntry(self.sidebar)
        self.txt_intervalo.insert(0, "67")
        self.txt_intervalo.pack(fill="x", padx=20, pady=5)

        self.btn_iniciar = ctk.CTkButton(self.sidebar, text="▶️ Iniciar Monitoramento", fg_color="#1f538d", hover_color="#00f2fe", command=self.start_bot_thread)
        self.btn_iniciar.pack(fill="x", padx=20, pady=(30, 10))

        self.btn_parar = ctk.CTkButton(self.sidebar, text="⏹️ Interromper Bot", fg_color="#a62b2b", hover_color="#ff4b4b", state="disabled", command=self.stop_bot)
        self.btn_parar.pack(fill="x", padx=20, pady=10)

        # ---------------------------------------------------------------------
        # VISUALIZADOR CENTRAL DE FEEDS (CONSOLE LOGIC)
        # ---------------------------------------------------------------------
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.lbl_monitor = ctk.CTkLabel(self.main_content, text="🎯 SALA DE CONTROLE GEOPOLÍTICO (ALERTA LIVE)", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_monitor.grid(row=0, column=0, sticky="w", padx=20, pady=15)

        self.console_log = ctk.CTkTextbox(self.main_content, font=ctk.CTkFont(family="monospace", size=12), text_color="#00f2fe")
        self.console_log.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.log_txt(f"[{datetime.now().strftime('%H:%M:%S')}] Sistema Desktop pronto para execução local.")

    def log_txt(self, texto):
        self.console_log.insert("end", texto + "\n")
        self.console_log.see("end")

    def start_bot_thread(self):
        if not self.bot_rodando:
            self.bot_rodando = True
            self.btn_iniciar.configure(state="disabled")
            self.btn_parar.configure(state="normal")
            self.bot_thread = threading.Thread(target=self.rodar_evento_async, daemon=True)
            self.bot_thread.start()

    def rodar_evento_async(self):
        self.bot_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.bot_loop)
        self.bot_loop.run_until_complete(self.monitorar_truth_social())

    def stop_bot(self):
        if self.bot_rodando:
            self.bot_rodando = False
            self.log_txt(f"\n[{datetime.now().strftime('%H:%M:%S')}] ⏹️ Comando de interrupção enviado...")
            if self.bot_loop:
                self.bot_loop.call_soon_threadsafe(self.bot_loop.stop)
            self.btn_iniciar.configure(state="normal")
            self.btn_parar.configure(state="disabled")

    async def monitorar_truth_social(self):
        user = self.txt_username.get()
        termos = [p.strip() for p in self.txt_termos.get().split(",")]
        try:
            interv = int(self.txt_intervalo.get())
        except:
            interv = 67

        self.log_txt(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Inicializando monitoramento nativo para @{user}...")

        base_site = "https://truthsocial.com"
        caminho_perfil = f"@{user}"
        url_perfil = urljoin(base_site + "/", caminho_perfil)

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            dados_rede = {"posts": []}

            async def capturar_resposta(response):
                if "/api/v1/accounts/" in response.url and "/statuses" in response.url:
                    try:
                        json_dados = await response.json()
                        if isinstance(json_dados, list):
                            dados_rede["posts"] = json_dados
                    except:
                        pass

            page.on("response", capturar_resposta)

            while self.bot_rodando:
                try:
                    self.log_txt(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando requisição para API...")
                    dados_rede["posts"] = []

                    await page.goto(url_perfil, wait_until="domcontentloaded", timeout=35000)
                    await page.wait_for_timeout(5000)

                    novos_posts_detectados = []

                    if dados_rede["posts"]:
                        for post in dados_rede["posts"]:
                            id_post = str(post.get("id"))
                            texto_html = post.get("content", "")
                            texto_limpo = re.sub(r'<[^>]+>', '', texto_html).strip()
                            link_post = post.get("url")

                            if id_post.isdigit():
                                novos_posts_detectados.append({
                                    "id": id_post, "texto": texto_limpo, "link": link_post
                                })

                    if novos_posts_detectados:
                        novos_posts_detectados.sort(key=lambda x: int(x["id"]))

                        if self.ultimo_id_visto is None:
                            self.ultimo_id_visto = novos_posts_detectados[-1]["id"]
                            self.log_txt(f"✅ Sincronizado localmente com sucesso via API! Monitorando: {termos}\n")
                            await asyncio.sleep(interv)
                            continue

                        for post in novos_posts_detectados:
                            if int(post["id"]) > int(self.ultimo_id_visto):
                                texto_minusculo = post["texto"].lower()
                                termo_encontrado = [p for p in termos if p.lower() in texto_minusculo]

                                if termo_encontrado:
                                    self.log_txt(f"\n📢 [ALERTA DETECTADO] [{datetime.now().strftime('%H:%M:%S')}]")
                                    self.log_txt(f"Termos acionados: {termo_encontrado}")
                                    self.log_txt(f"Texto:\n{post['texto']}")
                                    self.log_txt(f"Link: {post['link']}")
                                    self.log_txt("-" * 50)

                                self.ultimo_id_visto = post["id"]
                    else:
                        self.log_txt(f"[{datetime.now().strftime('%H:%M:%S')}] Feed verificado. Sem novos posts. Aguardando...")

                except Exception as e:
                    self.log_txt(f"⚠️ Alerta de comunicação nesta rodada: {e}")

                await asyncio.sleep(interv)

            await browser.close()
            self.log_txt(f"[{datetime.now().strftime('%H:%M:%S')}] Navegador encerrado com segurança.")

if __name__ == "__main__":
    app = TruthMonitorApp()
    app.mainloop()
