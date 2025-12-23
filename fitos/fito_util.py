from datetime import datetime, timezone

def get_now_utc():
    utc_now = datetime.now(timezone.utc)
    answer= utc_now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return  answer