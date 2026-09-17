import os
from tools.market_data import get_financial_metrics
from tools.indicators import calculate_sma
from core.react_loop import FinancialAgentCore

from dotenv import load_dotenv

# Register available tools
TOOLS_REGISTRY = {
    "get_financial_metrics": get_financial_metrics,
    "calculate_sma": calculate_sma
}

def main():
    # Initialize Agent Core
    agent = FinancialAgentCore(tools_dict=TOOLS_REGISTRY)

    # Sample query
    query = "Check financial metrics for NVDA stock, calculate its 20-day SMA, and provide a short trend assessment."
    report = agent.run(query)
    
    print(report)

if __name__ == "__main__":
    load_dotenv()
    main()