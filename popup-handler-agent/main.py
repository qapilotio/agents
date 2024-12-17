from utils import encode_image, extract_popup_details
from llm import initialize_llm
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from prompts import image_prompt, xml_prompt
from typing import Optional

from dotenv import load_dotenv
import os
import json  


load_dotenv()

app = FastAPI()

class APIRequest(BaseModel):
    image: Optional[str] = None
    testcase_dec: str
    xml: Optional[str] = None

@app.post("/invoke")
async def run_service(request: APIRequest):
    try:
        llm_key = os.getenv("OPENAI_API_KEY")
        if not llm_key:
            raise HTTPException(status_code=500, detail="API key not found. Please check your environment variables.")
        llm = initialize_llm(llm_key)

        if request.image and request.xml:
            raise HTTPException(status_code=422, detail="Both image and xml were provided. Please provide only one.")

        if request.image:
            encoded_image = encode_image(request.image)
            messages = [
                (
                    "system",
                    image_prompt,
                ),
                ("human", f"test-case description: {request.testcase_dec}"),
                ("human", [
                    {"type": "text", "text": "this is the screenshot of the current screen"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
                    },
                ]),
            ]
        if request.xml:
            processed_xml = extract_popup_details(request.xml)
            messages = [
                (
                    "system",
                    xml_prompt,
                ),
                ("human", f"test-case description: {request.testcase_dec}"),
                ("human", f'this is the output from the pop-detector: {processed_xml}')
            ]
        else:
            raise HTTPException(status_code=400, detail="Either image or xml must be provided.")

        ai_msg = llm.invoke(messages)
        output = ai_msg.content
        print("AI Message Content:", ai_msg.content)

        # Remove any extraneous formatting like triple backticks if present
        cleaned_content = ai_msg.content.strip("```json\n").strip("\n```")

        # Attempt to parse the JSON output from the AI message
        try:
            parsed_output = json.loads(cleaned_content)
        except json.JSONDecodeError:
            # If parsing fails, return the raw content with an error message
            raise HTTPException(status_code=500, detail=f"Failed to parse AI message content as JSON. Content: {ai_msg.content}")
        
        resource_id = parsed_output.get("element_metadata", {}).get("resource_id")

        print("Resource ID:", resource_id)
        # Return the parsed output in the API response
        return {
            "status": "success",
            "Agent-response": parsed_output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
