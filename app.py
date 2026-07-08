import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from google import genai
# from google.genai import types
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# client = genai.Client()
client = OpenAI()

class ChatRequest(BaseModel):
    image_data: str
    question: str

@app.post("/api/chat")
async def chat_with_page(request: ChatRequest):
    # if not os.getenv("GEMINI_API_KEY"):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API Key not configured.")
    
    try:
        # Decode the incoming base64 image data from Chrome
        # raw_bytes = base64.b64decode(request.image_data)
        image_data_url = f"data:image/jpeg;base64,{request.image_data}"
                
        # image_part = types.Part.from_bytes(
        #     data=raw_bytes,
        #     mime_type="image/jpeg"
        # )
        
    #     response = client.models.generate_content(
    #         model='gemini-2.5-flash',
    #         # Pass both the screen snapshot and the user's question
    #         contents=[image_part, request.question],
    #         config=types.GenerateContentConfig(
    #             system_instruction=(
    #                 "You are a strict visual assistant. Look ONLY at the provided image, which is a literal "
    #                 "screenshot of what the user currently sees on their monitor. Answer their question "
    #                 "using exclusively what is visually readable or present in this image. Do not use outside "
    #                 "knowledge or extrapolate things outside the frame. If the answer is not visible on the screen "
    #                 "right now, reply exactly with: 'I am sorry, but that information is not visible on your screen right now.'"
    #             )
    #         ),
    #     )
        
        
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Fast, affordable, and natively supports vision layout inputs
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict visual assistant. Look ONLY at the provided image, which is a literal "
                        "screenshot of what the user currently sees on their monitor. Answer their question "
                        "using exclusively what is visually readable or present in this image. Do not use outside "
                        "knowledge or extrapolate things outside the frame. If the answer is not visible on the screen "
                        "right now, reply exactly with: 'I am sorry, but that information is not visible on your screen right now.'"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": request.question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url,
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0 
        )
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
