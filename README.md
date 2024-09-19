# Stock Data Visualization with Dash and YFinance

This is my personal attempt in creating a python script that allows users to visualize stock data using the `yfinance` API and `Dash`. The application fetches historical stock data for any given ticker symbol and displays it in interactive charts built with Plotly.

## Features

- **Interactive Stock Data Visualization**: Enter a stock ticker symbol (e.g., `AAPL` for Apple) and select a time period to view the historical stock data.
- **Cached Data Fetching**: Utilizes LRU caching to store previously fetched stock data, improving performance and reducing redundant API calls.
- **Real-time Graphs**: The stock data is displayed using Plotly for interactive and visually appealing graphs.
- **Dynamic User Interface**: Built with Dash, the web interface allows users to input stock symbols and select time periods to update the graphs.

## Requirements

To run the application, ensure you have the following Python libraries installed:

```bash
pip install dash yfinance plotly
```

## Usage

1.  Clone this repository using Git:
     ```bash
     git clone https://github.com/Catefishh/Random-forest-stock-prediciton.git
     ```
   - Or download the `script.py` and `assets` directly.

2. Run the application:

   ```bash
   python script.py
   ```

3. Open your browser and go to `http://127.0.0.1:8050/` to interact with the web app.

## Application Structure

- `app.py`: The main Dash app that sets up the layout and callbacks for user interaction.
- `fetch_stock_data(symbol, period)`: A helper function that uses the `yfinance` API to retrieve stock data for a given symbol and time period. This function is cached to enhance performance.
- **Interactive Graphs**: The stock data is displayed using Plotly's graphing libraries, providing zoomable and interactive charts.

## Contributing

Feel free to open issues or submit pull requests if you'd like to contribute to the project. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.