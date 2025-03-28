import os
import groq
import base64
import json
from dotenv import load_dotenv

class GroqClient:
    def __init__(self, model_name: str = "llama-3.2-90b-vision-preview"):
        """Initialize Groq client with API key and model."""
        self.model_name = model_name
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        # Initialize client with or without proxies

        self.client = groq.Client(api_key=api_key)

    async def process_image_bytes(self, image_bytes: bytes) -> str:
        """Process an image using Groq's vision model to extract tables into CSV format."""
        try:
            # Convert image bytes to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Create the message content with the image
            # For Llama 3.2 vision models, we need to follow this specific format
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
            
            # Prepare the complete request
            messages = [
                {
                    "role": "user",
                    "content": message_content
                }
            ]
            
            # Make the API call synchronously to avoid await issues
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0,
                max_tokens=4000
            )
            
            # Extract the CSV content from the response
            csv_content = response.choices[0].message.content
            
            # Clean up the CSV content by removing any markdown code blocks or additional text
            if "```" in csv_content:
                # Extract content between code blocks if present
                csv_parts = csv_content.split("```")
                for part in csv_parts:
                    if "csv" not in part and "," in part and "\n" in part:
                        csv_content = part.strip()
                        break
            
            # If the response doesn't have CSV content or is empty, return an error
            if not csv_content or "," not in csv_content:
                return "Error: Could not extract CSV data from the image"
                
            return csv_content
            
        except Exception as e:
            print(f"Error processing image with Groq API: {str(e)}")
            # Provide a fallback for testing if the API call fails
            return f"Error: {str(e)}" 