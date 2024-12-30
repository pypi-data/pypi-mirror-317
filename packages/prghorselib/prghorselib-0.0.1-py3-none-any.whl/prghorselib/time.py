from datetime import datetime
import time

class TimestampUtils:
    async def get_unix_timestamp(self) -> int:
        return int(time.time())

    async def get_formatted_timestamp(self) -> str:
        now = datetime.now()
        return now.strftime('%H:%M:%S %d:%m:%Y')
