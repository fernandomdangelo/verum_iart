from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = os.getenv("MODELO_GERAL")

#Implementando Threads: As threads são a capacidade que o nosso assistente tem de garantir que todas as mensagens trocadas em uma mesma sessão possam ser acessadas antes, depois ou a qualquer momento. 

def criar_thread():
    return cliente.beta.threads.create()

