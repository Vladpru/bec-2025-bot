from . import start
from . import registration, about_bec, main_menu

def setup_routers(dp):
    dp.include_routers(
        start.router,
        registration.router,
        about_bec.router,
        main_menu.router,
    )