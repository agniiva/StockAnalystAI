# AI Financial Analyst Bot
Note: If you're searching Any Stock use the TICKER SYMBOL (e.g. PATANJALI.NS) (in some cases normal names doesn't work) - I can improve on it, but who cares!!

## Overview

### What is AI Financial Analyst Bot?

The AI Financial Analyst Bot is an intelligent application designed to provide comprehensive financial analysis and insights for any given company. It leverages OpenAI's GPT-3 model for analysis, yfinance for historical stock data, yahooquery for financial statements, and serper.dev for news retrieval.

### Why is it Useful?

Investing in the stock market often requires hours of research, financial literacy, and keeping up with news. This bot automates these tasks by providing a one-stop solution for all your research needs. It not only provides raw data but also offers AI-powered insights to make your investment decisions more informed.

### Unique Selling Points (USPs)

1. **One-Click Analysis**: Just input the company name and get a detailed analysis.
2. **Real-Time Company News**: Stay updated with the latest news related to the company.
3. **Comprehensive Data**: Get everything from stock evolution to balance sheets.
4. **AI-Powered Insights**: Receive detailed investment theses and recommendations.
5. **Multi-Source Analysis**: Data is retrieved from multiple reliable sources for a well-rounded view.

## 🚀 Features

- **Company News Retrieval**: Uses serper.dev API to fetch the latest news related to a company.
- **Historical Stock Data**: Utilizes yfinance library to fetch historical stock data.
- **Financial Statements**: Uses yahooquery to fetch the balance sheet, cash flow, and income statements.
- **AI-Powered Analysis**: Uses OpenAI's GPT-3 model to generate in-depth financial analysis and recommendations.

## Working Demo

https://github.com/agniiva/StockAnalystAI/assets/73607864/d3774b87-7052-4e15-b7ba-713cac61c995

## Images of the analysis
<img width="990" alt="image" src="https://github.com/agniiva/StockAnalystAI/assets/73607864/43da0c32-eb86-4be7-b388-e7efa82bffc3">
<img width="994" alt="image" src="https://github.com/agniiva/StockAnalystAI/assets/73607864/a9a4a5bc-bcaf-4697-80c9-e2f0d812f008">
![Uploading image.png…]()



## Prerequisites

### API Keys

You will need API keys for OpenAI and serper.dev. Add these keys in a `.env` file in the root directory. You can rename `.env.example` to `.env` to quickly get started.

### Python Dependencies

Install all Python dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the directory containing the code.
2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Input the company name and click "Analyze".

## Code Documentation

### Importing Libraries

- `streamlit`: For the web interface
- `matplotlib.pyplot`: For plotting graphs
- `financial_analyst`: Custom module for the analysis

### `main()`

The main function that handles the Streamlit UI and invokes the financial analysis. It plots stock data and displays the investment thesis.

### `financial_analyst.py`

Contains various helper functions to fetch and analyze financial data. Here are some important functions:

#### `get_company_news(company_name)`

Fetches the latest news for the given company using the serper.dev API.

#### `write_news_to_file(news, filename)`

Writes the fetched news to a specified file.

#### `get_stock_evolution(company_name, period="1y")`

Fetches and writes historical stock data for the specified period using yfinance.

#### `get_financial_statements(ticker)`

Fetches financial statements using the yahooquery library.

#### `get_data(company_name, company_ticker, period="1y", filename="investment.txt")`

Calls all the data fetching functions and compiles the results.

#### `financial_analyst(request)`

Main function for financial analysis. Uses OpenAI's GPT-3 model to analyze the compiled data and generate an investment thesis.

---

Feel free to extend or modify the application according to your needs. Happy Investing!
