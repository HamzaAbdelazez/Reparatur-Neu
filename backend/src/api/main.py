import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Reparatur API")


@app.get("/")
async def health():
    """
    Simple health check endpoint.

    Returns:
        A message confirming the API is running.
    """
    return {"message": "Reparatur API is up and running!"}


if __name__ == "__main__":
    # Start the server with live reload for development
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
