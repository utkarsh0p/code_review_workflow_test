from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/review")
async def review(request: Request):
    payload = await request.json()
    print("GITHUB PAYLOAD:", payload)

    return {"msg": "received"}

#line just to test the pr workflow (count 1)