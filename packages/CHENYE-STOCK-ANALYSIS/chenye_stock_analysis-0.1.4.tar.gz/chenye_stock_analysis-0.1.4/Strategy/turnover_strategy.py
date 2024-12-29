class TurnoverStrategy:
    """
    Implements the turnover and amount strategy:
    - Buy signal: turnover rate is between 2.5% and 17%, and the amount is >= 70 million.
    """
    @staticmethod
    def apply(df):
        """
        Apply the turnover and amount strategy to the data.

        :param df: pandas DataFrame with '换手率' and '成交额' columns.
        :return: pandas Series with Boolean buy signals.
        """
        return (df['换手率'].between(2.5, 17)) & (df['成交额'] >= 70000000)
