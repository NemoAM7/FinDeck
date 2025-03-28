# Data Science Assistant Setup Guide

This guide walks you through setting up and running the Data Science Assistant.

## Prerequisites

- Python 3.8+ with pip
- Node.js 16+ and npm (for React Native frontend, optional)

## Backend Setup

1. Install required dependencies:
   ```bash
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt
   ```

2. Start the FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will:
- Automatically launch the data exploration server in a separate process
- Process data science commands directly
- Expose a REST API endpoint at http://localhost:8000

## Testing the Backend

Once the server is running, you can test it with a curl command:

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"list dataframes"}]}'
```

Or check the health endpoint:
```bash
curl http://localhost:8000/health
```

## API Endpoints

- `POST /chat`: Send a chat message to the assistant
  - Request body: `{"messages": [{"role": "user", "content": "your message"}]}`
  - Commands: 
    - `load csv [path]`
    - `run script [python code]`
    - `get info [dataframe_name]`
    - `list dataframes`

- `GET /health`: Check if the server is running

## How It Works

The system has two main components:

1. **Data Exploration Server** (`server/data_exploration_server.py`):
   - This is launched as a subprocess by the backend
   - It provides tools for data exploration (not directly used in this simplified version)

2. **FastAPI Backend** (`backend/main.py`):
   - Provides a REST API for the frontend
   - Directly implements data science functionality
   - Handles CSV loading, script execution, and dataframe management

## Frontend Setup (Optional)

If you have Node.js installed and want to use the React Native frontend:

1. Make sure Node.js commands are working:
```bash
node --version
npm --version
```

2. Install React Native CLI:
```bash
npm install -g react-native-cli
```

3. Create a React Native project:
```bash
npx react-native init DataScienceAssistant
cd DataScienceAssistant
```

4. Copy frontend files from this repository to your project.

5. Install dependencies:
```bash
npm install
```

6. Update the `API_URL` in App.js to point to your FastAPI backend (default is http://localhost:8000).

7. Start the React Native app:
```bash
npx react-native start
```

8. In a separate terminal, run the app on your device/emulator:
```bash
# For Android
npx react-native run-android

# For iOS (Mac only)
npx react-native run-ios
```

## Troubleshooting

### Backend Issues

1. If you see errors starting the server:
   - Check that you've installed all the required dependencies
   - Make sure there are no conflicting processes using the same port

2. If CSV loading fails:
   - Verify the file path is correct and the file exists
   - Check that the CSV file is properly formatted

3. If script execution fails:
   - Examine the error message for syntax or runtime errors
   - Make sure you're not using packages that aren't available

### Windows-Specific Notes

This version was specially designed to work on Windows by:
1. Avoiding asyncio subprocess functionality that isn't supported on Windows
2. Implementing direct data science functionality in the FastAPI backend
3. Starting the server as a separate process with proper communication 