import pandas as pd
import numpy as np

def executar_backtest_financeiro(caminho_previsoes):
    """
    Simula a execução financeira da estratégia baseada nos sinais da IA
    e calcula métricas de desempenho ajustadas ao risco de mercado.
    """
    print(f"Carregando dados de previsões de: {caminho_previsoes}...")
    df = pd.read_csv(caminho_previsoes, index_col=0, parse_dates=True)
    df.sort_index(inplace=True)

    # 1. Alinhamento dos Sinais
    # O Sinal_IA gerado hoje no fechamento dita nossa posição para o retorno de amanhã.
    # Usamos o .shift(1) para garantir que a decisão foi tomada ANTES do movimento acontecer.
    df['Posicao_Estrategia'] = df['Sinal_IA'].shift(1)

    # 2. Cálculo dos Retornos Financeiros
    # Retorno da estratégia = Retorno do ativo multiplicada pela nossa posição (0 ou 1)
    df['Retorno_Ativo'] = df['Close'].pct_change()
    df['Retorno_Estrategia'] = df['Retorno_Ativo'] * df['Posicao_Estrategia']

    # Substitui os valores nulos iniciais por zero para manter a consistência matemática
    df['Retorno_Estrategia'].fillna(0, inplace=True)
    df['Retorno_Ativo'].fillna(0, inplace=True)

    # 3. Evolução do Capital Acumulado (Curva de Equity partindo de 1.0 ou 100%)
    df['Capital_Acumulado_IA'] = (1 + df['Retorno_Estrategia']).cumprod()
    df['Capital_Acumulado_Mercado'] = (1 + df['Retorno_Ativo']).cumprod()

    # =========================================================================
    # 4. EXTRAÇÃO DE MÉTRICAS QUANTITATIVAS (Métricas de Fundo de Investimento)
    # =========================================================================

    # Retorno Nominal Total
    retorno_total_ia = (df['Capital_Acumulado_IA'].iloc[-1] - 1) * 100
    retorno_total_mercado = (df['Capital_Acumulado_Mercado'].iloc[-1] - 1) * 100

    # Sharpe Ratio Anualizado (Mede retorno vs volatilidade assumida)
    # Considera 252 dias úteis de negociação no ano e taxa livre de risco zero para simplificação
    retorno_medio_diario = df['Retorno_Estrategia'].mean()
    desvio_padrao_diario = df['Retorno_Estrategia'].std()

    if desvio_padrao_diario > 0:
        sharpe_ratio = (retorno_medio_diario / desvio_padrao_diario) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # Maximum Drawdown (MDD - Maior prejuízo sofrido do topo histórico ao fundo subsequente)
    picos_capital = df['Capital_Acumulado_IA'].cummax()
    drawdowns = (df['Capital_Acumulado_IA'] - picos_capital) / picos_capital
    max_drawdown = drawdowns.min() * 100

    print("\n=======================================================")
    print("        RELATÓRIO DE DESEMPENHO DO BACKTEST            ")
    print("=======================================================")
    print(f" Retorno Total da IA no período:     {retorno_total_ia:.2f}%")
    print(f" Retorno Buy & Hold (Mercado Puro):   {retorno_total_mercado:.2f}%")
    print(f" Sharpe Ratio Anualizado da IA:      {sharpe_ratio:.2f}")
    print(f" Drawdown Máximo Histórico da IA:    {max_drawdown:.2f}%")
    print("=======================================================\n")

    return df

# =============================================================================
# BLOCO DE EXECUÇÃO LOCAL (Para testar o script no seu terminal)
# =============================================================================
if __name__ == "__main__":
    ARQUIVO_PREVISOES = "previsoes_ia_mercado.csv"

    try:
        df_resultado_final = executar_backtest_financeiro(ARQUIVO_PREVISOES)

        # Salva a planilha consolidada que contém as curvas de capital para plotarmos no Streamlit
        df_resultado_final.to_csv("resultado_final_backtest.csv")
        print("Planilha 'resultado_final_backtest.csv' gerada! Pronta para o Dashboard Visual.")

    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{ARQUIVO_PREVISOES}' não foi encontrado.")
        print("Execute o script de treinamento ('train.py') primeiro para computar as previsões da IA.")
