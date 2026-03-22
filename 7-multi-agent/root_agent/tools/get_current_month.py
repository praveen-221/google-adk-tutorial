from datetime import datetime

def get_current_month(format: str = "%Y-%m") -> dict:
    """
    Get the current month.
    Args:
        format (str): The format in which to return the current month. Example format: "%Y-%m"
    Returns:        
        dict: A dictionary containing the current month in the specified format.
    """
    return {
        "current_month": datetime.now().strftime(format)
    }