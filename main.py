from flask import Flask
from flask import request
from flask import Response
from flask import render_template
import Util
import msgHandler
import json
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


@app.route('/search', methods=['GET', 'POST'])
def downloadBook():
    if request.method == 'GET':
        openid = request.args.get('openid', None)
        if openid is not None:
            if Util.isUserEmailBinded(openid):
                return render_template('search_book.html', openid=openid)

    elif request.method == 'POST':
        openid = request.form.get('openid', None)
        book = request.form.get('book', None)
        if openid is not None and book is not None:
            bookInfos = Util.searchBook(book)
            result = {'booknum': len(bookInfos)}
            if len(bookInfos) > 0:
                bookList = []
                for x in bookInfos:
                    if x.toDict() is not None:
                        bookList.append(x.toDict())
                result['books'] = bookList
            return Response(json.dumps(result, ensure_ascii=False),  mimetype='application/json')
        else:
            return 'false'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
