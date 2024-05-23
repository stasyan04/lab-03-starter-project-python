from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from spaceship.config import Settings
from spaceship.routers import api, health

import numpy as np


def make_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.state.settings = settings

    if settings.debug:
        app.mount('/static', StaticFiles(directory='build'), name='static')

    app.include_router(api.router, prefix='/api', tags=['api'])
    app.include_router(health.router, prefix='/health', tags=['health'])

    @app.get('/', include_in_schema=False, response_class=FileResponse)
    async def root() -> str:
        return 'build/index.html'
    
    @app.get('/numpytest')
    def numpy_test():
        # Генеруємо дві випадкові матриці 10x10
        matrix_a = np.random.rand(10, 10)
        matrix_b = np.random.rand(10, 10)

        # Перемножуємо матриці
        product = np.matmul(matrix_a, matrix_b)

        # Конвертуємо матриці у списки для JSON-серіалізації
        matrix_a_list = matrix_a.tolist()
        matrix_b_list = matrix_b.tolist()
        product_list = product.tolist()

        # Формуємо результат у вигляді словника
        result = {
            "matrix_a": matrix_a_list,
            "matrix_b": matrix_b_list,
            "product": product_list
        }
        return result

    return app
