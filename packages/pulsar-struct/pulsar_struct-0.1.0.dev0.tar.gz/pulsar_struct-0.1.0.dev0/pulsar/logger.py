from datetime import datetime
import os
import hashlib
import uuid


def write_log(raw_str: str) -> str:
    """
    Write content to a text file in the current directory with a unique filename.

    Args:
        raw_str (str): The content to write to the file

    Returns:
        str: The path of the created file
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Generate unique filename components
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]

    # Create content hash for additional uniqueness
    content_hash = hashlib.md5(raw_str.encode()).hexdigest()[:6]

    # Construct filename
    filename = f"pulsar_{timestamp}_{content_hash}_{unique_id}.txt"
    filepath = os.path.join(logs_dir, filename)

    # Write content to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(raw_str)
        return filepath
    except Exception as e:
        raise IOError(f"Failed to write log file: {str(e)}")


# Example usage:
if __name__ == "__main__":
    # Test the function
    content = """## CalculatorInput

### Parameters
*Operation*: add
*X*: 10
*Y*: 5

### Result
15"""

    try:
        file_path = write_log(content)
        print(f"Log written successfully to: {file_path}")
    except IOError as e:
        print(f"Error: {e}")
