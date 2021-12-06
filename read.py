#!/usr/bin/python3

import smbus2
import bme280
import os
import time
import requests
import sys

location = 'kitchen'

supabase_host = os.getenv("SUPABASE_HOST")
supabase_key = os.getenv("SUPABASE_API_KEY")

if supabase_host == None:
  print("SUPABASE_HOST is a required environment variable, values should be of the form 'aaabbb.supabase.co'")
  exit(-1)

if supabase_key == None:
  print("SUPABASE_API_KEY is a required environment variable, values are JWTs that begin 'eyJhb'")
  exit(-1)

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

while True:
  try:
    data = bme280.sample(bus, address, calibration_params)

    r = requests.post(f'https://{supabase_host}/rest/v1/readings',
       json={
        "location": location,
        "created_at": data.timestamp.isoformat(),
        "temperature": data.temperature,
        "humidity": data.humidity,
        "pressure": data.pressure
       },
       headers={
         "apikey": supabase_key,
         "Authorization": "Bearer " + supabase_key,
         "Content-Type": "application/json",
         "Prefer": "return=representation"
       })

    print(f'{data.timestamp.isoformat()}: {data.temperature:.2f} °C | {r.status_code}')

    time.sleep(10)
  except KeyboardInterrupt:
    print('\nExiting.')
    sys.exit(0)
  except BaseException as err:
    print(f'Unexpected {err},  {type(err)}')
