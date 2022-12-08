"""
pip install google
pip install requests
pip install pyshorteners
pip install pytz
"""

import json
import requests
from time import sleep
from threading import Thread, Lock

global config
config = {"url": "https://api.telegram.org/bot5751503927:AAGwT-E4cpQHQlvE5bZLHqpKyDbB8xZoXCU/", "lock": Lock()}


def get_men():
    try:
        global x
        x = json.loads(requests.get(config["url"] + "getUpdates").text)
    except Exception as e:
        x = ""
        if "Failed to establish a new connection" in str(e):
            print("perca de conexão")
        else:
            print("erro desconhecido " + str(e))


def del_up(mensagem):
    global config
    config["lock"].acquire()
    requests.post(config["url"] + "getUpdates",{"offset": mensagem["update_id"]+1})
    config["lock"].release()


def enviar_mensagem(mensagem, msg):
    global config

    config["lock"].acquire()
    requests.post(config["url"] + "sendMessage",{"chat_id": mensagem["message"]["chat"]["id"], "text": str(msg)})
    config["lock"].release()


while True:
    global x
    x = ""
    while "result" not in x:
        get_men()
    if len(x["result"]) > 0:
        for mensagem in x["result"]:
            Thread(target=del_up, args=(mensagem, )).start()
            print(json.dumps(mensagem, indent=1))

    if "text" in mensagem["message"]:

        if "/PESQUISAR" in mensagem["message"]["text"].upper():
            
            print("pesquisar")
            from googlesearch import search
            Thread(target=enviar_mensagem, args=(mensagem,  "Os 10 primeiros resultados de sua pesquisa: ")).start()
            for resultado in search(mensagem["message"]["text"][10:], lang="pt", stop=10):
                Thread(target=enviar_mensagem, args=(mensagem, resultado)).start()
        elif "/CALCULAR" in mensagem["message"]["text"].upper():
            
            try:
                calculo = mensagem["message"]["text"][10:]
                Thread(target=enviar_mensagem, args=(mensagem, eval(calculo))).start()
            except Exception as e:
                if "NameError" in str(e):
                    resposta = "EXPRESSÃO INVALIDA!!!\nPor favor, ultilize apenas:\n(+) para adicão\n(-) para subtracão\n(*) para multiplicacão\n(/) para divisão\n(**) para potencia\nE sem espaços"
                    Thread(target=enviar_mensagem, args=(mensagem, resposta)).start()
                else:
                    Thread(target=enviar_mensagem, args=( mensagem, "Ocorreu um erro, tente novamente")).start()

        elif "/PREVISAO" in mensagem["message"]["text"].upper() or "/PREVISÃO" in mensagem["message"]["text"].upper():
            print("prev")
            API_PREV = "178c2ee0d961d191ffbede6bbac3d7ec"

            cidade = mensagem["message"]["text"][9:]
            link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_PREV}&lang=pt_br"

            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()
            print(requisicao_dic)
            if requisicao_dic["cod"] == 200:
                descricao = requisicao_dic['weather'][0]['description']
                temperatura = requisicao_dic['main']['temp'] - 273.15
                temperatura_min = requisicao_dic['main']['temp_min'] - 273.15
                temperatura_max = requisicao_dic['main']['temp_max'] - 273.15

                resposta = f"O clima em{requisicao_dic['name']}\nClima: {descricao}\nTêmperatura:{temperatura: ,.1f}°C \nMinima:{temperatura_min:,.1f}°C\nMaxima:{temperatura_max:,.1f}°C"
                Thread(target=enviar_mensagem, args=(mensagem, resposta)).start()
            elif requisicao_dic["cod"] == 400:
                Thread(target=enviar_mensagem, args=(mensagem, "Cidade não encontrada!!!")).start()

        elif "/ENCURTAR" in mensagem["message"]["text"].upper():
            import pyshorteners
            url = mensagem["message"]["text"][10:]

            s = pyshorteners.Shortener()

            shortUrl = s.tinyurl.short(url)
            Thread(target=enviar_mensagem, args=(mensagem, shortUrl)).start()

        elif "/HORARIO" in mensagem["message"]["text"].upper() or "/HORÁRIO" in mensagem["message"]["text"].upper():
            print("horario")
            from datetime import datetime, timedelta
            import pytz
            UTC = pytz.utc
            hoje = datetime.now(UTC)

            API_PREV = "178c2ee0d961d191ffbede6bbac3d7ec"
            cidade = mensagem["message"]["text"][8:]
            link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_PREV}&lang=pt_br"

            requisicao = requests.get(link)
            requisicao_dic = requisicao.json()
            if requisicao_dic["cod"] == 200:
                zone = requisicao_dic["timezone"]
                zona = int(zone)/60/60
                resposta_parc = hoje + timedelta(hours=int(zona))

                resposta = datetime.strftime(
                    resposta_parc, "Data: %d/%m/%Y \nHorário: %H:%M")
                Thread(target=enviar_mensagem, args=(mensagem, resposta)).start()
            elif requisicao_dic["cod"] == 400:
                Thread(target=enviar_mensagem, args=(mensagem, "Cidade não encontrada!!!")).start()

        elif "/CARAOUCOROA" in mensagem["message"]["text"].upper():
            print("cara ou coroa")
            from random import randint
            r = randint(1, 2)
            print(r)
            if r == 1:
                Thread(target=enviar_mensagem, args=(mensagem, "Deu CARA")).start()
            else:
                Thread(target=enviar_mensagem, args=(mensagem, "Deu COROA")).start()
        elif "/ALEATORIO" in mensagem["message"]["text"].upper() or "/ALEATÓRIO" in mensagem["message"]["text"].upper():
            n = mensagem["message"]["text"][10:]
            if n.isnumeric:
                from random import randint
                r = randint(0, int(n))
                print(r)
                Thread(target=enviar_mensagem, args=(mensagem, f"Seu numero: {r}")).start()
            else:
                Thread(target=enviar_mensagem, args=(mensagem, """Erro, envie apenas"/ALEATORIO número" ex: "/ALEATORIO 7" """)).start()
        else:
            print("nada")
            texto = """
ESSE É O PKM ULTILIDES
TEMOS AS SEGUINTES FUNCÕES:
"/PESQUISAR sua pesquisa" - Realiza uma pesquisa no google.
"/CALCULAR sua expressão matemática" - Resolve equações.
"/PREVISÃO cidade" - Mostra descrição do tempo e temperatura da cidade.
"/ENCURTAR seu link" - Encurta link fornecido.
"/HORARIO cidade" - Mostra a data e o horário na cidade correspondente.
"/CARAOUCOROA" - Cara ou coroa.
"/ALEATORIO número" - Lhe da um número entre 0 e o número que vc mandou.
"""
            Thread(target=enviar_mensagem, args=(mensagem, texto)).start()
    else:
        print("arquivo")
        Thread(target=enviar_mensagem, args=(
            mensagem, "No momento só estamos trabalhando com texto.")).start()
    sleep(2)
