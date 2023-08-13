import uvicorn
from fastapi import Request, Response

from src.api.app import app
from src.db.core import session


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = session
        response = await call_next(request)
    finally:
        await request.state.db.close()
    return response


if __name__ == '__main__':
    uvicorn.run(app=app)
