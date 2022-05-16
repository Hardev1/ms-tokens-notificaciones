from flask import Flask

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
from flask import request
from environment import *
from jose import jwt
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/enviar-texto")
def enviarSms():
    print(os.environ.get("SECURITY_HASH"))
    hashString = request.args.get("hash")
    if hashString == os.environ.get("SECURITY_HASH"):
        destino = request.args.get("destino")
        mensaje = request.args.get("mensaje")
        try:
            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=mensaje,
                from_="+12677192895",
                to="+57" + destino
            )

            print(message.sid)
            print("Mensaje enviado")
            return "OK"

        except Exception as e:
            print(e.message)
            return "KO"
    else:
        print("Sin hash")
        return "Hash error"


@app.route("/correo")
def enviarCorreo():
    hashString = request.args.get("hash")
    if hashString == os.environ.get("SECURITY_HASH"):
        destino = request.args.get("destino")
        asunto = request.args.get("asunto")
        mensaje = request.args.get("mensaje")
        message = Mail(

            from_email=os.environ.get("email_from"),
            to_emails=destino,
            subject=asunto,
            html_content=mensaje)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print("Enviado")
            return "OK"
        except Exception as e:
            print(e.message)
            return "KO"
    else:
        print("Sin hash")
        return "Hash error"

@app.route("/crear-token")
def crear():
    nombre = request.args.get("nombre")
    id_persona = request.args.get("id")
    id_rol = request.args.get("id_rol")
    print(nombre + id_persona + "--" + id_rol)
    try:
        secret_key = os.environ.get("JWT_SECRET_KEY")
        token = jwt.encode({'nombre': nombre, 'id': id_persona, 'rol': id_rol}, secret_key, algorithm='HS256')
        print(secret_key + "--" + token)
        return token
    except Exception as e:
        return "efe"

@app.route("/validar-token")
def validar():
    token = request.args.get("token")
    rol = request.args.get("rol")
    try:
        secret_key = os.environ.get("JWT_SECRET_KEY")
        token = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(token + '__' + rol)
        if token["rol"] == rol:
            print('ok')
            return "OK"
        else:
            print('ko')
            return "KO"
    except Exception as e:
        print('bad')
        return ""

@app.route("/verificar-token")
def verificar():
    token = request.args.get("token")
    try:
        secret_key = os.environ.get("JWT_SECRET_KEY")
        token = jwt.decode(token, secret_key, algorithms=['HS256'])
        print(token)
        return "OK"
    except Exception as e:
        return "KO"

if __name__ == "__main__":
    app.run()