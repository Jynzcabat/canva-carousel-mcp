from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from tools.canva_carousel.tool import generate_carousel

app = FastAPI()

class Slide(BaseModel):
    title: str
    text: str

class SlidesRequest(BaseModel):
    slides: List[Slide]

@app.get("/")
def root():
    return {"message": "GPT Carousel API is running."}

@app.post("/generate")
async def run_generate_carousel(data: SlidesRequest):
    slides = [{"title": s.title, "text": s.text} for s in data.slides]
    return generate_carousel(slides)
