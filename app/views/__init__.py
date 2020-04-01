from app.views.blacklist import black_blue
from app.views.isshopee import isshopee_blue
from app.views.istokopedia import istokopedia_blue
from app.views.mobile_multi_platform import mobile_mul_blue
from app.views.mobile_online import mobile_online_blue
from app.views.mobile_recharge import mobilerecharge_blue
from app.views.mobileauthentication import mobileauthentication_blue
from app.views.nik_check import nik_check_blue
from app.views.nik_mobile_check import nik_mobile_check_blue
from app.views.nik_multi_platform import nik_mul_blue


def init_blue(app):
    app.register_blueprint(blueprint = black_blue)
    app.register_blueprint(blueprint = nik_mul_blue)
    app.register_blueprint(blueprint = mobile_mul_blue)
    app.register_blueprint(blueprint = nik_check_blue)
    app.register_blueprint(blueprint = mobile_online_blue)
    app.register_blueprint(blueprint = nik_mobile_check_blue)
    app.register_blueprint(blueprint = mobileauthentication_blue)
    app.register_blueprint(blueprint = isshopee_blue)
    app.register_blueprint(blueprint = istokopedia_blue)
    app.register_blueprint(blueprint = mobilerecharge_blue)
