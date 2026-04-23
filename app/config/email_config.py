from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="83f010f46d20be",
    MAIL_PASSWORD="483fb9cc5df41b",
    MAIL_FROM="sistema@academico.com",
    MAIL_PORT=587,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def enviar_correo(destinatario: str, asunto: str, cuerpo: str):
    message = MessageSchema(
        subject=asunto,
        recipients=[destinatario],
        body=cuerpo,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)