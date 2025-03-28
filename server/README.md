# MCP Data Exploration Server

A server for interactive data exploration through the MCP protocol. This server allows for loading, exploring, and analyzing CSV datasets.

## Features

- Load CSV files into pandas DataFrames
- Run Python scripts with access to loaded DataFrames
- Get information about loaded DataFrames
- List all currently loaded DataFrames

## Getting Started

### Prerequisites

- Python 3.7+
- pandas
- numpy
- mcp package (`pip install mcp`)

### Running the Server

```bash
python data_exploration_server.py
```

## Using with the MCP Client

This server is designed to work with the MCP client. Connect to it using:

```bash
python client.py server/data_exploration_server.py
```

## Available Tools

### 1. load_csv

Loads a CSV file into a pandas DataFrame.

**Parameters:**
- `csv_path` (string, required): Path to the CSV file
- `df_name` (string, optional): Name for the DataFrame, defaults to df_1, df_2, etc.

**Example:**
```
load_csv with path="data/my_dataset.csv", df_name="housing_data"
```

### 2. run_script

Executes a Python script with access to loaded DataFrames.

**Parameters:**
- `script` (string, required): The Python script to execute

**Example:**
```
run_script with script="""
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
df_1.plot(kind='scatter', x='price', y='sqft')
plt.title('Price vs Square Footage')
plt.savefig('price_vs_sqft.png')
print('Plot saved to price_vs_sqft.png')
"""
```

### 3. get_dataframe_info

Gets detailed information about a loaded DataFrame.

**Parameters:**
- `df_name` (string, required): Name of the DataFrame

**Example:**
```
get_dataframe_info with df_name="housing_data"
```

### 4. list_dataframes

Lists all loaded DataFrames.

**Example:**
```
list_dataframes
```

## Example Workflow

1. Load a CSV file:
   ```
   load_csv with csv_path="data/housing.csv"
   ```

2. List loaded DataFrames:
   ```
   list_dataframes
   ```

3. Get information about the loaded DataFrame:
   ```
   get_dataframe_info with df_name="df_1"
   ```

4. Run a script to analyze the data:
   ```
   run_script with script="""
   # Calculate average price by neighborhood
   avg_prices = df_1.groupby('neighborhood')['price'].mean().sort_values(ascending=False)
   print(avg_prices)
   """
   ```

## License

MIT License 