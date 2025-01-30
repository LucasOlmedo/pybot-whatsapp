from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import datetime, requests

app = Flask(__name__)

user_states = {}

def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()

        return f"{data['city']} - {data['regionName']} - {data['country']}"

    except Exception:
        return "Localização não disponível"

@app.route("/webhook", methods=["POST"])
def webhook():

    global user_states

    msg = request.values.get("Body")
    sender = request.values.get("From")

    response = MessagingResponse()

    if sender not in user_states:
        user_states[sender] = "waiting_option"

        response.message(
            "Olá, digite as opções:\n\n"
            "[1] - Data Atual\n"
            "[2] - Local Atual\n"
            "[3] - Sair\n"
        )

    elif user_states[sender] == "waiting_option":

        if msg == "1":
            now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")
            response.message(f"📅 Data e hora atual: {now}")

        elif msg == "2":
            location = get_location()
            response.message(f"📍 Sua localização: {location}")
        
        elif msg == "3":
            response.message("👋 Volte sempre!")
            del user_states[sender]

        else:
            response.message(
                "⚠️ Opção inválida! Escolha uma das opções abaixo:\n\n"
                "[1] - Data Atual\n"
                "[2] - Local Atual\n"
                "[3] - Sair\n"
            )

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
