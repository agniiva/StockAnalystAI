import os
import requests
import json
from dotenv import load_dotenv
import yfinance as yf
from yahooquery import Ticker
from openai import OpenAI

client = OpenAI()

load_dotenv()
serper_api_key = os.getenv("SERP_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_company_news(company_name):
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'q': company_name
    }

    response = requests.post('https://google.serper.dev/news', headers=headers, json=data)
    data = response.json()

    return data.get('news')



def write_news_to_file(news, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for news_item in news:
            if news_item is not None:
                title = news_item.get('title', 'No title')
                link = news_item.get('link', 'No link')
                date = news_item.get('date', 'No date')
                file.write(f"Title: {title}\n")
                file.write(f"Link: {link}\n")
                file.write(f"Date: {date}\n\n")



def get_stock_evolution(company_name, period="1y"):
    # Get the stock information
    stock = yf.Ticker(company_name)
    # Get historical market data
    try:
        hist = stock.history(period=period)
    except Exception as e:
        print(e)
        return None

    # Convert the DataFrame to a string with a specific format
    data_string = hist.to_string()

    # Append the string to the "investment.txt" file
    with open("investment.txt", "a") as file:
        file.write(f"\nStock Evolution for {company_name}:\n")
        file.write(data_string)
        file.write("\n")

    # Return the DataFrame
    return hist


def get_financial_statements(ticker):
    # Create a Ticker object
    company = Ticker(ticker)
    valuation_measures = ""

    # Get financial data
    balance_sheet_data = company.balance_sheet()
    balance_sheet = balance_sheet_data.to_string() if hasattr(balance_sheet_data, 'to_string') else str(balance_sheet_data)
    
    cash_flow_data = company.cash_flow(trailing=False)
    cash_flow = cash_flow_data.to_string() if hasattr(cash_flow_data, 'to_string') else str(cash_flow_data)

    income_statement_data = company.income_statement()
    income_statement = income_statement_data.to_string() if hasattr(income_statement_data, 'to_string') else str(income_statement_data)
    
    try:
        valuation_measures = str(company.valuation_measures)  # This one might already be a dictionary or string
    except Exception as e:
        print(f"Error while getting valuation measures: {e}")
        valuation_measures = "N/A"

    # Write data to file
    with open("investment.txt", "a") as file:
        file.write("\nBalance Sheet\n")
        file.write(balance_sheet)
        file.write("\nCash Flow\n")
        file.write(cash_flow)
        file.write("\nIncome Statement\n")
        file.write(income_statement)
        file.write("\nValuation Measures\n")
        file.write(valuation_measures)





def get_data(company_name, company_ticker, period="1y", filename="investment.txt"):
    news = get_company_news(company_name)
    if news:
        write_news_to_file(news, filename)
    else:
        print("No news found.")

    hist = get_stock_evolution(company_ticker)

    get_financial_statements(company_ticker)

    return hist


def financial_analyst(request):
    print(f"Received request: {request}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[{
            "role":
            "user",
            "content":
            f"Given the user request, what is the comapany name and the company stock ticker ?: {request}?"
        }],
        functions=[{
            "name": "get_data",
            "description":
            "Get financial data on a specific company for investment purposes",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type":
                        "string",
                        "description":
                        "The name of the company",
                    },
                    "company_ticker": {
                        "type":
                        "string",
                        "description":
                        "the ticker of the stock of the company"
                    },
                    "period": {
                        "type": "string",
                        "description": "The period of analysis"
                    },
                    "filename": {
                        "type": "string",
                        "description": "the filename to store data"
                    }
                },
                "required": ["company_name", "company_ticker"],
            },
        }],
        function_call={"name": "get_data"},
    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        # Parse the arguments from a JSON string to a Python dictionary
        arguments = json.loads(message["function_call"]["arguments"])
        print(arguments)
        company_name = arguments["company_name"]
        company_ticker = arguments["company_ticker"]

        # Parse the return value from a JSON string to a Python dictionary
        hist = get_data(company_name, company_ticker)
        print(hist)

        with open("investment.txt", "r") as file:
            content = file.read()[:14000]

        second_response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "user",
                    "content": request
                },
                message,
                {
                    "role": "system",
                    "content": """Write a detailled investment thesis to answer
                      the user request as a html document. Provide numbers to justify
                      your assertions, a lot ideally. Always provide
                     a recommendation to buy the stock of the company
                     or not, given the information available,
                     give brutally honest opinions if you think we should buy it tell us to buy
                     and also be honest with it when you think we shouldn't buy, by the numbers available
                     also try to analyse if we should invest in short term or long term. Also give
                     reference to your souces. """
                },
                {
                    "role": "assistant",
                    "content": content,
                },
            ],
        )

        return (second_response["choices"][0]["message"]["content"], hist)
