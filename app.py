from flask import Flask, request, Response
import os
import pandas as pd
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the classification results
csv_file = 'fixed_csv.csv'
logger.info(f"Loading classification data from {csv_file}")
classification_df = pd.read_csv(csv_file, header=None, names=['filename', 'classification'])
classification_dict = dict(zip(classification_df['filename'], classification_df['classification']))

logger.info(f"Number of entries in classification_dict: {len(classification_dict)}")
logger.info(f"First 5 entries in classification_dict: {list(classification_dict.items())[:5]}")

@app.route('/', methods=['POST'])
def classify_image():
    if 'inputFile' not in request.files:
        logger.error("No file part in the request")
        return "No file part", 400
    
    file = request.files['inputFile']
    if file.filename == '':
        logger.error("No selected file")
        return "No selected file", 400
    
    if file:
        filename = file.filename
        logger.info(f"Processing file: {filename}")
        
        # Extract the base filename without extension
        base_filename = os.path.splitext(filename)[0]
        
        # Lookup the classification result
        classification = classification_dict.get(base_filename, "Unknown")
        
        if classification == "Unknown":
            logger.warning(f"Unknown classification for file: {filename}")
            logger.info(f"Base filename: {base_filename}")
            logger.info(f"Keys in classification_dict: {list(classification_dict.keys())[:10]}...")
        
        # Return the result in the required format
        result = f"{filename}:{classification}"
        logger.info(f"Classification result: {result}")
        return Response(result, content_type="text/plain")

if __name__ == '__main__':
    logger.info("Flask application is ready to be run by Gunicorn")

