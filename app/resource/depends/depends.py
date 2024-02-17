from injector import Injector, inject
from app.db.db import AppConfig

injection = Injector([AppConfig()])

@inject
def get_di_class(_class):
    return injection.get(_class)