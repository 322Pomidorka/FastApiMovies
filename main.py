from httpxrr.singleOnHttpx import on_start_up, on_shutdown
from fastapi import FastAPI
from users.router import router as router_users
from movies.router import router as router_movies

app = FastAPI(docs_url="/", on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.include_router(router_users)
app.include_router(router_movies)


