from datetime import datetime
import yfinance as yf
from google.adk.agents import Agent

def get_stock_price(stock_name: str) -> dict:
    """
        Get stock price for the given stock
        Args:
            stock_name: name of the stock for which price needs to be fetched
        Returns:
            A confimation message
            Stock name
            Stock price
            timestamp
    """
    try:
        ticker = yf.Ticker(stock_name)
        stock_price = ticker.info.get("currentPrice")

        if stock_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch stock price for {stock_name}"
            }
        
        current_time = datetime.now().strftime(format = "%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "stock_name": stock_name,
            "stock_price": stock_price,
            "timestamp": current_time
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}"
        }

stock_agent = Agent(
    name = "stock_agent",
    model = "gemma-3-27b-it",
    description = "An agent that can look up stock prices and track them over time.",
    instruction = """
        You are a helpful stock market assistant that helps users track their stocks of interest.
        
        When asked about stock prices:
        1. Use the get_stock_price tool to fetch the latest price for the requested stock(s)
        2. Format the response to show each stock's current price and the time it was fetched
        3. If a stock price couldn't be fetched, mention this in your response
        
        Example response format:
        "Here are the current prices for your stocks:
        - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
        - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
        - META: $123.45 (updated at 2024-04-21 16:30:00)"

        If the user asks about anything else, you should delegate the task to the manager agent.
    """,
    tools = [get_stock_price]
)