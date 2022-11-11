# importing libraries
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)  # instantiate the mail class
mail.init_app(app)
# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ssashokkumar@student.tce.edu'
app.config['MAIL_PASSWORD'] = 'Summa@ITOM'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# @app.route('/send-mail')
def index():
    msg = Message(
        'Hello',
        sender='ssashokkumar2000@gmail.com',
        recipients=['ssashokkumar2000@gmail.com']
    )
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg)
    return 'Sent'


if __name__ == '__mail__':
    app.run()
