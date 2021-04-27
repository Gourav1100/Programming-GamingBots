from datetime import datetime
import pytz
def retime():
  time=(datetime.now(pytz.timezone("Asia/Calcutta"))).strftime("%H:%M:%S")
  return time