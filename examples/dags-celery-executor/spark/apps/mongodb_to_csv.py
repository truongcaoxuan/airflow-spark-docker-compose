# Import package and depedencies
import re

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

#from daria.write import DariaWriters
#import com.github.mrpowers.spark.daria.sql.DariaWriters

# Create spark session
spark = SparkSession.builder \
    .appName("Analysis StackOverflow's User Behavior") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
    .config('spark.mongodb.input.uri', 'mongodb://mongodb-container/DEP303_ASM2') \
    .config('spark.mongodb.output.uri', 'mongodb://mongodb-container/DEP303_ASM2') \
    .getOrCreate()

# Configure MongoDB connection settings
#mongo_uri = "mongodb://mongodb-container:27017"
#mongo_database = "DEP303_ASM2"
#q_collection = "Questions"
#a_collection = "Answers"

# Read data from MongoDB
#df = spark.read.format("com.mongodb.spark.sql.DefaultSource") \
#    .option("uri", f"{mongo_uri}/{mongo_database}.{a_collection}") \
#    .load()

print("-------------------------------------")
print("Read Data from Answers collection")
answers_df = spark.read \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .option("uri", "mongodb://mongodb-container/DEP303_ASM2.Answers") \
    .load() \
    .drop("_id")
answers_df.printSchema()

print("Standardize Answers collection Schema")
answers_standardized_df = answers_df \
    .withColumn("CreationDate", to_date(regexp_extract(col("CreationDate"), r"([0-9-]+)T", 1), "yyyy-MM-dd")) \
    .withColumn("OwnerUserId", col("OwnerUserId").cast(IntegerType()))
answers_standardized_df.printSchema()


#====================================================================
# spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 5_GetQuestionsWithMoreThan5Answers.py

# ------------------------------------------
# Calculate how many answers each question has
# ------------------------------------------

summary_questions_df = answers_standardized_df \
    .withColumn("Id", col("ParentId")) \
    .groupBy("Id") \
    .agg(count(col("*")).alias("Number of answers")) \
    .orderBy(col("Id").asc())

#summary_questions_df.show()

# summary_questions_df.write.format("com.mongodb.spark.sql.DefaultSource") \
    # .mode("overwrite") \
    # .option("database", "DEP303_ASM2") \
    # .option("collection", "Results") \
    # .save()
    
print("-------------------------------------")
print("Save output csv")
# Write the transformed data to a CSV file
#output_path = "/opt/spark-data/output"
output_path = "/opt/spark/process-data/output"
summary_questions_df.coalesce(1).write.mode("overwrite").csv(output_path, header=True)
#summary_questions_df.repartition(1).write.mode("overwrite").csv(output_path, header=True)

# answers_standardized_df \
    # .withColumn("Id", col("ParentId")) \
    # .groupBy("Id") \
    # .agg(count(col("*")).alias("Number of answers")) \
    # .repartition(1).write.mode("overwrite").format("csv").save(output_path,header=True)
    
# Stop the Spark session
spark.stop()