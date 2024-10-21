from configuration import get_config
from pipeline import DailyInsights


if __name__ == '__main__':
    date = '2024/08/18'
    config = get_config(date)
    DI = DailyInsights(config)
    DI.get_calls_insight()
