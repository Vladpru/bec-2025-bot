from . import start, registration

def setup_routers(dp):
    dp.include_routers(
        start.router,
        registration.router
    )