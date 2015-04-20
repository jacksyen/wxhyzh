from flask import Flask
from flask import request
import msgHandler
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def requestReceiver():
    if request.method == 'GET':
        if request.args.get('echostr', None) is not None:
            return request.args.get('echostr')
    else:
        msgHandler.dispatchMsg(request.data)


if __name__ == '__main__':
    app.run(debug=True)
