from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
async def health_point():
    return "Server is running and endpoints are ok"


@app.get("/data")
async def data(item: str):

    return item
