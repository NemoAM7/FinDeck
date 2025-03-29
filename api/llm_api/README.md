# LLM API

This API allows you to interact with Large Language Models (LLMs) through text prompts, image inputs, or a combination of both. Images are stored directly in the database for easy retrieval.

## Endpoints

### Text Prompts

```
POST /api/llm/prompt/text
```

Process a text-only prompt and get a response from the LLM.

**Request Body:**
```json
{
  "prompt": "Your text prompt here",
  "model_name": "llama-3.2-90b-preview" // Optional, defaults to llama-3.2-90b-preview
}
```

**Response:**
```json
{
  "id": 1,
  "prompt": "Your text prompt here",
  "response": "LLM response text",
  "prompt_type": "text_only",
  "timestamp": "2023-06-15T10:30:45.123456",
  "image_filename": null,
  "model_used": "llama-3.2-90b-preview",
  "processing_time": 1234 // milliseconds
}
```

### Text + Image Prompts

```
POST /api/llm/prompt/image
```

Process a text prompt with an accompanying image.

**Form Data:**
- `prompt`: Text description or question about the image
- `image`: Image file (JPEG, PNG, etc.)
- `model_name`: (Optional) Model to use, defaults to "llama-3.2-90b-vision-preview"

**Response:**
```json
{
  "id": 2,
  "prompt": "What does this image show?",
  "response": "LLM response about the image",
  "prompt_type": "text_and_image",
  "timestamp": "2023-06-15T10:35:12.654321",
  "image_filename": "example.jpg",
  "model_used": "llama-3.2-90b-vision-preview",
  "processing_time": 2345 // milliseconds
}
```

### Image-Only Prompts

```
POST /api/llm/prompt/image-only
```

Process an image without a specific text prompt (uses a default description prompt).

**Form Data:**
- `image`: Image file (JPEG, PNG, etc.)
- `model_name`: (Optional) Model to use, defaults to "llama-3.2-90b-vision-preview"

**Response:**
```json
{
  "id": 3,
  "prompt": "What can you see in this image? Provide a detailed description.",
  "response": "LLM description of the image",
  "prompt_type": "image_only",
  "timestamp": "2023-06-15T10:40:20.123456",
  "image_filename": "example2.jpg",
  "model_used": "llama-3.2-90b-vision-preview",
  "processing_time": 2100 // milliseconds
}
```

### Interaction History

```
GET /api/llm/history
```

Get a list of all previous LLM interactions.

**Response:**
```json
[
  {
    "id": 3,
    "prompt": "What can you see in this image? Provide a detailed description.",
    "response": "LLM description of the image",
    "prompt_type": "image_only",
    "timestamp": "2023-06-15T10:40:20.123456",
    "image_filename": "example2.jpg"
  },
  {
    "id": 2,
    "prompt": "What does this image show?",
    "response": "LLM response about the image",
    "prompt_type": "text_and_image",
    "timestamp": "2023-06-15T10:35:12.654321",
    "image_filename": "example.jpg"
  },
  {
    "id": 1,
    "prompt": "Your text prompt here",
    "response": "LLM response text",
    "prompt_type": "text_only",
    "timestamp": "2023-06-15T10:30:45.123456",
    "image_filename": null
  }
]
```

### Interaction Details

```
GET /api/llm/history/{interaction_id}
```

Get detailed information about a specific interaction.

**Response:**
```json
{
  "id": 1,
  "prompt": "Your text prompt here",
  "response": "LLM response text",
  "prompt_type": "text_only",
  "timestamp": "2023-06-15T10:30:45.123456",
  "image_filename": null,
  "model_used": "llama-3.2-90b-preview",
  "processing_time": 1234
}
```

### Retrieve Interaction Image

```
GET /api/llm/history/{interaction_id}/image
```

Get the image associated with a specific interaction. Returns the image directly as binary data with the appropriate content type.

## Usage Examples

### Text Prompt Example (JavaScript/Fetch)

```javascript
const response = await fetch('http://localhost:8000/api/llm/prompt/text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'Explain how neural networks work',
    model_name: 'llama-3.2-90b-preview'
  }),
});

const result = await response.json();
console.log(result.response);
```

### Image Prompt Example (JavaScript/Fetch)

```javascript
const formData = new FormData();
formData.append('prompt', 'What can you tell me about this image?');
formData.append('image', imageFile); // From file input
formData.append('model_name', 'llama-3.2-90b-vision-preview');

const response = await fetch('http://localhost:8000/api/llm/prompt/image', {
  method: 'POST',
  body: formData,
});

const result = await response.json();
console.log(result.response);
```

### Retrieving an Image (JavaScript/Fetch)

```javascript
// Get interaction details first
const detailsResponse = await fetch('http://localhost:8000/api/llm/history/2');
const details = await detailsResponse.json();

// If it has an image, fetch it
if (details.image_filename) {
  const imageUrl = `http://localhost:8000/api/llm/history/2/image`;
  
  // Display the image
  document.getElementById('resultImage').src = imageUrl;
}
```

## Supported Models

- Text-only prompts: "llama-3.2-90b-preview" (default)
- Image prompts: "llama-3.2-90b-vision-preview" (default)

Other Groq-supported models can be specified in the `model_name` parameter. 