import json, pika, datetime
from pv_value_simulator import pv_kw_power_curve_value as generate_pv_value

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='meter')

meterValues = []

def received_meter_reading(ch, method, properties, body):
  print(f" [x] Received {body}")

  body = json.loads(body)

  if 'terminate' in body.keys():
    ch.stop_consuming()
    with open('data.txt', 'w') as outfile:
      json.dump(meterValues, outfile, indent=2, separators=(',', ': '))
      output = json.dumps(meterValues,indent=2, separators=(',', ': '))
      print(f"\nSaving\n{output}\nto 'data.txt'")
    return

  meter_time = datetime.datetime.fromtimestamp(body['timestamp'])
  midnight  = meter_time.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
  sec_of_day = (meter_time - midnight).seconds

  current_pv_value_kw = generate_pv_value(sec_of_day)

  meter_watts = body['meter (Watts)']

  sum_of_watts = meter_watts + current_pv_value_kw * 1000
  record = {
              'timestamp':meter_time.timestamp(),
              'meter power value (Watts)':meter_watts,
              'simulated pv power value (kW)': current_pv_value_kw,
              'sum of power values (Watts)': sum_of_watts
           }

  meterValues.append(record)




channel.basic_consume(queue='meter',
                      on_message_callback=received_meter_reading,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
