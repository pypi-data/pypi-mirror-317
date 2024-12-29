class BollingerStrategy:
    """
    Implements the Bollinger Bands strategy:
    - Buy signal: close price is lower than the lower Bollinger Band.
    """
    @staticmethod
    def apply(df):
        """
        Apply the Bollinger Bands strategy to the data.
        
        :param df: pandas DataFrame with 'close' and '布林带下轨' columns.
        :return: pandas Series with Boolean buy signals.
        """
        return df['close'] < df['布林带下轨']