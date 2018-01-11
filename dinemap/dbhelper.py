import datetime
import dbconfig
import pymysql

class DBHelper:

    def connect(self, database="dinemap"):
        return pymysql.connect(host='localhost',user=dbconfig.db_user,passwd=dbconfig.db_password,db=database)


    def get_all_diningEvents(self):
        connection = self.connect()
        try:
            query = "SELECT latitude, longitude, date, category, description FROM diningEvents;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            named_diningEvents = []
            for diningEvent in cursor:
                named_diningEvent = {
                    'latitude': diningEvent[0],
                    'longitude': diningEvent[1],
                    'date': datetime.datetime.strftime(diningEvent[2], '%Y-%m-%d'),
                    'category': diningEvent[3],
                    'description': diningEvent[4]
                }
                named_diningEvents.append(named_diningEvent)
            return named_diningEvents

        except Exception as e:
            print(e)

        finally:
            connection.close()

    def add_diningEvent(self, category, date, latitude, longitude,
            description):
        connection = self.connect()
        try:
            query = ("INSERT INTO diningEvents (category, date, latitude," + 
                "longitude, description) VALUES (%s, %s, %s, %s, %s);")
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longitude,description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

