from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").master("local").getOrCreate() 

from pyignite import Client

client = Client()
client.connect("localhost", 10800)

CITY_CREATE_TABLE_QUERY = '''CREATE TABLE City (
    ID INT(11),
    Name CHAR(35),
    CountryCode CHAR(3),
    District CHAR(20),
    Population INT(11),
    PRIMARY KEY (ID, CountryCode)
) WITH "affinityKey=CountryCode"'''

client.sql(CITY_CREATE_TABLE_QUERY)

CITY_CREATE_INDEX = "CREATE INDEX idx_country_code ON city (CountryCode)"

client.sql(CITY_CREATE_INDEX)

CITY_INSERT_QUERY = """INSERT INTO City(
    ID, Name, CountryCode, District, Population
) VALUES (?, ?, ?, ?, ?)"""

CITY_DATA = [
    [3793, "New York", "USA", "New York", 8008278],
    [3794, "Los Angeles", "USA", "California", 3694820],
    [3795, "Chicago", "USA", "Illinois", 2896016],
    [3796, "Houston", "USA", "Texas", 1953631],
    [3797, "Philadelphia", "USA", "Pennsylvania", 1517550],
    [3798, "Phoenix", "USA", "Arizona", 1321045],
    [3799, "San Diego", "USA", "California", 1223400],
    [3800, "Dallas", "USA", "Texas", 1188580],
]

for row in CITY_DATA:
    client.sql(CITY_INSERT_QUERY, query_args=row)

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