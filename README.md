# Overview

In this project the taxi trip event data are streamed and processed to detect fatigue driving behavior among 
taxi drivers. The data pipeline is built using a Kafka only platform to simply the architecture down from
adding another stream processing framework, such as Spark or Flink. 

# Raw data 
The taxi trip event data are from City of Chicago https://data.cityofchicago.org/widgets/wrvz-psew, downloaded 
to Amazon S3 using wget https://data.cityofchicago.org/api/views/wrvz-psew/rows.csv. 

# Ingestion
KafkaProducer available in kafka-pyhon is used to write data to the kafka topic.The raw data are cleaned and reorganized 
to reduce data size and match format requirment for the streaming process. 

# Streaming 
The data is streamed and processed using KSQL,  a querying engine built on top of Kafka Streams. The real time events are simulated by reading the timestamps of each trip event. 
During the streaming process the total driving time of two hours of aggregation window is calculated for each driver. The aggregation window is a hoping window with an advanced step of 15 minutes. 
The fatigue driving criteria is that the resting time within two hours is less than 15 minutes. Once the criteria is met the driver ID is output into a table for any query during the application. 


# Web UI
The Web UI is built using Dash. The total driving time for each driver and the fatigue driver ID were read directly from topic. 
