import mailtrap as mt
def sendem():
    mail = mt.Mail(
    sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
    to=[mt.Address(email="hackerrr2512@gmail.com")],
    subject="Client booking",
    text="Join the Link for the client",
    category="Integration Test",
    )

    client = mt.MailtrapClient(token="ed44d90cd2375f1efdafd89deec213e1")
    client.send(mail)