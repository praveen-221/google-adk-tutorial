from datetime import datetime

def get_current_time(format: str) -> dict:
    """
    Get the current time.
    Args:
        format (str): The format in which to return the current time. Example format: "%Y-%m-%d %H:%M:%S"
    Returns:        
        dict: A dictionary containing the current time in the specified format.
    """
    return {
        "current_time": datetime.now().strftime(format)
    }