# CHENYE-STOCK-ANALYSIS

**CHENYE-STOCK-ANALYSIS** is a Python package built on [BaoStock](https://www.baostock.com/), designed to simplify the process of retrieving stock data from the Chinese A-share market and calculating common technical indicators such as Bollinger Bands and KDJ. This tool enables developers to efficiently analyze and visualize stock data.

------

### **1. Features**

- **Retrieve the latest trading day data:** Query the most recent trading day in the Chinese A-share market.
- **Filter stock codes:** Retrieve stock codes and names, excluding ST stocks, Sci-tech innovation board (科创板), and Beijing Stock Exchange (北交所) stocks.
- **Stock data acquisition:** Retrieve historical K-line data for given stock codes and date ranges.
- Technical indicators calculation:
  - **Bollinger Bands:** Calculate the middle, upper, and lower bands.
  - **KDJ indicators:** Calculate K, D, and J values.
- **Data export:** Save the retrieved stock data to CSV or Excel files.

------

### **2. Installation**

Run the following command in your Python environment to install the package:

```bash
pip install CHENYE-STOCK-ANALYSIS==0.1.4
```

------

### **3. Usage Examples**

#### **3.1 Querying technical indicators for a single stock**

The following example demonstrates how to query technical indicators for a single stock (e.g., Pudong Development Bank `sh.600000`) within a specified date range:

```python
from stock_analysis.stock_analysis import DataFetcher

# Initialize DataFetcher
fetcher = DataFetcher()

try:
    # Get the most recent trading day
    recent_trading_day = fetcher.find_recent_trading_day()
    print(f"Most recent trading day: {recent_trading_day}")

    # Query data for Pudong Development Bank over the last 30 days
    code = "sh.600000"
    start_date = "20231201"
    end_date = recent_trading_day

    # Retrieve K-line data
    df = fetcher.fetch_stock_data(code, start_date, end_date)
    if df.empty:
        print(f"No data retrieved for stock {code}")
    else:
        # Calculate Bollinger Bands
        df = fetcher.compute_bollinger_bands(df)

        # Calculate KDJ
        df = fetcher.compute_kdj(df)

        # Display the results
        print(df)

        # Save to an Excel file
        df.to_excel(f"{code}_data.xlsx", index=False)
        print(f"Data saved to {code}_data.xlsx")
finally:
    # Log out of BaoStock
    fetcher.logout()
```

------

#### **3.2 Retrieving technical indicators for all stocks**

The following example demonstrates how to retrieve technical indicators for all stocks in the Chinese A-share market and save the results to an Excel file:

```python
from stock_analysis.stock_analysis import DataFetcher

# Initialize DataFetcher
fetcher = DataFetcher()

try:
    # Get the most recent trading day
    recent_trading_day = fetcher.find_recent_trading_day()
    print(f"Most recent trading day: {recent_trading_day}")

    # Retrieve all stock codes and names
    codes, names = fetcher.get_all_stock_codes()
    print(f"Retrieved {len(codes)} stocks")

    # Get data for all stocks on the most recent trading day
    data = fetcher.get_data_for_all_stocks(codes, names, recent_trading_day)
    print(f"Retrieved data for {len(data)} stocks")

    # Save to an Excel file
    output_file = f"All_Stocks_{recent_trading_day}.xlsx"
    data.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")
finally:
    # Log out of BaoStock
    fetcher.logout()
```

------

### **4. Function Descriptions**

#### **4.1 Query the most recent trading day**

```python
recent_trading_day = fetcher.find_recent_trading_day()
```

- **Purpose:** Query the most recent trading day in the Chinese A-share market.
- **Returns:** A string representing the date in `YYYYMMDD` format.

------

#### **4.2 Retrieve all stock codes**

```python
codes, names = fetcher.get_all_stock_codes()
```

- **Purpose:** Retrieve stock codes and names for all non-ST stocks, excluding Sci-tech Innovation Board and Beijing Stock Exchange stocks.
- Returns:
  - `codes`: List of stock codes.
  - `names`: List of stock names.

------

#### **4.3 Retrieve data for a single stock**

```python
df = fetcher.fetch_stock_data("sh.600000", "20231201", "20231231")
```

- **Purpose:** Retrieve historical K-line data for a single stock within a specified date range.
- Parameters:
  - `code`: Stock code (e.g., `sh.600000`).
  - `start_date`: Start date in `YYYYMMDD` format.
  - `end_date`: End date in `YYYYMMDD` format.
- **Returns:** A `DataFrame` containing the date, open price, close price, and other information.

------

#### **4.4 Calculate Bollinger Bands**

```python
df = fetcher.compute_bollinger_bands(df)
```

- **Purpose:** Add Bollinger Bands calculations to a given `DataFrame`.
- Parameters:
  - `df`: A `DataFrame` containing the `close` column.
- **Returns:** A new `DataFrame` with added columns for the middle, upper, and lower bands.

------

#### **4.5 Calculate KDJ indicators**

```python
df = fetcher.compute_kdj(df)
```

- **Purpose:** Add KDJ indicator calculations to a given `DataFrame`.
- Parameters:
  - `df`: A `DataFrame` containing the `low`, `high`, and `close` columns.
- **Returns:** A new `DataFrame` with added columns for K, D, and J values.

------

#### **4.6 Retrieve data for all stocks**

```python
data = fetcher.get_data_for_all_stocks(codes, names, recent_trading_day)
```

- **Purpose:** Retrieve historical data for all specified stocks and calculate technical indicators.
- Parameters:
  - `codes`: List of stock codes.
  - `names`: List of stock names.
  - `recent_trading_day`: The most recent trading day in `YYYYMMDD` format.
- **Returns:** A `DataFrame` containing data for all stocks.

------

### **5. Left-Side Trading Stock Selection Strategy**

The **Left-Side Trading Strategy** identifies buy opportunities in the Chinese A-share market based on predefined conditions. This strategy is flexible, allowing users to apply individual strategies (e.g., Bollinger Band, KDJ) or a combined strategy.

#### **5.1 Predefined Conditions**

1. **Condition 1 (Bollinger Band):** The closing price is lower than the lower Bollinger Band.
2. **Condition 2 (KDJ Crossover):** The K value is about to cross the D value (difference < 5), and for the last three days, the K value has consistently been below the D value.
3. **Condition 3 (Turnover Rate):** The turnover rate is between 2.5% and 17%.
4. **Condition 4 (Transaction Amount):** The transaction amount is greater than or equal to 70 million.

------

#### **5.2 Implementation Steps**

##### **Step 1: Retrieve and Save Stock Data**

The first step is to retrieve stock data for all A-share stocks using the `DataFetcher` class. Save the data as an Excel file for reuse to avoid redundant API calls and improve efficiency.

```python
from stock_analysis.stock_analysis import DataFetcher

# Initialize DataFetcher
fetcher = DataFetcher()

try:
    # Retrieve the most recent trading day
    recent_trading_day = fetcher.find_recent_trading_day()
    print(f"Most recent trading day: {recent_trading_day}")

    # Retrieve all stock codes and names
    codes, names = fetcher.get_all_stock_codes()
    print(f"Retrieved {len(codes)} stocks")

    # Fetch stock data for all stocks
    data = fetcher.get_data_for_all_stocks(codes, names, recent_trading_day)
    print(f"Retrieved data for {len(data)} stocks")

    # Save the data for reuse
    raw_data_file = f"All_Stocks_{recent_trading_day}.xlsx"
    data.to_excel(raw_data_file, index=False)
    print(f"All stock data saved to {raw_data_file}")
finally:
    # Log out of BaoStock
    fetcher.logout()
```

##### **Step 2: Apply a Single Strategy**

Once the data is retrieved and saved, you can load it and apply a specific strategy. Each strategy is implemented as a class with a static `apply` method in the `Strategy` module.

###### **Example: Apply Bollinger Band Strategy**

```python
import pandas as pd
from Strategy.bollinger_strategy import BollingerStrategy

# Load the previously saved data
input_file = "All_Stocks_20241227.xlsx"  # Replace with your file name
df = pd.read_excel(input_file)

# Apply the Bollinger Band strategy
bollinger_signal = BollingerStrategy.apply(df)
filtered_data = df[bollinger_signal]
print(f"Selected {len(filtered_data)} stocks based on Bollinger Band strategy")

# Save the filtered results
output_file = "Filtered_Stocks_Bollinger_20241227.xlsx"
filtered_data.to_excel(output_file, index=False)
print(f"Filtered data saved to {output_file}")
```

###### **Example: Apply Turnover Strategy**

```python
from Strategy.turnover_strategy import TurnoverStrategy

# Apply the Turnover strategy
turnover_signal = TurnoverStrategy.apply(df)
filtered_data = df[turnover_signal]
print(f"Selected {len(filtered_data)} stocks based on Turnover strategy")

# Save the filtered results
output_file = "Filtered_Stocks_Turnover_20241227.xlsx"
filtered_data.to_excel(output_file, index=False)
print(f"Filtered data saved to {output_file}")
```

------

##### **Step 3: Apply All Strategies (Combined)**

To apply all strategies simultaneously, use the `CombinedStrategy` class. This class integrates the logic of all individual strategies.

```python
from Strategy.combined_strategy import CombinedStrategy

# Apply the combined strategy
combined_signal = CombinedStrategy.apply(df)
filtered_data = df[combined_signal]
print(f"Selected {len(filtered_data)} stocks based on the combined strategy")

# Save the filtered results
output_file = "Filtered_Stocks_Combined_20241227.xlsx"
filtered_data.to_excel(output_file, index=False)
print(f"Filtered data saved to {output_file}")
```

------

#### **5.3 Modular Strategy Design**

The `Strategy` module includes the following files and classes:

1. **`bollinger_strategy.py`:**
   - **Class:** `BollingerStrategy`
   - **Method:** `apply(df)`
   - **Logic:** Closing price is lower than the lower Bollinger Band.
2. **`kdj_strategy.py`:**
   - **Class:** `KDJStrategy`
   - **Method:** `apply(df)`
   - **Logic:** K value is about to cross D value (difference < 5), and for the last three days, the K value has been below D value.
3. **`turnover_strategy.py`:**
   - **Class:** `TurnoverStrategy`
   - **Method:** `apply(df)`
   - **Logic:** Turnover rate is between 2.5% and 17%, and transaction amount is >= 70 million.
4. **`combined_strategy.py`:**
   - **Class:** `CombinedStrategy`
   - **Method:** `apply(df)`
   - **Logic:** Combines all three strategies. A stock must satisfy all conditions to be selected.

The `__init__.py` file exports all strategies for simplified imports:

```python
from .bollinger_strategy import BollingerStrategy
from .kdj_strategy import KDJStrategy
from .turnover_strategy import TurnoverStrategy
from .combined_strategy import CombinedStrategy

__all__ = [
    "BollingerStrategy",
    "KDJStrategy",
    "TurnoverStrategy",
    "CombinedStrategy",
]
```

------

#### **5.4 Why Save Data First?**

1. **Efficiency:** Fetching all stock data once avoids redundant API calls, saving time and reducing resource usage.
2. **Reusability:** Saved data can be reused for testing various strategies or adjusting parameters.
3. **Scalability:** This workflow supports batch processing for large datasets, ensuring scalability for extensive analysis.

