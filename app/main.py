from fastapi import FastAPI

from routers import auth, delivery, parcel, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(parcel.router)
app.include_router(delivery.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
