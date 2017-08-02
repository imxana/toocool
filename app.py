from flask import Flask
from flask_cors import CORS
from apps import models, test, qiniu, flaskr, transfer, eazy_login

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config.DevelopmentConfig')


models.register(app)
test.register(app)


# your own module
eazy_login.register(app)
# flaskr.register(app)
qiniu.register(app)
transfer.register_front(app)
transfer.register_calculate(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
