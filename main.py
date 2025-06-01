from fastapi import FastAPI
from tools.canva_carousel.tool import generate_carousel

app = FastAPI()

@app.post("/generate")
async def run_generate_carousel(slides: list):
    return generate_carousel(slides)
