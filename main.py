from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Provider finder is running"}