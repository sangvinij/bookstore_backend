from datetime import timedelta, datetime

VERIFICATION_CODE_TTL = datetime.utcnow() + timedelta(minutes=30)