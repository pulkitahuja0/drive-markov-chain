from datetime import date

# Gives year of most recent COMPLETE NFL szn
def most_recent_nfl_szn():
    today = date.today()

    year = today.year
    month = today.month

    print(today.month)

    if month < 3:
        return year - 2
    return year - 1
