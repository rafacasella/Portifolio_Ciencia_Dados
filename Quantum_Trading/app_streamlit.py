import streamlit as pd_st
import pandas as pd
import plotly.graph_objects as go

# Configuração da página e layout do Dashboard
pd_st.set_page_config(page_title="IA Quant Trading", layout="wide")

# Estilização em CSS para embutir perfeitamente no iframe transparente do portfólio
pd_st.markdown("""
    <style>
        .main {background-color: #0b0f19; color: #ffffff;}
        div[data-testid="stMetricValue"] {color: #00f2fe; font-family: monospace; font-size: 28px;}
        div[data-testid="stMetricLabel"] {color: #a0aec0;}
        h1, h2, h3 {color: #ffffff; font-family: 'Helvetica Neue', sans-serif;}
    </style>
""", unsafe_allow_html=True)

pd_st.title("🤖 Inteligência Artificial aplicada ao Trading Quantitativo")
pd_st.subheader("Simulação de Performance e Sinais de Direção do Mercado")

@pd_st.cache_data
def carregar_dados_consolidados():
    """
    Carrega a planilha final com os resultados calculados pelo script de backtest.
    """
    try:
        df = pd.read_csv("resultado_final_backtest.csv", index_col=0, parse_dates=True)
        return df
    except FileNotFoundError:
        return None

# Carregamento do pipeline de dados
df_resultado = carregar_dados_consolidados()

if df_resultado is not None:
    # -------------------------------------------------------------------------
    # 1. BLOCO SUPERIOR: CARTÕES DE MÉTRICAS QUANTITATIVAS
    # -------------------------------------------------------------------------
    # Extração dos valores finais da série temporal
    retorno_ia = (df_resultado['Capital_Acumulado_IA'].iloc[-1] - 1) * 100
    retorno_mercado = (df_resultado['Capital_Acumulado_Mercado'].iloc[-1] - 1) * 100

    # Cálculo dinâmico do Sharpe Ratio do período
    ret_estr = df_resultado['Retorno_Estrategia']
    sharpe = (ret_estr.mean() / (ret_estr.std() + 1e-10)) * (252 ** 0.5) if ret_estr.std() > 0 else 0

    # Cálculo do Drawdown Máximo
    picos = df_resultado['Capital_Acumulado_IA'].cummax()
    dds = (df_resultado['Capital_Acumulado_IA'] - picos) / picos
    max_dd = dds.min() * 100

    # Renderização das colunas visuais no Streamlit
    met1, met2, met3, met4 = pd_st.columns(4)
    met1.metric(label="Retorno Acumulado (IA)", value=f"{retorno_ia:.2f}%", delta=f"{retorno_ia - retorno_mercado:.2f}% vs Mercado")
    met2.metric(label="Retorno Buy & Hold", value=f"{retorno_mercado:.2f}%")
    met3.metric(label="Sharpe Ratio Anualizado", value=f"{sharpe:.2f}")
    met4.metric(label="Drawdown Máximo Histórico", value=f"{max_dd:.2f}%")

    pd_st.markdown("---")

    # -------------------------------------------------------------------------
    # 2. BLOCO CENTRAL: GRÁFICO DA CURVA DE EVOLUÇÃO DE CAPITAL (PLOTLY)
    # -------------------------------------------------------------------------
    pd_st.subheader("📈 Evolução do Patrimônio: Estratégia IA vs. Buy & Hold")

    fig = go.Figure()

    # Linha de capital da Inteligência Artificial (Utiliza a cor Azul/Digital do seu nicho)
    fig.add_trace(go.Scatter(
        x=df_resultado.index,
        y=df_resultado['Capital_Acumulado_IA'],
        mode='lines',
        name='Estratégia Quant (IA)',
        line=dict(color='#00f2fe', width=2.5)
    ))

    # Linha de capital do mercado de referência (Cor cinza para dar contraste e destacar o seu modelo)
    fig.add_trace(go.Scatter(
        x=df_resultado.index,
        y=df_resultado['Capital_Acumulado_Mercado'],
        mode='lines',
        name='Buy & Hold (Mercado Puro)',
        line=dict(color='#4a5568', width=1.5, dash='dash')
    ))

    # Customização visual do gráfico para o tema escuro do portfólio
    fig.update_layout(
        template="plotly_dark",
        backgroundColor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor='#1e293b'),
        yaxis=dict(showgrid=True, gridcolor='#1e293b', title="Multiplicador de Capital (Base 1.0)"),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    pd_st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------------
    # 3. BLOCO INFERIOR: PAINEL DE ÚLTIMOS SINAIS GERADOS
    # -------------------------------------------------------------------------
    pd_st.markdown("---")
    pd_st.subheader("🎯 Últimos Direcionamentos e Probabilidades Computadas pela IA")

    # Filtra as últimas 5 linhas do histórico para prestação de contas dos sinais mais recentes
    ultimos_sinais = df_resultado[['Close', 'Probabilidade_Alta', 'Sinal_IA']].tail(5).copy()
    ultimos_sinais['Sinal_IA'] = ultimos_sinais['Sinal_IA'].map({1: "🟢 COMPRA (Alta)", 0: "🔴 FORA (Queda)"})
    ultimos_sinais['Probabilidade_Alta'] = ultimos_sinais['Probabilidade_Alta'].map(lambda x: f"{x*100:.2f}%")
    ultimos_sinais.columns = ['Preço de Fechamento', 'Probabilidade de Alta', 'Sinal Emitido pela IA']

    pd_st.dataframe(ultimos_sinais, use_container_width=True)

else:
    # Aviso estrutural caso os scripts Python anteriores ainda não tenham rodado no diretório
    pd_st.error("⚠️ Planilha de resultados ('resultado_final_backtest.csv') não localizada no diretório.")
    pd_st.markdown("Por favor, execute o pipeline em ordem no seu computador para alimentar a interface:")
    pd_st.code("python extract_and_prep.py\npython train.py\npython backtest.py")
