from web.controllers.api import route_api
from flask import request, jsonify
from application import app, db
import requests, json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate


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

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
        app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
    app.logger.info(url)
    r = requests.get(url)
    res = json.loads(r.text)
    app.logger.info(url)
    openid = res['openid']

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
    判断是否已经注册过，注册了直接返回
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if bind_info:
        member_info = Member.query.filter_by(id=bind_info.member_id).first()
        resp['msg'] = '已经绑定'
        resp['data'] = {'nickname': member_info.nickname}
        return jsonify(resp)

    model_member = Member()
    model_member.nickname = nickname
    model_member.sex = sex
    model_member.avatar = avatar
    model_member.salt = ''
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

    resp['data'] = {'nickname': nickname}
    return jsonify(resp)
