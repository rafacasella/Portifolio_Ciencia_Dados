import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def treinar_inteligencia_artificial(caminho_csv):
    """
    Carrega a matriz de features, divide os dados temporalmente,
    treina o modelo de Machine Learning e avalia sua acurácia preditiva.
    """
    print(f"Carregando a matriz de features de: {caminho_csv}...")
    # Carrega os dados garantindo que a data seja tratada como índice ordenado
    df = pd.read_csv(caminho_csv, index_col=0, parse_dates=True)
    df.sort_index(inplace=True)

    # 1. Definição das colunas preditivas (Features) e da coluna alvo (Target)
    colunas_features = [
        'Retorno_Diario', 'RSI_14',
        'SMA_10', 'SMA_30',
        'Bollinger_Superior', 'Bollinger_Inferior'
    ]

    X = df[colunas_features]
    y = df['Alvo_IA']

    # =========================================================================
    # 2. Divisão Temporal Estrita (Time Series Split)
    # NÃO podemos usar train_test_split aleatório em finanças para evitar Data Leakage.
    # Usaremos os primeiros 80% dos dados para Treino e os últimos 20% para Teste.
    # =========================================================================
    tamanho_treino = int(len(df) * 0.8)

    X_train, X_test = X.iloc[:tamanho_treino], X.iloc[tamanho_treino:]
    y_train, y_test = y.iloc[:tamanho_treino], y.iloc[tamanho_treino:]

    print(f"Registros para Treinamento (Passado): {len(X_train)}")
    print(f"Registros para Teste Fora da Amostra (Futuro): {len(X_test)}")

    # =========================================================================
    # 3. Inicialização e Treinamento do Modelo
    # Random Forest é excelente para dados não-lineares e reduz o risco de overfitting
    # =========================================================================
    print("\nIniciando o treinamento do modelo Random Forest...")
    modelo = RandomForestClassifier(
        n_estimators=100,     # Número de árvores de decisão na floresta
        max_depth=5,          # Profundidade máxima controlada para evitar decoreba (overfitting)
        random_state=42,       # Garante que o resultado seja reproduzível
        n_jobs=-1             # Usa todos os núcleos do processador para acelerar
    )

    modelo.fit(X_train, y_train)
    print("Modelo treinado com sucesso!")

    # =========================================================================
    # 4. Avaliação Estatística de Precisão Preditiva
    # =========================================================================
    predicoes_teste = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, predicoes_teste)

    print("\n=======================================================")
    print(f" ACURÁCIA PRECOGNITIVA DA IA: {acuracia * 100:.2f}%")
    print("=======================================================")

    print("\nRelatório Técnico de Classificação (Métricas de Finanças):")
    print(classification_report(y_test, predicoes_teste, target_names=['Queda/Empate (0)', 'Alta (1)']))

# Adiciona as previsões e probabilidades de volta ao bloco de teste para o backtest posterior
    df_resultados_teste = df.iloc[tamanho_treino:].copy()
    df_resultados_teste['Sinal_IA'] = predicoes_teste

# Captura a probabilidade calculada pela IA para cada previsão
    probabilidades = modelo.predict_proba(X_test)
    df_resultados_teste['Probabilidade_Alta'] = probabilidades[:, 1]

    return df_resultados_teste, modelo

# =============================================================================
# BLOCO DE EXECUÇÃO LOCAL (Para testar o script no seu terminal)
# =============================================================================
if __name__ == "__main__":
    ARQUIVO_FEATURES = "features_mercado.csv"

    try:
        # Executa a esteira de treinamento
        dados_backtest, modelo_final = treinar_inteligencia_artificial(ARQUIVO_FEATURES)

        # Salva as previsões em um novo CSV que será consumido pelo simulador financeiro
        dados_backtest.to_csv("previsoes_ia_mercado.csv")
        print("\nArquivo 'previsoes_ia_mercado.csv' gerado com sucesso para o Backtest!")

    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{ARQUIVO_FEATURES}' não foi encontrado.")
        print("Execute o script de extração ('extract_and_prep.py') primeiro para gerar a base de dados.")
