import os
from loguru import logger

def create_file(filepath: str, content: str):
    """
    Creates a file with the provided content if it does not already exist.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Check if the file already exists
    if not os.path.exists(filepath):
        # Write the content to the file asynchronously
        with open(filepath, "w") as file:
            file.write(content)
        logger.info(f"File '{filepath}' has been created successfully.")
    else:
        logger.info(f"File '{filepath}' already exists. No changes were made.")