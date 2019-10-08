CREATE STREAM stream_taxi
  (trip_id STRING,taxi_id STRING,trip_start STRING, trip_end STRING, trip_time INT)
  WITH (KAFKA_TOPIC='topic_fatigue',
        VALUE_FORMAT='DELIMITED',
        KEY='taxi_id',
        TIMESTAMP='trip_start',
        TIMESTAMP_FORMAT='yyyy-MM-dd-HH:mm');

CREATE TABLE table_aggre_sum AS
  SELECT taxi_id,
        SUM(trip_time) AS trip_time_total
  FROM stream_taxi
  WINDOW HOPPING (SIZE 2 hours, ADVANCE BY 15 minutes)
  GROUP BY taxi_id;

CREATE TABLE fatigue_drivers AS
  SELECT taxi_id, trip_time_total
  FROM table_aggre_sum
  WHERE trip_time_total > 5400;
