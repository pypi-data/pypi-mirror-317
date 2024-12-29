import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
from IPython.display import display, clear_output


class DataFetcher:
    def __init__(self):
        """
        Initialize and log in to BaoStock.
        """
        self.lg = bs.login()
        if self.lg.error_code != '0':
            raise Exception(f"Login failed: {self.lg.error_msg}")
        print("BaoStock login successful!")

    @staticmethod
    def find_recent_trading_day():
        """
        Find the most recent trading day by querying the 'sh.000001' index.
        Returns:
            str: The most recent trading day in 'YYYYMMDD' format.
        """
        current_date = datetime.now().date()
        while True:
            date_str = current_date.strftime('%Y-%m-%d')
            rs = bs.query_history_k_data_plus(
                "sh.000001",
                "date,open,high,low,close",
                start_date=date_str,
                end_date=date_str,
                frequency="d",
                adjustflag="2"
            )
            data_list = []
            while rs.next():
                data_list.append(rs.get_row_data())
            if len(data_list) > 0:
                return current_date.strftime('%Y%m%d')
            current_date -= timedelta(days=1)

    @staticmethod
    def get_all_stock_codes():
        """
        Get all A-share stock codes, excluding ST, Sci-tech board, and Beijing Exchange stocks.
        Returns:
            list, list: Lists of stock codes and stock names.
        """
        rs = bs.query_stock_basic()
        data_list = []
        if rs.error_code != '0':
            raise Exception(f"Error fetching stock codes: {rs.error_msg}")
        while rs.next():
            data_list.append(rs.get_row_data())

        stock_df = pd.DataFrame(data_list, columns=rs.fields)

        # Filter stocks
        stock_df = stock_df[~stock_df['code_name'].str.contains('ST', na=False)]
        stock_df = stock_df[~stock_df['code'].str.startswith('sh.688')]
        stock_df = stock_df[~stock_df['code'].str.startswith('bj.')]
        stock_df = stock_df[stock_df['type'] == '1']

        return stock_df['code'].tolist(), stock_df['code_name'].tolist()

    @staticmethod
    def fetch_stock_data(code, start_date, end_date):
        """
        Fetch historical K-line data for a stock within the given date range.
        """
        fields = "date,code,open,high,low,close,volume,amount,turn"
        rs = bs.query_history_k_data_plus(
            code, fields,
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="2"
        )
        data_list = []
        if rs.error_code != '0':
            print(f"Failed to fetch data for {code}: {rs.error_msg}")
            return pd.DataFrame()
        while rs.next():
            data_list.append(rs.get_row_data())

        df = pd.DataFrame(data_list, columns=rs.fields)
        for col in ["open", "high", "low", "close", "volume", "amount", "turn"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    @staticmethod
    def compute_bollinger_bands(df, period=20, multiplier=2):
        """
        Compute Bollinger Bands (middle, upper, and lower bands) for the given DataFrame.
        """
        if len(df) < period:
            return df

        df['布林带中轨'] = df['close'].rolling(window=period, min_periods=period).mean()
        df['STD'] = df['close'].rolling(window=period, min_periods=period).std()
        df['布林带上轨'] = df['布林带中轨'] + multiplier * df['STD']
        df['布林带下轨'] = df['布林带中轨'] - multiplier * df['STD']
        return df

    @staticmethod
    def compute_kdj(df, n=7, m1=3, m2=3):
        """
        Compute KDJ (K, D, J) indicators for the given DataFrame.
        """
        if len(df) < n:
            return df

        df['Low_Min'] = df['low'].rolling(window=n, min_periods=n).min()
        df['High_Max'] = df['high'].rolling(window=n, min_periods=n).max()
        df['RSV'] = (df['close'] - df['Low_Min']) / (df['High_Max'] - df['Low_Min']) * 100
        df['K值'] = df['RSV'].ewm(alpha=1/m1, adjust=False).mean()
        df['D值'] = df['K值'].ewm(alpha=1/m2, adjust=False).mean()
        df['J值'] = 3 * df['K值'] - 2 * df['D值']
        return df

    @staticmethod
    def build_stock_record(df, code, name, check_date):
        """
        Build a single record (dictionary) for a specific stock on a specific date.
        """
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        target_dt = datetime.strptime(check_date, '%Y%m%d')
        row_today = df[df['date'] == target_dt]
        if row_today.empty:
            return None
        row_today = row_today.iloc[0]
        return {
            "股票代码": code.replace('sh.', '').replace('sz.', ''),
            "股票名称": name,
            "日期": row_today['date'].strftime('%Y-%m-%d'),
            "收盘价": row_today['close'],
            "最低价": row_today['low'],
            "布林带下轨": row_today.get('布林带下轨', None),
            "布林带中轨": row_today.get('布林带中轨', None),
            "布林带上轨": row_today.get('布林带上轨', None),
            "K值": row_today.get('K值', None),
            "D值": row_today.get('D值', None),
            "J值": row_today.get('J值', None),
            "换手率": row_today['turn'],
            "成交额": row_today['amount']
        }

    def get_data_for_all_stocks(self, codes, names, recent_trading_day):
        """
        Fetch data, compute Bollinger Bands and KDJ for all stocks.
        """
        start_date = (datetime.strptime(recent_trading_day, '%Y%m%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        end_date = datetime.strptime(recent_trading_day, '%Y%m%d').strftime('%Y-%m-%d')

        all_data = pd.DataFrame(columns=[
            "股票代码", "股票名称", "日期", "收盘价", "最低价",
            "布林带下轨", "布林带中轨", "布林带上轨",
            "K值", "D值", "J值",
            "换手率", "成交额"
        ])

        for idx, (code, name) in enumerate(zip(codes, names), start=1):
            print(f"Processing {idx}/{len(codes)}: {code} - {name}")
            try:
                df_raw = self.fetch_stock_data(code, start_date, end_date)
                if df_raw.empty:
                    print(f"No data for {code} - {name}")
                    continue

                df_bbands = self.compute_bollinger_bands(df_raw.copy())
                df_kdj = self.compute_kdj(df_bbands)
                record = self.build_stock_record(df_kdj, code, name, recent_trading_day)
                if record:
                    all_data = pd.concat([all_data, pd.DataFrame([record])], ignore_index=True)
                    clear_output(wait=True)
                    display(all_data)
            except Exception as e:
                print(f"Error processing {code} - {name}: {e}")
                continue

        return all_data

    def logout(self):
        """
        Log out of BaoStock.
        """
        bs.logout()
        print("Logged out of BaoStock!")