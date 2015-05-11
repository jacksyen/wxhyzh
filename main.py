from flask import Flask
from flask import request
from flask import render_template
import Util
import msgHandler
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def requestReceiver():
    if request.method == 'GET':
        if request.args.get('echostr', None) is not None:
            return request.args.get('echostr')
    else:
        msg = str(request.data, encoding='utf8')
        print(msg)
        result = msgHandler.dispatchMsg(msg)
        if request is not None:
            return result
        else:
            return ''

@app.route('/bindEmail', methods=['POST', 'GET'])
def bindEmail():
    if request.method == 'GET':
        openid = request.args.get('openid', None)
        if openid is not None:
            return render_template('responsive-full-background-image-demo.html', openid=openid)
    elif request.method == 'POST':
        openid = request.form.get('openid', None)
        email = request.form.get('email', None)
        print(email, openid)
        Util.bindUserEmail(openid, email)
        return render_template('resulthtml.html', text='绑定成功')

if __name__ == '__main__':
    app.run(debug=True)
