# Import package and depedencies
import re

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create spark session
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Analysis StackOverflow's User Behavior") \
    .config('job.local.dir', 'file:/opt/spark/process-data/output/_temporary/0/_temporary') \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
    .config('spark.mongodb.input.uri', 'mongodb://mongodb-container/DEP303_ASM2') \
    .config('spark.mongodb.output.uri', 'mongodb://mongodb-container/DEP303_ASM2') \
    .getOrCreate()

print("-------------------------------------")
print("Read Data from Answers collection")

# Configure MongoDB connection settings
mongo_uri      = "mongodb://mongodb-container"
mongo_database = "DEP303_ASM2"
q_collection   = "Questions"
a_collection   = "Answers"

# Read data from MongoDB
answers_df = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", f"{mongo_uri}/{mongo_database}.{a_collection}") \
    .load() \
    .drop("_id")

"""
answers_df = spark.read \
.format("com.mongodb.spark.sql.DefaultSource") \
.option("uri", "mongodb://mongodb-container/DEP303_ASM2.Answers") \
.load() \
.drop("_id")
"""

answers_df.printSchema()

print("Standardize Answers collection Schema")
answers_standardized_df = answers_df \
    .withColumn("CreationDate", to_date(regexp_extract(col("CreationDate"), r"([0-9-]+)T", 1), "yyyy-MM-dd")) \
    .withColumn("OwnerUserId", col("OwnerUserId").cast(IntegerType()))
answers_standardized_df.printSchema()


#====================================================================
# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 mongodb_to_csv.py
# /opt/spark/bin/spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 /opt/spark-apps/mongodb_to_csv.py
"""
/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
--packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
--driver-memory 1G \
--executor-memory 1G \
/opt/spark-apps/mongodb_to_csv.py
"""

# ------------------------------------------
# Calculate how many answers each question has
# ------------------------------------------

summary_questions_df = answers_standardized_df \
    .withColumn("Id", col("ParentId")) \
    .groupBy("Id") \
    .agg(count(col("*")).alias("Number of answers")) \
    .orderBy(col("Id").asc())
    #.filter(col("Id") != "") \
summary_questions_df.show()

# Import Summary questions dataframe direct to Mongodb
""" summary_questions_df.write.format("com.mongodb.spark.sql.DefaultSource") \
    .mode("overwrite") \
    .option("database", "DEP303_ASM2") \
    .option("collection", "Results") \
    .save() """

# Write the transformed data to a CSV file
output_path = "/opt/airflow-data/output"
summary_questions_df.coalesce(1).write.mode("overwrite").csv(output_path, header=True)

# Stop the Spark session
spark.stop()