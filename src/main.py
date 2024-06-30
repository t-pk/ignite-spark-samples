from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ignite-spark").master("local").getOrCreate() 

from pyignite import Client

client = Client()
client.connect("localhost", 10800)

CITY_SELECT_QUERY = "SELECT * FROM City"

cities = client.sql(CITY_SELECT_QUERY)
for city in cities:
    print(*city)

# Query Ignite data
query = "SELECT * FROM City"
result = client.sql(query)

# Define DataFrame schema and create DataFrame
columns = ["ID", "Name", "CountryCode", "District", "Population"]
df = spark.createDataFrame(result, columns)

# Show DataFrame
df.show()

# Stop Spark session
spark.stop()

# Disconnect from Ignite
client.close()
