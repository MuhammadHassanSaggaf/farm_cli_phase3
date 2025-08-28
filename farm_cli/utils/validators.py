from datetime import datetime

def parse_date(s):
    if not s:
        return None
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError('Date must be in YYYY-MM-DD or DD-MM-YYYY format')

def to_float(s, field_name='value'):
    try:
        return float(s)
    except Exception:
        raise ValueError(f'{field_name} must be a number')
