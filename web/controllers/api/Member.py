from web.controllers.api import route_api
from flask import request,jsonify
from application import app,db
@route_api.route('/member/login',methods=['POST','GET'])
def login():
    req = request.values
    app.logger.info(req)
    return