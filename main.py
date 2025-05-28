from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from app.views import client_view, service_view, order_view, pay_view
from app.config.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(title="DobleAAMotors API", version="0.1.0", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Hello World"}


api_router = APIRouter(prefix="/api")

api_router.include_router(
    client_view.client_router, prefix="/clients", tags=["Clients"]
)
api_router.include_router(
    service_view.service_router, prefix="/services", tags=["Services"]
)
api_router.include_router(order_view.order_router, prefix="/orders", tags=["Orders"])
api_router.include_router(pay_view.pay_router, prefix="/pays", tags=["Pays"])

app.include_router(api_router)
