Raspberry Pi Thermo
===================
This repo contains the nearly-trivial Python3 script to read a BME280 temperature, pressure and
humidity sensor connected to a Raspberry Pi Zero-WH via I2C and report the results to a Supabase
database.

Bill of Materials
-----------------
1. [Raspberry Pi Zero-WH](https://www.adafruit.com/product/3708), Micro-SD card, and a USB power 
   supply of your choice
2. [BME280](https://www.adafruit.com/product/2652)
3. [Stemma-QT cable](https://www.adafruit.com/product/4397)

Service Dependencies
--------------------
1. [Supabase](https://supabase.com/)

Usage
-----
Configure two environment variables, commonly stored in your profile or rc file, `SUPABASE_API_KEY`
and `SUPABASE_HOST`. The values vor these variables can be found in your Supabase account's API
documentation.

Using `read.py` requires configuring your Supabase database to have a table named `readings`:
```sql
CREATE TABLE IF NOT EXISTS readings (
   created_at timestamp with timezone,
   location varchar(255),
   temperature double precision,
   humidity double precision,
   pressure double precision
);
```

You may find it useful to also create a minutely view over this table:
```sql
CREATE VIEW readings_minutely_avg AS (
  SELECT date_trunc('minute', created_at) as created_at, 
  location, 
  avg(temperature) as temperature,
  avg(humidity) as humidity, 
  avg(pressure) as pressure
  FROM readings
  GROUP BY date_trunc('minute', created_at), location
);
```

After setting up your environment variables and tables you can directly run read.py:
```
./read.py
```
