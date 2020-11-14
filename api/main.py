from fastapi import FastAPI

from .routers import truss

fea_app = FastAPI()


@fea_app.get('/')
def app_root():
    return 'fea-app api'


fea_app.include_router(
    truss.router,
    prefix='/truss',
)
