from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from assistente import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = os.getenv("MODELO_GERAL")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")

introducao = carrega("E:/Projetos/iart_verum/dados/introducao_requisitos_tecnicos.txt")

def bot(prompt):
    maximo_tentativas = 1  # Define o número máximo de tentativas de comunicação com a API da OpenAI
    repeticao = 0  # Inicializa o contador de repetições

    while True:  # Loop infinito para tentar a comunicação com a API
        try:
            prompt_do_sistema = f"""
            Você é o IART Verum um assistente que auxilia na contrução de RTs utilize sempre o arquivo {introducao}
            para inicar a conversa com o usuário.
            """  # Mensagem de introdução do sistema

            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_do_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo
                )  # Faz a chamada para a API da OpenAI para obter a resposta do assistente virtual
            return response  # Retorna a resposta do assistente virtual
        

        except Exception as erro:  # Trata exceções que possam ocorrer durante a comunicação com a API
            repeticao += 1  # Incrementa o contador de repetições
            if repeticao >= maximo_tentativas:  # Verifica se atingiu o número máximo de tentativas
                return "Erro no GPT: %s" % erro  # Retorna uma mensagem de erro
            print('Erro de comunicação com OpenAI: ', erro)  # Imprime o erro ocorrido na comunicação
            sleep(1)  # Aguarda 1 segundo antes de tentar novamente


@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    print(resposta)
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
