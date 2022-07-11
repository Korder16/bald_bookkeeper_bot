from datetime import datetime, time

def get_diff_working_hours(username: str):
    
    stop_working = {
        'islamtramov': 18,
        'TikhonovD': 18,
        'rash708': 18,
        'NSIbragim': 19,
        'misha1234555': 19
    }
    
    
    if username == 'NikoGasanov':
        message = 'отдохни от доты, брат, не сегодня'
    else:
        now = datetime.now()
        stop = datetime.now().replace(hour=stop_working[username], minute=0, second=0)
        if now.time() < time(stop_working[username] - 9, 00, 00) or now.time() > time(stop_working[username], 00, 00):
            message = 'леее, куда прёшь, пора отдыхать'
        else:
            diff = stop - now
            diff_without_ms = str(diff).split(".")[0]
            message = f'до конца рабочего дня осталось: {diff_without_ms}'
    return message


def is_rashid_relaxing():
    now = datetime.now().time()
    return (now < time(9, 00, 00) or now > time(18, 00, 00))
