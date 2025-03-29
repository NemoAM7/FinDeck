from typing import Any, Dict, Optional
import pandas as pd
import numpy as np
import io
import sys
import os
import traceback
import logging
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create logs directory if it doesn't exist
os.makedirs('server/logs', exist_ok=True)

# Set up file logging instead of console
log_file = 'server/logs/data_exploration.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a'),
    ]
)
logger = logging.getLogger('data_exploration_server')

# Create a custom log function that writes to the log file, not console
def log_message(message, level='INFO'):
    """Log a message to the log file without printing to console"""
    if level.upper() == 'INFO':
        logger.info(message)
    elif level.upper() == 'ERROR':
        logger.error(message)
    elif level.upper() == 'WARNING':
        logger.warning(message)
    elif level.upper() == 'DEBUG':
        logger.debug(message)

# Print startup message
log_message(f"Data exploration server starting up. Logs will be written to {log_file}")
log_message("You can monitor logs in a separate terminal using: 'type server/logs/data_exploration.log' (Windows) or 'tail -f server/logs/data_exploration.log' (Unix)")

# Store loaded dataframes
dataframes = {}
df_counter = 1

# Initialize FastMCP server
mcp = FastMCP("data-exploration")

@mcp.tool()
async def load_csv(csv_path: str, df_name: Optional[str] = None) -> str:
    """Loads a CSV file into a DataFrame.
    
    Args:
        csv_path: Path to the CSV file
        df_name: Optional name for the DataFrame (defaults to df_1, df_2, etc.)
    """
    global df_counter
    try:
        # Generate a default dataframe name if not provided
        if not df_name:
            df_name = f"df_{df_counter}"
            df_counter += 1
        
        logger.info(f"Loading CSV file: {csv_path}")
        
        # Load the CSV file
        df = pd.read_csv(csv_path)
        
        # Store the dataframe in memory
        dataframes[df_name] = df
        
        # Generate summary information
        summary = {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample": df.head(5).to_dict(),
            "missing_values": df.isna().sum().to_dict()
        }
        
        logger.info(f"Successfully loaded {csv_path} with {summary['shape'][0]} rows and {summary['shape'][1]} columns")
        
        return f"Successfully loaded {csv_path} as '{df_name}'.\n" + \
               f"Shape: {summary['shape'][0]} rows x {summary['shape'][1]} columns\n" + \
               f"Columns: {', '.join(summary['columns'])}\n" + \
               f"First 5 rows preview available in memory."
    
    except Exception as e:
        error_msg = f"Error loading CSV: {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def run_script(script: str) -> str:
    """Executes a Python script with access to loaded dataframes.
    
    Args:
        script: The Python script to execute
    """
    try:
        # Log script execution
        log_message(f"Executing script: {script[:100]}{'...' if len(script) > 100 else ''}")
        
        # Create a StringIO object to capture output
        output_buffer = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output_buffer
        
        # Create a local environment with pandas, numpy and loaded dataframes
        local_env = {
            'pd': pd,
            'np': np,
            'plt': None,  # Will be imported in the script if needed
        }
        
        # Add all loaded dataframes to the local environment
        for df_name, df in dataframes.items():
            local_env[df_name] = df
        
        # Execute the script
        try:
            exec(script, local_env)
            result = output_buffer.getvalue()
            
            # If there was no output, check if the script returned a value
            if not result and '_return_value' in local_env:
                result = str(local_env['_return_value'])
                
            # Handle figure output if matplotlib was used
            if 'plt' in local_env and local_env['plt'] is not None:
                result += "\n[Note: Matplotlib figure was generated but cannot be displayed directly in text. Save it to a file or convert to base64 encoding to view.]"
                
            log_message("Script executed successfully")
            return result if result else "Script executed successfully (no output)"
            
        except Exception as e:
            error_msg = f"Error executing script: {str(e)}\n"
            error_msg += traceback.format_exc()
            log_message(f"Script execution error: {str(e)}", 'ERROR')
            return error_msg
            
    finally:
        # Restore stdout
        sys.stdout = old_stdout

@mcp.tool()
async def get_dataframe_info(df_name: str) -> str:
    """Get information about a loaded DataFrame.
    
    Args:
        df_name: Name of the DataFrame to get info about
    """
    log_message(f"Getting info for DataFrame: {df_name}")
    
    if df_name not in dataframes:
        log_message(f"DataFrame '{df_name}' not found", 'WARNING')
        return f"Error: DataFrame '{df_name}' not found. Available DataFrames: {list(dataframes.keys())}"
    
    df = dataframes[df_name]
    
    # Generate DataFrame information
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    # Add descriptive statistics
    desc_stats = df.describe().to_string()
    
    # Add correlation information if numerical columns exist
    num_cols = df.select_dtypes(include=[np.number]).columns
    corr_str = ""
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        corr_str = f"\n\nCorrelation Matrix:\n{corr.to_string()}"
    
    log_message(f"Successfully retrieved info for DataFrame: {df_name}")
    return f"DataFrame '{df_name}' Information:\n\n{info_str}\n\nDescriptive Statistics:\n{desc_stats}{corr_str}"

@mcp.tool()
async def list_dataframes() -> str:
    """List all loaded DataFrames."""
    log_message("Listing all loaded DataFrames")
    
    if not dataframes:
        return "No DataFrames are currently loaded."
    
    result = "Loaded DataFrames:\n"
    for name, df in dataframes.items():
        result += f"- {name}: {df.shape[0]} rows × {df.shape[1]} columns\n"
    
    return result

if __name__ == "__main__":
    # Log server startup
    log_message("Data exploration server is running")
    print(f"Server started. Logs are being written to {log_file}")
    print(f"To view logs in a separate terminal, use:")
    print(f"  - Windows: type {log_file}")
    print(f"  - Unix: tail -f {log_file}")
    
    # Initialize and run the server
    mcp.run(transport='stdio') 