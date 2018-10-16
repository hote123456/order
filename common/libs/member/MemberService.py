# encoding : utf-8
# @Time    : 10/15/18 11:17 PM
# @Author  : magic
# @Email   : 
# @File    : MemberService.py
# @Software: PyCharm
import hashlib, random, string, requests, json
from application import app


class Memberservice():

    @staticmethod
    def geneAuthCode(member_info):
        m = hashlib.md5()
        str = '%s-%s-%s' % (member_info.id, member_info.salt, member_info.status)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    @staticmethod
    def geneSalet(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return (''.join(keylist))

    @staticmethod
    def getWeChatOpenId(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
            app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        app.logger.info(url)
        r = requests.get(url)
        res = json.loads(r.text)
        app.logger.info(url)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid
