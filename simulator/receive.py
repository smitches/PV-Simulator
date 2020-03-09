import json, pika, datetime
from pv_value_simulator import pv_kw_power_curve_value as generate_pv_value

## Create connection to local broker and create channel with listening to 'meter' queue
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='meter')

## Keep list of powerValues to output to file
powerValues = []

## Define callback method for handling messages
def received_meter_reading(ch, method, properties, body):
  print(f" [x] Received {body}")

  ## Parse body from json into dictionary
  body = json.loads(body)

  ## End callback and listening upon 'terminate' message and output file
  if 'terminate' in body.keys():
    ch.stop_consuming()
    with open('data.txt', 'w') as outfile:
      json.dump(powerValues, outfile, indent=2, separators=(',', ': '))
      output = json.dumps(powerValues,indent=2, separators=(',', ': '))
      print(f"\nSaving\n{output}\nto 'data.txt'")
    return

  ## Calculate what time of day the meter reading is from
  meter_time = datetime.datetime.fromtimestamp(body['timestamp'])
  midnight  = meter_time.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
  sec_of_day = (meter_time - midnight).seconds

  ## Generate simulated photovoltaic power value at this time of day
  current_pv_value_kw = generate_pv_value(sec_of_day)

  ## Read meter power value and calculate sum of power values
  meter_watts = body['meter (Watts)']
  sum_of_watts = meter_watts + current_pv_value_kw * 1000

  ## Make a record of this simulated reading with additional info
  record = {
              'timestamp':meter_time.timestamp(),
              'meter power value (Watts)':meter_watts,
              'simulated pv power value (kW)': current_pv_value_kw,
              'sum of power values (Watts)': sum_of_watts
           }

  ## Store record in list to be saved in output file at later point
  powerValues.append(record)




channel.basic_consume(queue='meter',
                      on_message_callback=received_meter_reading,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
