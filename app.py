# Gemini API backend

# import os
# import base64
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv

# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# client = genai.Client()

# class ChatRequest(BaseModel):
#     image_data: str
#     question: str

# @app.post("/api/chat")
# async def chat_with_page(request: ChatRequest):
#     if not os.getenv("GEMINI_API_KEY"):
#         raise HTTPException(status_code=500, detail="Gemini API Key not configured.")
    
#     try:
#         raw_bytes = base64.b64decode(request.image_data)
                
#         image_part = types.Part.from_bytes(
#             data=raw_bytes,
#             mime_type="image/jpeg"
#         )
        
#         response = client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=[image_part, request.question],
#             config=types.GenerateContentConfig(
#                 system_instruction=(
#                     "You are a strict visual assistant. Look ONLY at the provided image, which is a literal "
#                     "screenshot of what the user currently sees on their monitor. Answer their question "
#                     "using exclusively what is visually readable or present in this image. Do not use outside "
#                     "knowledge or extrapolate things outside the frame. If the answer is not visible on the screen "
#                     "right now, reply exactly with: 'I am sorry, but that information is not visible on your screen right now.'"
#                 )
#             ),
#         )
        
#         return {"answer": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# class SuggestionRequest(BaseModel):
#     image_data: str
#     chat_history: list = []  # Receives past user/ai dialogue arrays

# @app.post("/api/suggest-questions")
# async def suggest_questions(request: SuggestionRequest):
#     if not os.getenv("GEMINI_API_KEY"):
#         raise HTTPException(status_code=500, detail="Gemini API Key not configured.")
        
#     try:
#         raw_bytes = base64.b64decode(request.image_data)
#         image_part = types.Part.from_bytes(data=raw_bytes, mime_type="image/jpeg")
        
#         history_context = ""
#         if request.chat_history:
#             history_context = "Current conversation history:\n"
#             for msg in request.chat_history:
#                 role = msg.get('role', 'user') if isinstance(msg, dict) else getattr(msg, 'role', 'user')
#                 text = msg.get('text', '') if isinstance(msg, dict) else getattr(msg, 'text', '')
#                 history_context += f"{role.upper()}: {text}\n"

#         prompt = (
#             f"{history_context}\n"
#             "Analyze the screenshot provided. Based strictly on the text and factual data visible "
#             "in the image, generate exactly 3 short, punchy follow-up questions a user might want to ask next.\n\n"
#             "CRITICAL RULES:\n"
#             "1. Each question MUST be under 6-8 words so it fits perfectly on a tiny screen.\n"
#             "2. Questions must be SOLELY about the educational/factual content of the page. "
#             "NEVER ask about UI settings, text size, buttons, color modes, layouts, or appearance configurations.\n"
#             "3. If there is chat history provided above, make the new suggestions logical follow-ups to what was just discussed.\n"
#             "4. Separate each question with a newline. Do not include numbers, dashes, or symbols."
#         )
        
#         response = client.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=[image_part, prompt],
#         )
        
#         questions = []
#         for line in response.text.split('\n'):
#             cleaned = line.strip().lstrip('0123456789.-*• ')
#             if cleaned:
#                 questions.append(cleaned)
                
#         if not questions:
#             questions = ["What is the main topic here?", "Can you explain this screen?", "Summarize the core concept"]
            
#         return {"suggestions": questions[:3]}
        
#     except Exception as e:
#         print(f"ERROR IN SUGGESTIONS: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


#Open AI API backend

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

client = OpenAI()

class ChatRequest(BaseModel):
    image_data: str
    question: str

class SuggestionRequest(BaseModel):
    image_data: str
    chat_history: list = []  

@app.post("/api/chat")
async def chat_with_page(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API Key not configured.")
    
    try:
        image_data_url = f"data:image/jpeg;base64,{request.image_data}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/api/suggest-questions")
async def suggest_questions(request: SuggestionRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OpenAI API Key not configured.")
        
    try:
        image_data_url = f"data:image/jpeg;base64,{request.image_data}"
        history_context = ""
        if request.chat_history:
            history_context = "Current conversation history:\n"
            for msg in request.chat_history:
                role = msg.get('role', 'user') if isinstance(msg, dict) else getattr(msg, 'role', 'user')
                text = msg.get('text', '') if isinstance(msg, dict) else getattr(msg, 'text', '')
                history_context += f"{role.upper()}: {text}\n"

        prompt = (
            f"{history_context}\n"
            "Analyze the screenshot provided. Based strictly on the text and factual data visible "
            "in the image, generate exactly 3 short, punchy follow-up questions a user might want to ask next.\n\n"
            "CRITICAL RULES:\n"
            "1. Each question MUST be under 6-8 words so it fits perfectly on a tiny screen.\n"
            "2. Questions must be SOLELY about the educational/factual content of the page. "
            "NEVER ask about UI settings, text size, buttons, color modes, layouts, or appearance configurations.\n"
            "3. If there is chat history provided above, make the new suggestions logical follow-ups to what was just discussed.\n"
            "4. Separate each question with a newline. Do not include numbers, dashes, or symbols."
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data_url,
                                "detail": "low"  
                            }
                        }
                    ]
                }
            ],
            temperature=0.0
        )
    
        raw_text = response.choices[0].message.content or ""
        
        questions = []
        for line in raw_text.split('\n'):
            cleaned = line.strip().lstrip('0123456789.-*• ')
            if cleaned:
                questions.append(cleaned)
                
        if not questions:
            questions = ["What is the main topic here?", "Can you explain this screen?", "Summarize the core concept"]
            
        return {"suggestions": questions[:3]}
        
    except Exception as e:
        print(f"ERROR IN SUGGESTIONS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)