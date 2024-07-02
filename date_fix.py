from datetime import datetime

formats = [
    "%m/%d/%Y, %H:%M",
    "%d/%m/%Y %H:%M",
    "%d/%m/%y %H:%M",
    "%A, %d-%b-%y %H:%M:%S",
    "%m/%d/%y %H:%M",
    "%m/%d/%Y, %I:%M %p",
    "%d/%m/%Y %I:%M %p",
    "%d/%m/%y %I:%M %p",
    "%A, %d-%b-%y %I:%M:%S %p",
    "%m/%d/%y %I:%M %p"
]


def detect_format(date_str):
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)

            formats.remove(fmt)
            formats.insert(0, fmt)
            return fmt
        except ValueError:
            continue
    return None


def format_find(dates):
    for date in dates:
        fmt = detect_format(date)

    return fmt
