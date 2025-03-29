# Deploying SmartBI-clone on Replit

This guide explains how to deploy this Data Science Assistant on Replit.

## Steps to Deploy

1. **Create a Replit Account**
   - Sign up at [replit.com](https://replit.com) if you don't have an account

2. **Create a New Repl**
   - Click "Create Repl" button
   - Choose "Python" as the template
   - Name your project (e.g., "SmartBI-clone")
   - Click "Create Repl"

3. **Upload Project Files**
   - Use the Replit file upload feature or
   - Connect to GitHub if your project is there
   - Make sure all files are in the correct directories

4. **Set Environment Variables**
   - Go to the "Tools" section in the sidebar
   - Select "Secrets"
   - Add your environment variables (from your .env file)
   - Make sure to add any API keys needed

5. **Run the Project**
   - Replit will automatically install dependencies from pyproject.toml
   - Press the "Run" button
   - The application will start and be available at the URL provided by Replit

## Project Structure

This project has the following components:
- `api/`: FastAPI backend for data processing
- `server/`: Data exploration server
- `.replit`: Configuration file for Replit
- `pyproject.toml`: Dependencies for Poetry/Replit

## Troubleshooting

- If you encounter dependency issues, check the Replit console for error messages
- Make sure your environment variables are correctly set in the Secrets tab
- If you need to run a custom command, you can modify the .replit file

## Usage

Once deployed:
1. Access your application via the URL provided by Replit
2. Use the API endpoints as documented in the main README
3. For any updates to your code, simply edit in Replit and press "Run" again

## Notes

- Replit provides 0.5 GB of RAM and limited disk space on free accounts
- For larger applications, consider upgrading to a paid Replit plan
- The application will sleep after inactivity on free plans; use services like UptimeRobot to keep it awake 