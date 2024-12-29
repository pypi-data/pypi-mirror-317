from .bollinger_strategy import BollingerStrategy
from .kdj_strategy import KDJStrategy
from .turnover_strategy import TurnoverStrategy

class CombinedStrategy:
    """
    Combines multiple strategies (Bollinger Bands, KDJ, and Turnover).
    """
    @staticmethod
    def apply(df):
        """
        Apply all strategies and combine the results.

        :param df: pandas DataFrame with necessary columns for all strategies.
        :return: pandas Series with combined Boolean buy signals.
        """
        bollinger_signal = BollingerStrategy.apply(df)
        kdj_signal = KDJStrategy.apply(df)
        turnover_signal = TurnoverStrategy.apply(df)

        # Combine signals: All conditions must be met
        return bollinger_signal & kdj_signal & turnover_signal
