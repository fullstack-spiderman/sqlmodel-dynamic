import time
import fastapi
import uvicorn

app = fastapi.FastAPI()


@app.get('/dev')
async def dev():
    time.sleep(1)
    return {
        'env': 'dev',
        'user': 'postgres',
        'pass': 'postgres',
        'host': 'localhost',
        'port': 5432,
        'db': 'webdev'
    }


@app.get('/prod')
async def prod():
    time.sleep(2)
    return {
        'env': 'prod',
        'user': 'produser',
        'pass': 'prodpass',
        'host': 'prodhost',
        'port': 5432,
        'db': 'webprod'
    }


if __name__ == '__main__':
    uvicorn.run(app, debug=True, port=8000)
