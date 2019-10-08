import sys
  
import time
import json
import boto3
import lazyreader
#import helpers
from kafka.producer import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
while True:

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='nyctaxi-trip-data',
                        Key="{}/{}".format('test_data','test1.txt'))

    for line in lazyreader.lazyread(obj['Body'], delimiter='\n'):

        #message_info = line.strip()
        #msg = helpers.map_schema(message_info, self.schema)
#        data = {'number' : line}

        producer.send('test',value=line)

        time.sleep(0.1)
