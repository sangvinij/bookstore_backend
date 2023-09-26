from datetime import datetime, timedelta

VERIFICATION_CODE_TTL = datetime.utcnow() + timedelta(minutes=30)
