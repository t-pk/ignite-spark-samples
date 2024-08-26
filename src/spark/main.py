from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import lit

# Setup Spark session

spark = SparkSession.builder \
    .appName("SparkCRUDOperations") \
    .getOrCreate()

# Create DataFrame
data = [
    Row(id=1, name="John Doe", age=30),
    Row(id=2, name="Jane Doe", age=25),
    Row(id=3, name="Mike Smith", age=35)
]
df = spark.createDataFrame(data)

# # Save DataFrame as a table
# df.write.mode("overwrite").saveAsTable("people")

# Read data
people_df = spark.table("people")
people_df.show()

# # Update data
# update_df = people_df.filter(people_df.id == 2).withColumn("name", lit("Jane Smith"))
# remaining_df = people_df.filter(people_df.id != 2)
# updated_df = remaining_df.union(update_df)
# updated_df.write.mode("overwrite").saveAsTable("people")
# spark.table("people").show()

# # Delete data
# remaining_df = people_df.filter(people_df.id != 3)
# remaining_df.write.mode("overwrite").saveAsTable("people")
# spark.table("people").show()

# # Insert data
# new_data = [Row(id=4, name="Alice Johnson", age=28)]
# new_df = spark.createDataFrame(new_data)
# inserted_df = people_df.union(new_df)
# inserted_df.write.mode("overwrite").saveAsTable("people")
# spark.table("people").show()
