# start

# Identify the API endpoint that you want to access. This is the URL where the API is hosted and the specific route
# that you need to call to retrieve the data you want.
import opencage.geocoder
import json
import requests
import sqlite3
import datetime


response = requests.get("http://api.open-notify.org/iss-now.json")
r_jason = response.json()

location_list = []
lat = r_jason['iss_position']['latitude']
lon = r_jason['iss_position']['longitude']
time = r_jason['timestamp']
location_list.append((lat, lon, time))

# Initialize the OpenCage geocoder with your API key - Insert your API Key - commented out as no API key
"""geocoder = opencage.geocoder.OpenCageGeocode("YOUR_API_KEY_HERE")

# Reverse geocode the ISS location to get the name of the country
result = geocoder.reverse_geocode(lat, lon)
country = result[0]['components']['country']"""

# placeholder country as no API Key
country = "France"

# create datetime object for time
date_time = datetime.datetime.fromtimestamp(time)

# Print the result
print(f"The ISS is currently over {country} as of {date_time}, latitude: {lat}, longitude: {lon}")


# Connect to the database
db = sqlite3.connect("isslocation.db")
cursor = db.cursor()

#  Insert the data into the database. Depending on the structure of your database and the format of the data you
# retrieved from the API, you may need to transform the data into a specific format or schema before inserting it into
# the database. You can use SQL commands like INSERT to add the data to your database tables.

# Create the table (if it doesn't already exist)
cursor.execute("""
        CREATE TABLE IF NOT EXISTS isslocation (
            country TEXT PRIMARY KEY,
            lat INTEGER NOT NULL,
            lon INTEGER NOT NULL,
            datetime DATETIME
        )""")
db.commit()

# add the info if not already there.
try:
    cursor.execute("""
                   INSERT INTO isslocation (country, lat, lon, datetime)
                   VALUES (?,?,?,?)""", (country, lat, lon, date_time))

    db.commit()
# update the table if info already there
except sqlite3.IntegrityError:
    cursor.execute("""UPDATE isslocation SET country = ?, lat = ?, lon = ?, datetime = ?
    """, (country, lat, lon, date_time))

finally:
    cursor.close()
    db.close()

print("This information has been added to the database")

#End