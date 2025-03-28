# Data Science Assistant

A simple but powerful data science assistant that allows you to:
- Load and analyze CSV files
- Run Python data science scripts
- Get information about loaded DataFrames
- List available DataFrames

## Project Structure

- `backend/`: FastAPI backend that handles data processing
- `frontend/`: React Native frontend for interacting with the assistant
- `server/`: Data exploration server components

## Setup Instructions

### Prerequisites

- Python 3.8+ with pip
- Node.js 16+ and npm (for React Native)
- React Native CLI

### Step 1: Setup the Python Backend

1. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Start the FastAPI server:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Setup the React Native Frontend

#### If Node.js Commands Aren't Working

If you've installed Node.js but the `node` and `npm` commands aren't recognized, follow these steps:

1. **Fix PATH Issues**:
   - Open Windows search
   - Type "Environment Variables" and select "Edit the system environment variables"
   - Click "Environment Variables" at the bottom
   - Under "System variables" find "Path" and click "Edit"
   - Check if your Node.js installation path is there (typically `C:\Program Files\nodejs\`)
   - If not, add it and click "OK"
   - **Restart your terminal or PowerShell**

2. **Verify Installation Directly**:
   Try running the Node.js executable directly:
   ```
   C:\Program Files\nodejs\node.exe --version
   C:\Program Files\nodejs\npm.cmd --version
   ```

3. **Reinstall Node.js**:
   If the above doesn't work, reinstall Node.js:
   - Download from [nodejs.org](https://nodejs.org/)
   - Run as Administrator
   - Choose the option to automatically install necessary tools

#### Setup React Native

Once Node.js is working:

1. Install React Native CLI:
```bash
npm install -g react-native-cli
```

2. Install project dependencies:
```bash
cd frontend
npm install
```

3. Start the React Native development server:
```bash
npx react-native start
```

4. In a new terminal, run the app:
```bash
# For Android
npx react-native run-android

# For iOS (Mac only)
npx react-native run-ios
```

## Usage

1. Start the backend server
2. Start the React Native app
3. Use the following commands in the chat:
   - `load csv [path]` - Load a CSV file
   - `run script [python code]` - Run a Python script
   - `get info [dataframe_name]` - Get information about a DataFrame
   - `list dataframes` - List all loaded DataFrames

## Troubleshooting

### Node.js Issues

1. **Command not found errors**:
   - Make sure Node.js is in your PATH
   - Try using the full path to node.exe

2. **Permission errors**:
   - Try running your terminal as Administrator

3. **Module not found errors**:
   - Make sure you've run `npm install` in the project directory

### Backend Issues

1. **Import errors**:
   - Make sure all Python dependencies are installed
   - Check that you're running the server from the correct directory

2. **CSV loading errors**:
   - Ensure the CSV file exists at the specified path
   - Check that the CSV file is properly formatted

### React Native Issues

1. **Metro bundler errors**:
   - Clear the cache: `npx react-native start --reset-cache`

2. **Android device not connected**:
   - Run `adb devices` to check for connected devices
   - Make sure USB debugging is enabled on your device

3. **iOS simulator issues**:
   - Ensure Xcode is properly installed (Mac only)
   - Try `npx react-native run-ios --simulator="iPhone 14"` 