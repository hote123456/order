# -*- coding: utf-8 -*-
SERVER_PORT = 5000
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = 'mooc_food'

IGNORE_URLS = [
    "^/user/login",
    "^/api"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 5
PAGE_DISPLAY = 10

STATUS_MAPPING={
    '1':'正常',
    '0':'已删除'
}

MIYA_APP ={
    'appid':'wxa930885d6225a0e4',
    'appkey':'efb98969bff7e906812f639430496fb6'
}