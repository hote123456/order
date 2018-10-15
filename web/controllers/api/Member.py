from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests


@route_api.route('/member/login', methods=['POST', 'GET'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code=JSCODE&grant_type=authorization_code'.format(
        app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'])
    app.logger.info(url)
    r = requests.get(url)
    res = r.text
    app.logger.info(res)
    return jsonify(resp)
