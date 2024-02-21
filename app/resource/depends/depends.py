from injector import Injector, inject
from app.db.db import AppConfig, TestAppConfig

di = Injector([AppConfig()])

async def update_injector(_class):
    global di
    di = Injector([_class])

@inject
def get_di_class(_class):
    return di.get(_class)