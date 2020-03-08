import datetime, json, pika, random, time

NOON = datetime.datetime.now().replace(hour = 12, minute = 0, second = 0, microsecond = 0)

def sendReadings(beginningTime = NOON, measurements = None, endTime = None, intervalSeconds = 3): 
  if not (measurements or endTime):
    measurements = 10
  elif endTime:
    measurements = (endTime - beginningTime).seconds // intervalSeconds

  connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = connection.channel()

  channel.queue_declare(queue='meter')
  
  for measurement_num in range(measurements):
    second_delta = intervalSeconds * measurement_num
    measurement_time = beginningTime + datetime.timedelta(seconds = second_delta)

    body = {}
    body['timestamp'] = measurement_time.timestamp()
    body['meter (Watts)'] = random.random()*9000

    channel.basic_publish(exchange='', routing_key='meter', body=json.dumps(body))
    print(f' [x] Sent {body}')

  channel.basic_publish(exchange='', routing_key='meter', body=json.dumps({'terminate':True}))
  connection.close()

sendReadings(measurements = 2)
