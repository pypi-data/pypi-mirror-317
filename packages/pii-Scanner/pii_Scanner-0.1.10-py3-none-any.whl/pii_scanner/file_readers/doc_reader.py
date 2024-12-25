import json
import logging
from typing import Dict, Any, Optional, Union
from unstructured.partition.auto import partition
from pii_scanner.scanners.spacy_matcher_scanner import SpacyMatchScanner
from pii_scanner.file_readers.process_column import process_column_data
from pii_scanner.utils.preprocess_text_nlp import preprocess_text

import nltk

# # Ensure you have NLTK stopwords downloaded
# nltk.download('punkt')
# nltk.download('stopwords')

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



async def doc_pii_detector(file_path: str, region=None) -> str:
    """
    Detect PII in DOCX, PDF, or TXT files using NER Scanner.

    """
    scanner = SpacyMatchScanner()  # Initialize your NER Scanner

    try:
        # Extract elements from the document using Unstructured
        elements = partition(filename=file_path)
        logger.info(f"Successfully read and partitioned file: {file_path}")

        # Preprocess each element's text and concatenate all preprocessed texts into one string
        texts = [await preprocess_text(element.text) for element in elements if hasattr(element, 'text')]
        combined_text = ' '.join(texts)  # Join all preprocessed texts into one string

        # Log the number of elements and the combined string
        logger.info(f"Preprocessed {len(texts)} elements. Combined text: {combined_text}")

        # Perform NER scan on the entire list of preprocessed texts
        results = await scanner.scan_async(combined_text, region=region)
        
        logger.info("Processing completed successfully.")
        return results

    except FileNotFoundError:
        error_message = f"Error: The file '{file_path}' was not found."
        logger.error(error_message)
        return json.dumps({"error": error_message}, indent=4)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return json.dumps({"error": str(e)}, indent=4)

