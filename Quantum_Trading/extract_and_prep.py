import pandas as pd
import numpy as np
import yfinance as yf

def extrair_dados_financeiros(ticker, data_inicio, data_fim):
    """
    Passo 1: Coleta dados históricos estruturados diretamente do Yahoo Finance.
    """
    print(f"Baixando dados históricos para o ativo: {ticker}...")
    # Realiza o download dos dados brutos com ajuste automático de splits e dividendos
    dados = yf.download(ticker, start=data_inicio, end=data_fim, auto_adjust=True)

    # Se o yfinance retornar colunas MultiIndex, simplifica para um nível básico
    if isinstance(dados.columns, pd.MultiIndex):
        dados.columns = dados.columns.get_level_values(0)

    return dados

def calcular_metricas_preditivas(df):
    """
    Passo 2: Engenharia de Features. Transforma dados brutos de preço em
    métricas matemáticas (padrões descritivos) para alimentar a IA.
    """
    print("Calculando indicadores matemáticos e métricas preditivas...")
    df = df.copy()

    # 1. Retorno Diário (Volatilidade básica do ativo)
    df['Retorno_Diario'] = df['Close'].pct_change()

    # 2. Médias Móveis Simples (SMA) - Rastreadores de tendência pura
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_30'] = df['Close'].rolling(window=30).mean()

    # 3. Índice de Força Relativa (RSI) - Medidor de Momento (Sobracompra / Sobrevenda)
    delta = df['Close'].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = ganho / (perda + 1e-10) # Evita divisão por zero
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # 4. Bandas de Bollinger (Volatilidade e desvio estatístico do preço)
    df['Media_Bollinger_20'] = df['Close'].rolling(window=20).mean()
    df['Desvio_Bollinger_20'] = df['Close'].rolling(window=20).std()
    df['Bollinger_Superior'] = df['Media_Bollinger_20'] + (df['Desvio_Bollinger_20'] * 2)
    df['Bollinger_Inferior'] = df['Media_Bollinger_20'] - (df['Desvio_Bollinger_20'] * 2)

    # =========================================================================
    # Passo 3: Criação do Alvo Preditivo (Target para Aprendizado Supervisionado)
    # A IA vai tentar prever se o fechamento do PRÓXIMO DIA será MAIOR que o de hoje.
    # =========================================================================
    df['Preco_Amanha'] = df['Close'].shift(-1)
    df['Alvo_IA'] = np.where(df['Preco_Amanha'] > df['Close'], 1, 0)

    # Limpa linhas com valores nulos causados pelas janelas de cálculo móvel (rolling/shift)
    df.dropna(inplace=True)

    return df

# =============================================================================
# BLOCO DE EXECUÇÃO LOCAL (Para testar o script no seu terminal)
# =============================================================================
if __name__ == "__main__":
    # Vamos usar PETR4 como exemplo prático de alta liquidez no mercado brasileiro
    TICKER_ALVO = "PETR4.SA"
    DATA_START = "2020-01-01"
    DATA_END = "2026-06-01" # Ajustado para dados históricos consistentes

    # Executa a esteira de dados
    dados_brutos = extrair_dados_financeiros(TICKER_ALVO, DATA_START, DATA_END)
    dados_processados = calcular_metricas_preditivas(dados_brutos)

    # Exibe no terminal uma prévia para conferência estrutural
    print("\n Extração e Engenharia concluídas com Sucesso!")
    print(f"Total de registros gerados prontos para a IA: {len(dados_processados)}")
    print("\nVisualização das primeiras linhas da matriz de Features:")
    print(dados_processados[['Close', 'RSI_14', 'SMA_10', 'Alvo_IA']].head())

    # Salva em formato CSV local para que o script de treinamento possa carregar depois
    dados_processados.to_csv("features_mercado.csv")
    print("\nArquivo 'features_mercado.csv' salvo com sucesso!")