import streamlit as st
import asyncio
import re
import sys
import os
from datetime import datetime
from urllib.parse import urljoin
from playwright.async_api import async_playwright

# =============================================================================
# INICIALIZAÇÃO DE INFRAESTRUTURA PARA AMBIENTES DE NUVEM
# =============================================================================
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/adminuser/.cache/ms-playwright"

@st.cache_resource
def inicializar_navegadores_nuvem():
    try:
        import subprocess
        print("📥 Sincronizando binários do Chromium com o ambiente Linux...")
        subprocess.run(["playwright", "install", "chromium"], check=True)
        print("✅ Navegadores prontos para execução!")
    except Exception as e:
        print(f"Aviso de infraestrutura de inicialização: {e}")

inicializar_navegadores_nuvem()

# =============================================================================
# CONTROLE DE ESTADO DA SESSÃO (Evita perda de dados ao atualizar a interface)
# =============================================================================
if "historico_posts" not in st.session_state:
    st.session_state.historico_posts = []
if "alertas_disparados" not in st.session_state:
    st.session_state.alertas_disparados = []
if "ultimo_id" not in st.session_state:
    st.session_state.ultimo_id = None
if "bot_rodando" not in st.session_state:
    st.session_state.bot_rodando = False

# =============================================================================
# SIDEBAR DE CONFIGURAÇÃO OPERACIONAL
# =============================================================================
st.sidebar.header("⚙️ Parâmetros Operacionais")
user_input = st.sidebar.text_input("Perfil Monitorado (Username):", value="realDonaldTrump")
palavras_input = st.sidebar.text_input("Termos de Alerta (separados por vírgula):", value="Iran, conflict, Hormuz, oil, taxes, tariffs")
intervalo = st.sidebar.slider("Intervalo de Checagem (segundos):", min_value=10, max_value=300, value=67)

# Tratamento dos inputs da barra lateral
lista_palavras = [p.strip() for p in palavras_input.split(",")]

# Botões de Comando do Pipeline
col_btn1, col_btn2 = st.sidebar.columns(2)
if col_btn1.button("▶️ Iniciar Bot", use_container_width=True):
    st.session_state.bot_rodando = True
if col_btn2.button("⏹️ Pausar Bot", use_container_width=True):
    st.session_state.bot_rodando = False

# =============================================================================
# BLOCO VISUAL 1: PAINEL DE MÉTRICAS (KPIs)
# =============================================================================
met1, met2, met3 = st.columns(3)
status_bot = "🟢 ATIVO / EXECUTANDO" if st.session_state.bot_rodando else "🔴 INTERROMPIDO"
met1.metric(label="Status do Pipeline", value=status_bot)
met2.metric(label="Total de Posts Varridos", value=len(st.session_state.historico_posts))
met3.metric(label="Alertas de Mercado Acionados", value=len(st.session_state.alertas_disparados), delta=f"{len(st.session_state.alertas_disparados)} Alvos Críticos")

st.markdown("---")

# =============================================================================
# ABAS DE NAVEGAÇÃO DE DADOS
# =============================================================================
tab_alertas, tab_feed = st.tabs(["🎯 Alertas Disparados (Market Sinais)", "📋 Todos os Posts Capturados (Raw Feed)"])

with tab_alertas:
    st.subheader("🚨 Feed de Alertas Críticos Ativados")
    if not st.session_state.alertas_disparados:
        st.info("Nenhum post recente acionou as palavras-chave configuradas.")
    else:
        for alerta in reversed(st.session_state.alertas_disparados):
            st.markdown(f"""
                <div class="alert-card">
                    <p style='color:#ff4b4b; font-weight:bold; margin-bottom:5px;'>📢 TERMOS ENCONTRADOS: {alerta['termos']} | 🕒 {alerta['data']}</p>
                    <p style='font-size:15px;'>{alerta['texto']}</p>
                    <a href='{alerta['link']}' target='_blank' style='color:#00f2fe; text-decoration:none; font-weight:bold;'>Ver post original no Truth Social →</a>
                </div>
            """, unsafe_allow_html=True)

with tab_feed:
    st.subheader("📊 Ingestão de Dados via Rede do Truth Social")
    if not st.session_state.historico_posts:
        st.info("Aguardando primeira execução do web scraper para exibir o log de rede.")
    else:
        for post in reversed(st.session_state.historico_posts):
            st.markdown(f"""
                <div class="post-card">
                    <p style='color:#00f2fe; font-size:12px; margin-bottom:5px;'>ID: {post['id']}</p>
                    <p style='font-size:14px;'>{post['texto']}</p>
                </div>
            """, unsafe_allow_html=True)

# =============================================================================
# CORE LOGIC: PIPELINE DE EXTRAÇÃO ADAPTADO PARA STREAMLIT
# =============================================================================
async def executar_rodada_scrapper():
    base_site = "https://truthsocial.com"
    caminho_perfil = f"@{user_input}"
    url_perfil = urljoin(base_site + "/", caminho_perfil)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox"])
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
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

        try:
            await page.goto(url_perfil, wait_until="domcontentloaded", timeout=35000)
            await page.wait_for_timeout(5000)

            if dados_rede["posts"]:
                novos_posts = []
                for post in dados_rede["posts"]:
                    id_post = str(post.get("id"))
                    texto_html = post.get("content", "")
                    texto_limpo = re.sub(r'<[^>]+>', '', texto_html).strip()
                    link_post = post.get("url")

                    if id_post.isdigit():
                        novos_posts.append({"id": id_post, "texto": texto_limpo, "link": link_post})

                if novos_posts:
                    novos_posts.sort(key=lambda x: int(x["id"]))

                    # Sincronização inicial do ID caso seja a primeira rodada
                    if st.session_state.ultimo_id is None:
                        st.session_state.ultimo_id = novos_posts[-1]["id"]
                        st.session_state.historico_posts = novos_posts
                    else:
                        for np in novos_posts:
                            # Adiciona novos posts ao histórico geral se não estiver contido
                            if np not in st.session_state.historico_posts:
                                st.session_state.historico_posts.append(np)

                            # Avalia gatilho de inteligência artificial/termos
                            if int(np["id"]) > int(st.session_state.ultimo_id):
                                texto_min = np["texto"].lower()
                                termos_achados = [p for p in lista_palavras if p.lower() in texto_min]

                                if termos_achados:
                                    st.session_state.alertas_disparados.append({
                                        "termos": ", ".join(termos_achados),
                                        "data": datetime.now().strftime('%H:%M:%S'),
                                        "texto": np["texto"],
                                        "link": np["link"]
                                    })
                                st.session_state.ultimo_id = np["id"]
        except Exception as e:
            st.sidebar.error(f"Alerta de comunicação de rede: {e}")
        finally:
            await browser.close()

# Loop de Controle reativo do Streamlit para manter o robô rodando vivo em background
if st.session_state.bot_rodando:
    with st.spinner(f"Aguardando janela de verificação operacional... ({intervalo}s)"):
        asyncio.run(executar_rodada_scrapper())
        # Pausa antes da interface forçar a re-execução (atualizando dados na tela)
        st.wait_for_timeout(1000 * intervalo)
        st.rerun()
