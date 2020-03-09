import datetime, json, pika, random, time

## Define a sendReadings function to send data to RabbitMQ Broker
def sendReadings(beginningTime = None, measurements = None, endTime = None, intervalSeconds = None): 
  ## Overwrite measurements value if beginningTime and endTime are given
  if endTime:
    measurements = (endTime - beginningTime).seconds // intervalSeconds

  ## Connect to broker and declare queue
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = connection.channel()
  channel.queue_declare(queue='meter')
  
  ## Send each measurement as a simulated value at each time step
  for measurement_num in range(measurements):
    second_delta = intervalSeconds * measurement_num
    measurement_time = beginningTime + datetime.timedelta(seconds = second_delta)

    body = {}
    body['timestamp'] = measurement_time.timestamp()
    body['meter (Watts)'] = random.random()*9000

    channel.basic_publish(exchange='', routing_key='meter', body=json.dumps(body))
    print(f' [x] Sent {body}')

  ## Send final message declaring end of simulation
  channel.basic_publish(exchange='', routing_key='meter', body=json.dumps({'terminate':True}))
  connection.close()

