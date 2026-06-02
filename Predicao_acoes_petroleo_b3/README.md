# Modelagem Preditiva de Preços para Ações do Setor Petrolífero

Este projeto implementa um modelo de Inteligência Artificial baseado em redes neurais para prever o preço de fechamento de grandes empresas do setor petrolífero e de energia do mercado brasileiro.

## 🎯 Objetivo do Projeto

Prever o comportamento do preço das ações de quatro grandes players do setor petrolífero e de energia:
* **Petrobras (PETR4)**
* **Prio (PRIO3)**
* **Ultrapar (UGPA3)**
* **Cosan (CSAN3)**

O sistema utiliza dados históricos de séries temporais para identificar padrões e auxiliar na tomada de decisões estratégicas de investimentos.

## 🧠 Por que utilizar a rede LSTM?

A arquitetura **LSTM (Long Short-Term Memory)** foi escolhida por ser uma variação especializada de Redes Neurais Recorrentes (RNN) ideal para este problema.

* **Dados Sequenciais:** Perfeita para modelar séries temporais financeiras.
* **Dependências de Longo Prazo:** Consegue capturar relações de tempo distantes no histórico.
* **Histórico Longo:** Lida eficientemente com grandes volumes de dados passados.
* **Memória Seletiva:** Suas portas internas evitam o problema do *vanishing gradient* (desaparecimento do gradiente).
* **Padrões Complexos:** Excelente capacidade para capturar movimentos sazonais e cíclicos do mercado de commodities.

### 📊 Prós e Contras da LSTM


| Vantagens (✅) | Desvantagens (❌) |
| :--- | :--- |
| Memória de longo prazo robusta | Requer grande volume de dados para treino |
| Captura tendências complexas e sazonalidade | Processamento computacionalmente custoso |
| Estado da arte para previsão de séries temporais | Hiperparâmetros altamente sensíveis |

## 🛠️ Tecnologias e Bibliotecas Principais

* **TensorFlow / Keras:** Construção, treinamento e avaliação da rede neural profunda LSTM.
* **Scikit-Learn:** Separação de dados, pré-processamento (escalagem) e métricas de validação.
* **Pandas & NumPy:** Manipulação algorítmica e estruturação dos dados financeiros.

## 🔧 Principais Ajustes e Arquitetura do Modelo

### 1. Escalagem dos Dados e Prevenção de Data Leakage
A separação entre os dados de **Treino** e **Teste** é feita **ANTES** de aplicar a escala nos dados (como o `MinMaxScaler`). 
* **Por que fazer isso?** Aplicar o scaler em todo o DataFrame de uma vez causaria *data leakage* (vazamento de dados). O modelo "preveria o futuro" de forma artificial porque conheceria previamente o valor máximo global que só aconteceria na base de teste.

### 2. Criação de Janelas Temporais (Multivariada)
O modelo foi estruturado utilizando **janelas temporais de 60 dias**.
* **Necessidade:** Redes LSTM não conseguem prever o amanhã olhando apenas para um dia isolado. Elas precisam de contexto sequencial para identificar tendências.
* **Como a rede enxerga:** Para estimar o preço do dia seguinte, a rede analisa se a ação subiu ou caiu nos últimos dois meses. Essa janela fornece o histórico para as células da LSTM decidirem quais informações reter ou descartar.

### 3. Camadas e Hiperparâmetros
* **Units (50):** Define o número de valores e estados que a célula memoriza do passado em cada camada.
* **Dropout (20%):** A cada iteração do treino, 20% dos neurônios são desligados aleatoriamente. Isso força a rede a não memorizar os dados (overfitting), tornando o modelo muito mais generalista.
* **Early Stopping:** Técnica de interrupção implementada para parar o treinamento automaticamente assim que o erro de validação parar de cair, economizando tempo computacional e evitando o sobreajuste.

## 📈 Erro e Validação

O sucesso do modelo é medido através de duas métricas principais expressas em formato percentual:

* **MAE (%) / MAPE (Erro Médio Absoluto Percentual):** Representa o erro percentual médio diário das previsões. 
  * *Exemplo:* Um MAE de 2,5% significa que as previsões erram, em média, 2,5% para cima ou para baixo do valor real da ação.
* **RMSE (%) (Raiz do Erro Quadrático Médio):** Mostra o desvio padrão dos erros de forma percentual. Como penaliza erros maiores severamente, é ideal para checar se o modelo sofreu "sustos" ou falhas graves em dias de alta volatilidade do setor petrolífero.

## 🚀 Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script principal ou Jupyter Notebook para treinar e avaliar o modelo.