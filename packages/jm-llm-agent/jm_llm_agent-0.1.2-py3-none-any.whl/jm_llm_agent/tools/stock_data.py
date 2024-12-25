import pandas as pd
import yfinance as yf


def get_stock_data(symbol: str, period: str = "3mo") -> pd.DataFrame | None:
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        df = df.reset_index()
        return df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    except Exception as e:
        print(f"Error getting stock data: {e}")
        return None


def trans_data_to_json(data):
    # Format date and round numeric columns
    df = data.copy()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_columns:
        df[col] = df[col].round(2)
    return df.to_json(orient="records")


def trans_data_to_markdown(data):
    # Format date and round numeric columns
    df = data.copy()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_columns:
        df[col] = df[col].round(2)

    # Convert DataFrame to markdown table
    markdown_table = "| " + " | ".join(df.columns) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"

    # Add rows
    for _, row in df.iterrows():
        markdown_table += "| " + " | ".join(str(val) for val in row.values) + " |\n"

    return markdown_table


if __name__ == "__main__":
    symbol = "AAPL"
    stock_data = get_stock_data(symbol)
    if stock_data is not None:
        print("\nStock History:")
        print(stock_data.head())

    symbol = "tsla"
    data = get_stock_data(symbol)

    # 保存为 Markdown 表格
    md_path = f"{symbol}.md"
    md_content = trans_data_to_markdown(get_stock_data(symbol))
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"Data saved to {md_path}")
