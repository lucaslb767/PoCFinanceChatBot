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

mensagens = [{'role': 'user', 'content': 'Qual é a cotação da Microsoft agora?'}]



resposta = client.chat.completions.create(
    messages= mensagens,
    model = 'gpt-4-turbo-2024-04-09',
    tools = tools,
    tool_choice="auto"
)

tool_calls = resposta.choices[0].message.tool_calls

if tool_calls:
    mensagens.append(resposta.choices[0].message)
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[func_name]
        func_args = json.loads(tool_call.function.arguments)
        func_return = function_to_call(**func_args)
        mensagens.append({
            'tool_call_id': tool_call.id,
            'role': 'tool',
            'name': func_name,
            'content': func_return
        })
        segunda_resposta = client.chat.completions.create(
            messages=mensagens,
            model = 'gpt-4-turbo-2024-04-09'
        )
        print(segunda_resposta.choices[0].message)
        mensagens.append(segunda_resposta.choices[0].message)


