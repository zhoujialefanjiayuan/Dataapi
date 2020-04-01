from datetime import datetime, date

from sqlalchemy import UniqueConstraint

from app.ext import db


class Base():
    created_at = db.Column(db.DATETIME,default=datetime.now)

    def add_db_data(self):
        with db.auto_commit_db():
            db.session.add(self)



# 角色模型类(一方)
#1-哈杜  2-advance  3-izidata
class Api_order(db.Model,Base):
    __tablename__ = "api_order"
    id  = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(200))
    order = db.Column(db.String(200),default='')



class Black_list(db.Model,Base):
    __tablename__ = "black_list"
    # db.Colomn()表示模型类的属性,
    # 主键
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    nik = db.Column(db.String(50))
    mobile_no = db.Column(db.String(50))
    name = db.Column(db.String(100))
    hitReason = db.Column(db.String(100),default='OVERDUE_DAYS_BETWEEN_60_TO_90',comment='OVERDUE_DAYS_BETWEEN_60_TO_90 or OVERDUE_DAYS_MORE_THAN_90')
    channel = db.Column(db.String(10))
    eventtime = db.Column(db.String(10))
    response = db.Column(db.String(500))

#身份证多头查询
class NikMultiPlatform(db.Model,Base):
    __tablename__ = "nik_multiplatform"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nik = db.Column(db.String(50))
    user = db.Column(db.String(50))
    day = db.Column(db.Date,default=date.today())
    channel = db.Column(db.String(10))
    UniqueConstraint(nik,user,day)

#手机号多头查询
class MobileMultiPlatform(db.Model,Base):
    __tablename__ = "mobile_multiplatform"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mobile_no = db.Column(db.String(50))
    user = db.Column(db.String(50))
    day = db.Column(db.Date, default=date.today())
    channel = db.Column(db.String(10))
    UniqueConstraint(mobile_no, user, day)


#身份证检查
class NIkCheck(db.Model,Base):
    __tablename__ = "nik_check"
    nik = db.Column(db.String(20),primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(20),default='')
    address = db.Column(db.String(250),default='')
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    village = db.Column(db.String(50))
    work = db.Column(db.String(50),default='')
    religion = db.Column(db.String(50),default='')
    date_of_birth = db.Column(db.String(50),default='')
    marital_status = db.Column(db.String(50),default='')
    channel = db.Column(db.String(10))

#手机号再网时长
class MobileOnline(db.Model,Base):
    __tablename__ = "mobile_online"
    mobile_no = db.Column(db.String(50),primary_key=True)
    online =  db.Column(db.Integer)

#身份证手机号检查
class NikMobileCheck(db.Model,Base):
    __tablename__ = "nik_mobile_check"
    nik = db.Column(db.String(20),primary_key=True)
    mobile_no = db.Column(db.String(50))

#手机号是否认证
class MobileAuth(db.Model,Base):
    __tablename__ = "mobile_auth"
    mobile_no = db.Column(db.String(50),primary_key=True)
    isauth = db.Column(db.Boolean,default=True)

#手机号充值行为
class MobileRecharge(db.Model,Base):
    __tablename__ = "mobile_recharge"
    mobile_no = db.Column(db.String(50),primary_key=True)
    topup_0_30 = db.Column(db.String(20))
    topup_0_60 = db.Column(db.String(20))
    topup_0_90 = db.Column(db.String(20))
    topup_0_180 = db.Column(db.String(20))
    topup_0_360 = db.Column(db.String(20))
    topup_30_60 = db.Column(db.String(20))
    topup_60_90 = db.Column(db.String(20))
    topup_90_180 = db.Column(db.String(20))
    topup_180_360 = db.Column(db.String(20))
    topup_360_720 = db.Column(db.String(20))

class User(db.Model,Base):
    __tablename__ = "user"
    accesskey = db.Column(db.String(30), primary_key=True)
    secretkey = db.Column(db.String(30),unique=True)
    username = db.Column(db.String(20),unique=True)
    password = db.Column(db.String(20))
    balance= db.Column(db.DECIMAL(11,3))
    extend_balance= db.Column(db.DECIMAL(6,2))
    email= db.Column(db.String(25))
    phone= db.Column(db.String(25))

class Api_log(object):
    _mapper = {}
    #Api_log.model(useraccesskey,username) 创建实例
    @staticmethod
    def model(username,useraccesskey):
        class_name = '%s_%s' % (username,useraccesskey)
        ModelClass = Api_log._mapper.get(class_name, None)
        if ModelClass is None:
            ModelClass = type(class_name, (db.Model,Base), {
                '__module__': __name__,
                '__name__': class_name,
                '__tablename__': '%s_%s' % (username,useraccesskey),
                '__bind_key__' : 'users_logs',
                'id' : db.Column(db.Integer,autoincrement=True,primary_key=True),
                'created_at': db.Column(db.DATETIME,default=datetime.now),
                'apiname':db.Column(db.String(20)),
                'response_code':db.Column(db.Integer,default=200),
                'paied':db.Column(db.DECIMAL(5,3),default=0),#支付金额
                'nik':db.Column(db.String(50),default=''),#提交参数nik
                'mobile_no': db.Column(db.String(50),default=''),#提交参数mobile_no
                'params':db.Column(db.String(500),default=''),
                'applytime':db.Column(db.String(20)),
                'iscal_paied':db.Column(db.Boolean,default=0)
            })
            Api_log._mapper[class_name] = ModelClass
        cls = ModelClass()
        return cls
    @classmethod
    def getcls(cls,modelname):
        return cls._mapper.get(modelname)
