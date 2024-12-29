import yfinance as yf
import json

import openai
from dotenv import load_dotenv, find_dotenv

def cotacao_historica(ticker:str, periodo:str = '1y'):
    dat = yf.Ticker(ticker)
    hist = dat.history(period=periodo)
    # print(f'info: {dat.info}')
    # print(f'calendar: {dat.calendar}')
    # print(f'analysis_price_target: {dat.analyst_price_targets}')
    # print(f'quartely income stmt: {dat.quarterly_income_stmt}')
    print(f'closing hist: {hist}')
    # print(f'option chain: {dat.option_chain(dat.options[0]).calls}')

cotacao_historica('MSFT')

tools = [
    {
        "type": "function",
        "function": {
            "name": "cotacao_historica",
            "description": "Retorna a cotação diária histórica para uma ação",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "O ticker da ação. Exemplo: 'PETR4' para a petrobras",
                    },
                    "unidade": {
                        "type": "string", 
                        "enum": ["celsius", "fahrenheit"]
                    },
                },
                "required": ["local"],
            },
        },
    }
    ]