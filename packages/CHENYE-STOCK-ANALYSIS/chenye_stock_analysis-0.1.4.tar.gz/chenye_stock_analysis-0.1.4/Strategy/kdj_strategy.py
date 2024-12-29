class KDJStrategy:
    """
    Implements the KDJ strategy:
    - Buy signal: K value is about to cross D value (K is slightly below D),
      and for the past 3 days, K was consistently below D.
    """
    @staticmethod
    def apply(df):
        """
        Apply the KDJ strategy to the data.

        :param df: pandas DataFrame with 'K值' and 'D值' columns.
        :return: pandas Series with Boolean buy signals.
        """
        return (
            (df['K值'] < df['D值']) & 
            (df['D值'] - df['K值'] < 5) & 
            (df['K值'].shift(1) < df['D值'].shift(1)) & 
            (df['K值'].shift(2) < df['D值'].shift(2))
        )
