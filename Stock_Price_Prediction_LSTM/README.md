# Predictive Price Modeling for Oil Sector Stocks

This project implements an Artificial Intelligence model based on neural networks to predict the closing price of major oil and energy companies in the Brazilian stock market.

## 🎯 Project Objective

Predict price behavior for four major players in the oil and energy sector:
* **Petrobras (PETR4)**
* **Prio (PRIO3)**
* **Ultrapar (UGPA3)**
* **Cosan (CSAN3)**

The system utilizes historical time series data to identify patterns and support strategic investment decision-making.

## 🧠 Why Use LSTM Networks?

The **LSTM (Long Short-Term Memory)** architecture was selected because it is a specialized variation of Recurrent Neural Networks (RNN) ideal for this problem.

* **Sequential Data:** Perfect for modeling financial time series.
* **Long-Term Dependencies:** Captures time relationships distant in the history.
* **Long Historical Record:** Efficiently handles large volumes of past data.
* **Selective Memory:** Internal gates prevent the vanishing gradient problem.
* **Complex Patterns:** Excellent capability to capture seasonal and cyclical movements of the commodities market.

### 📊 LSTM Pros and Cons


| Advantages (✅) | Disadvantages (❌) |
| :--- | :--- |
| Robust long-term memory | Requires large volume of training data |
| Captures complex trends and seasonality | Computationally expensive processing |
| State-of-the-art for time series forecasting | Highly sensitive hyperparameters |

## 🛠️ Core Tech Stack & Libraries

* **TensorFlow / Keras:** Construction, training, and evaluation of the deep LSTM neural network.
* **Scikit-Learn:** Data splitting, preprocessing (scaling), and validation metrics.
* **Pandas & NumPy:** Algorithmic manipulation and structuring of financial data.

## 🔧 Core Model Architecture & Adjustments

### 1. Data Scaling & Data Leakage Prevention
The split between **Train** and **Test** data is performed **BEFORE** applying data scaling (such as `MinMaxScaler`). 
* **Why do this?** Applying the scaler to the entire DataFrame at once would cause *data leakage*. The model would artificially "predict the future" because it would have prior knowledge of the global maximum value that only occurs within the test set.

### 2. Time Window Creation (Multivariate)
The model was structured utilizing **60-day time windows**.
* **The Need:** LSTM networks cannot predict tomorrow by looking at a single isolated day. They require sequential context to identify trends.
* **How the Network Sees It:** To estimate the next day's price, the network analyzes whether the stock rose or fell over the last two months. This window provides the history for the LSTM cells to decide which information to retain or discard.

### 3. Layers & Hyperparameters
* **Units (50):** Defines the number of values and states the cell memorizes from the past in each layer.
* **Dropout (20%):** During each training iteration, 20% of the neurons are randomly deactivated. This forces the network to avoid memorizing data (overfitting), making the model much more generalizable.
* **Early Stopping:** An implementation technique to automatically halt training as soon as validation loss stops decreasing, saving computational time and preventing overfitting.

## 📈 Error & Validation

Model success is measured through two primary metrics expressed in percentage format:

* **MAE (%) / MAPE (Mean Absolute Percentage Error):** Represents the average daily percentage error of the predictions. 
  * *Example:* A 2.5% MAE means that predictions miss, on average, by 2.5% above or below the actual stock value.
* **RMSE (%) (Root Mean Squared Error):** Displays the standard deviation of errors in a percentage format. Since it severely penalizes larger errors, it is ideal for checking whether the model suffered major failures during high-volatility days in the oil sector.

## 🚀 How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script or Jupyter Notebook to train and evaluate the model.
