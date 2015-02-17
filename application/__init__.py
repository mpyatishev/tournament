from flask import Flask

app = Flask(__name__)
app.debug = True
# app.threaded = True

from application import urls
