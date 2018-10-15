from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db


@route_api.route('/member/login', methods=['POST', 'GET'])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    code = req['code'] if 'code' in req else ''
    if not code or len(code)<1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)
    return jsonify(resp)
