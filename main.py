from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    return {"key": "Test"}


@app.get("/{pk}")
def get_item(pk: int, message: str = None):
    return {"pk": pk, "message": message}
