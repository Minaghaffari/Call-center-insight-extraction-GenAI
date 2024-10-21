import sys
from configuration import get_config
from pipeline import DailyInsights


if __name__ == '__main__':
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        print(
            "Error: Please provide a date as an argument. Usage: python main.py YYYY/MM/DD")
        sys.exit(1)
    # date = '2024/08/18'
    config = get_config(date)
    DI = DailyInsights(config)
    DI.get_calls_insight()
