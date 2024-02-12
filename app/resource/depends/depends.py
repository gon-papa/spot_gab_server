from injector import Injector, inject

injection = Injector()

@inject
def get_di_class(_class):
    return injection.get(_class)