from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests, json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import Memberservice


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

    openid = Memberservice.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = 'weixin api is wrong'
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
    判断是否已经注册过，注册了直接返回
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = Memberservice.geneSalet()
        model_member.created_time = model_member.created_time = getCurrentDate()

        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.created_time = model_bind.updated_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = '%s#%s' % (Memberservice.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)


@route_api.route('/member/check-reg', methods=['POST', 'GET'])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        return jsonify(resp)

    openid = Memberservice.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = 'weixin api is wrong'
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = '未关联'
        return jsonify(resp)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = '未查询到绑定信息'
        return jsonify(resp)
    token = '%s#%s'%(Memberservice.geneAuthCode(member_info),member_info.id)
    resp['data'] = {'token':token}
    return jsonify(resp)
