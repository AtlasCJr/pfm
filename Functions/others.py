from datetime import datetime

def getDate() -> str:
    date = datetime.now()
    day = date.day

    if 11 <= day <= 13:
        suffix = 'th'
    last_digit = day % 10
    if last_digit == 1:
        suffix = 'st'
    elif last_digit == 2:
        suffix = 'nd'
    elif last_digit == 3:
        suffix = 'rd'
    else:
        suffix = 'th'
    
    formatted_date = date.strftime(f"%A, %B {day}{suffix} %Y")

    return formatted_date