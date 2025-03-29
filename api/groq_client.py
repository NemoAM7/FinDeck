import os
import groq
import base64
import json
import time
import asyncio
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

class GroqClient:
    def __init__(self, model_name: str = "llama-3.2-90b-vision-preview"):
        """Initialize Groq client with API key and model."""
        self.model_name = model_name
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.client = groq.Client(api_key=api_key)
        self.conversation_history: List[Dict[str, Any]] = []
            
    async def process_image_bytes(self, image_bytes: bytes) -> str:
        """Process an image using Groq's vision model to extract tables into CSV format."""
        try:
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            message_content = [
                {
                    "type": "text",
                    "text": "Extract the table from this image and convert it to CSV format. Only provide the raw CSV data without any explanations, markdown formatting, or code blocks."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
            
            messages = [
                {
                    "role": "user",
                    "content": message_content
                }
            ]
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0,
                max_tokens=4000
            )
            
            csv_content = response.choices[0].message.content
            
            if "```" in csv_content:
                csv_parts = csv_content.split("```")
                for part in csv_parts:
                    if "csv" not in part and "," in part and "\n" in part:
                        csv_content = part.strip()
                        break
            
            if not csv_content or "," not in csv_content:
                return "Error: Could not extract CSV data from the image"
                
            return csv_content
            
        except Exception as e:
            print(f"Error processing image with Groq API: {str(e)}")
            return f"Error: {str(e)}" 
            
    async def process_text_prompt(self, prompt: str, model_name: str = None) -> dict:
        """Process a text prompt using Groq's LLM."""
        try:
            start_time = time.time()
            
            model = model_name if model_name else self.model_name
            
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            
            processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
            
            return {
                "response": response.choices[0].message.content,
                "model_used": model,
                "processing_time": processing_time
            }
            
        except Exception as e:
            print(f"Error processing text prompt with Groq API: {str(e)}")
            return {
                "response": f"Error: {str(e)}",
                "model_used": model_name if model_name else self.model_name,
                "processing_time": 0
            }
            
    async def process_multimodal_prompt(self, text_prompt: str, image_bytes: bytes, model_name: str = None) -> dict:
        """Process a text prompt with an image using Groq's vision model."""
        try:
            start_time = time.time()
            
            model = model_name if model_name else self.model_name
            if "vision" not in model:
                raise ValueError("The specified model does not support vision capabilities")
            
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            message_content = [
                {
                    "type": "text",
                    "text": text_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
            
            messages = [
                {
                    "role": "user",
                    "content": message_content
                }
            ]
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            
            processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
            
            return {
                "response": response.choices[0].message.content,
                "model_used": model,
                "processing_time": processing_time
            }
            
        except Exception as e:
            print(f"Error processing multimodal prompt with Groq API: {str(e)}")
            return {
                "response": f"Error: {str(e)}",
                "model_used": model_name if model_name else self.model_name,
                "processing_time": 0
            }
    
    def add_to_conversation(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
        
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        return self.conversation_history
        
    def reset_conversation(self) -> None:
        """Reset the conversation history"""
        self.conversation_history = []

if __name__ == "__main__":
    async def main():
        client = GroqClient()
        
        # Example text prompt
        result = await client.process_text_prompt("What is the capital of France?")
        print(f"Response: {result['response']}")
        
    asyncio.run(main()) 