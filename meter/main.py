import datetime
from send import sendReadings

def getTime(hh_mm_ss):
  if not hh_mm_ss:
    return None

  hh, mm, ss = map(int,hh_mm_ss.split(':'))
  return datetime.datetime.now().replace(hour = hh, minute = mm, second = ss, microsecond = 0)


def main():
  import sys

  args = sys.argv[1:]
  argDict = {k:v for k,v in map(lambda x: x.split('='), args)}

  params = {}
  params['beginningTime']   = getTime(argDict.get('beg', '12:00:00'))
  params['endTime']         = getTime(argDict.get('end'))
  params['measurements']    = int(argDict.get('num','10'))
  params['intervalSeconds'] = int(argDict.get('int', '5'))

  sendReadings(**params)

if __name__ == '__main__':
  main()
