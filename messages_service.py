from fastapi import FastAPI

app = FastAPI()


@app.get("/lab2")
def root():
    return "not implemented yet"
