import yfinance as yf
import json

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def cotacao_historica(ticker:str, periodo:str = '1mo') -> dict:
    dat = yf.Ticker(ticker)
    hist = dat.history(period=periodo)['Close']
    hist.index = hist.index.strftime('%Y-%m-%d')
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    return hist.to_json()

print(cotacao_historica('PETR4.SA'))

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
                        "description": "O ticker da ação. Exemplo: 'PETR4.SA' para a petrobras",
                    },
                    "periodo": {
                        "type": "string", 
                        'description': 'Período que será retornado de dados históricos sendo "1d","1mo"',
                        'enum': ['1d','5d','1mo', '6mo', '1y', '5y', '10y', 'ytd', 'max']
                    },
                },
                "required": ["ticker"],
            },
        },
    }
    ]

funcoes_disponiveis = {'cotacao_historica' : cotacao_historica}

