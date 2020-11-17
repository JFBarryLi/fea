from fastapi import FastAPI

from .routers import truss

fea_app = FastAPI(
    title='fea-app api',
    description='Api for finite element solvers.',
    version='v1'
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
