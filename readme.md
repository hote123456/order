Python Flask订餐系统
=====================
##启动

export ops_config=local && python manager.py runserver

export ops_config=production && python manager.py runserver

##flask-sqlacodegen
#
    flask-sqlacodegen 'mysql://root:Aa123456!@127.0.0.1/food_db' --outfile "common/models/model.py"  --flask
    flask-sqlacodegen 'mysql://root:Aa123456!@127.0.0.1/food_db' --tables user --outfile "common/models/user.py"  --flask

username = magic
password = 123456


