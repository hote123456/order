# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, jsonify, make_response, redirect, g

from application import app, db
from common.libs.Helper import ops_render
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import Userservice
from common.models.user import User

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return ops_render("user/login.html")

    resp = {'code': 200, 'msg': 'success', 'data': {}}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = 'username false'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = 'pwd false'
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = 'no user'
        return jsonify(resp)

    if user_info.login_pwd != Userservice.genePwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = 'no user'
        return jsonify(resp)

    response = make_response(json.dumps({'code': 200, 'msg': '登录成功'}))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (Userservice.geneAuthCode(user_info),user_info.uid),60*60*24*120)##120天不过其
    return response


@route_user.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'GET':
        return ops_render("user/edit.html",{'current':'edit'})

    resq = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resq['code'] = -1
        resq['msg'] = '请输入用户名'
        return jsonify(resq)

    if email is None or len(email) < 1:
        resq['code'] = -1
        resq['msg'] = '请输入邮箱'
        return jsonify(resq)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resq)


@route_user.route("/reset-pwd", methods=['POST', 'GET'])
def resetPwd():
    if request.method == 'GET':
        return ops_render("user/reset_pwd.html",{'current':'reset-pwd'})

    resq = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resq['code'] = -1
        resq['msg'] = '请输入密码'
        return jsonify(resq)

    if new_password is None or len(new_password) < 6:
        resq['code'] = -1
        resq['msg'] = '请输入密码'
        return jsonify(resq)

    if old_password == new_password:
        resq['code'] = -1
        resq['msg'] = '密码需要2次不一样'
        return jsonify(resq)

    user_info = g.current_user
    user_info.login_pwd = Userservice.genePwd(new_password,user_info.login_salt)

    db.session.add(user_info)
    db.session.commit()

    response = make_response(json.dumps(resq))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (Userservice.geneAuthCode(user_info), user_info.uid),
                        60 * 60 * 24 * 120)  ##120天不过其
    return response

@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
