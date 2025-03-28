# Table Extractor

A Python tool for extracting tables from images and converting them to CSV format. This tool is particularly useful for digitizing handwritten tables from historical documents.

## Features

- Detects table structure using line detection
- Extracts text from table cells using Tesseract OCR
- Converts extracted data to pandas DataFrame and CSV format
- Handles both printed and handwritten tables
- Includes logging for debugging and monitoring

## Prerequisites

1. Python 3.7 or higher
2. Tesseract OCR installed on your system:
   - Windows: Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - Mac: `brew install tesseract`

## Installation

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure Tesseract is in your system PATH

## Usage

1. Place your table image in the `server/data` directory

2. Run the script:
   ```bash
   python server/table_extractor.py
   ```

3. The script will:
   - Process the image
   - Extract table structure
   - Perform OCR on each cell
   - Save the results to CSV
   - Display the extracted data

## Customization

You can adjust the following parameters in the `TableExtractor` class:

- `min_line_length`: Minimum length of line to be considered a table line (default: 100)
- `line_thickness`: Thickness of lines to detect (default: 2)
- `cell_padding`: Padding around cell content (default: 5)

## Logging

Logs are written to `server/logs/table_extractor.log`. You can monitor the logs in real-time using:

- Windows: `type server/logs/table_extractor.log`
- Unix: `tail -f server/logs/table_extractor.log`

## Example

```python
from table_extractor import TableExtractor

# Initialize the extractor
extractor = TableExtractor()

# Process an image
df = extractor.process_image(
    "path/to/your/image.png",
    output_path="path/to/output.csv"
)

# View the extracted data
print(df)
```

## Tips for Best Results

1. Use high-quality images with good contrast
2. Ensure the table has clear lines and borders
3. Avoid complex backgrounds
4. For handwritten tables, use clear, well-formed handwriting
5. Adjust the parameters if needed for your specific use case

## Troubleshooting

1. If table detection fails:
   - Check image quality
   - Adjust `min_line_length` and `line_thickness`
   - Ensure proper lighting in the image

2. If OCR accuracy is poor:
   - Improve image quality
   - Adjust `cell_padding`
   - Consider using a different OCR engine

3. If cells are not properly aligned:
   - Check the table structure
   - Adjust the cell detection parameters
   - Verify the image is not skewed

## License

MIT License 