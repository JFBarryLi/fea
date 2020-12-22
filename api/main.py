from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import truss

fea_app = FastAPI(
    title='fea-app api',
    description='Api for finite element solvers.',
    version='v1'
)

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://192.168.0.102',
    'http://192.168.0.102:3000',
    'https://barryli.ca',
    'https://fea.barryli.ca',
]

fea_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET', 'POST'],
    allow_headers=['*'],
)


@fea_app.get('/')
def app_root():
    return {
        'title': fea_app.title,
        'description': fea_app.description,
        'version': fea_app.version,
        'docs': '/docs',
        'truss': '/truss',
    }


fea_app.include_router(
    truss.router,
    prefix='/truss',
)
