import sys
import time
import boto3
import csv
import pandas as pd
from smart_open import open
from kafka.producer import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
while True:

     with open ('s3://nyctaxi-trip-data/taxi_chicago.csv',encoding='utf8') as s3_taxi_data:
        read_taxi=csv.reader(s3_taxi_data,delimiter=',')
        next(read_taxi,None)
        for line in read_taxi:         
            # data cleanup; to reduce the string length of taxi id 
            key_string = line[1][:10]

            line_string =''

            # to skip invalid data            
            if not line[0] or not line[1] or not line[2] or not line[3] or not line[4]:
                continue
            for i in range(5):
                if i == 0 or i ==1:
                    line[i]=line[i][:10]
             # to change the time format to be recoganized in KSQL
                if i == 2 or i == 3:
                    line[i] = pd.to_datetime(line[i])
                    line[i]=line[i].strftime("%Y-%m-%d-%H:%M")
                if i == (4):
                    delimiter = ''
                else:
                    delimiter = ','
                line_string=line_string+''.join(line[i])+delimiter
            print (key_string)
            print (line_string)
            producer.send('topic_fatigue',value=line_string,key=key_string)
          # optional; to control ingestion rate
          # time.sleep(1) 
