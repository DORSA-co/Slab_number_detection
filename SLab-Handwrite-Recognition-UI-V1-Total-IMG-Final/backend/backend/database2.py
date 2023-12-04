from numpy import rec
import sqlite3

# from tenacity import retry_if_exception


TABELS_NAME = {
    "coils_info": "images",
}

CONNECTION_ERROR = "Connection error"
SUCCESSFULL = "True"


class dataBase:
    def __init__(self):
        pass

    def create_connection(self):
        self.conn = sqlite3.connect("database2.db")

        self.cur = self.conn.cursor()

        # self.sql_command = """CREATE TABLE Camera(Serial Number INTEGER PRIMARY KEY, Height INTEGER, Width INTEGER , Gain INTEGER, Exposure INTEGER, offsetX INTEGER, offsetY INTEGER  )"""
        # self.cur.execute(self.sql_command)

        # self.conn.commit()
        # self.conn.close()

        return self.conn, self.cur

    def insert(self):
        self.conn = sqlite3.connect("database2.db")
        self.cur = self.conn.cursor()
        self.sql_command = """INSERT INTO camera VALUES(24,23,24,26,27,30,31)"""
        self.cur.execute(self.sql_command)
        self.conn.commit()
        self.conn.close()
        # return self.conn, self.cur

    def show_row(self):
        self.conn = sqlite3.connect("database2.db")
        self.cur = self.conn.cursor()
        self.cur.execute("select * from {}".format("camera"))
        records = self.cur.fetchall()
        print("records")
        print(records)

        field_names = [col[0] for col in self.cur.description]
        res = []

        # connection.close()
        self.cur.close()
        # print("MySQL connection is closed")

        for record in records:
            record_dict = {}
            for i in range(len(field_names)):
                record_dict[field_names[i]] = record[i]
            res.append(record_dict)
        print(res)

        self.conn.close()
        # return self.conn, self.cur

    def load_parms(self, table_name):
        self.create_connection()
        self.cur.execute("select * from {}".format("Camera"))
        records = self.cur.fetchall()

        field_names = [col[0] for col in self.cur.description]
        res = []

        # connection.close()
        self.cur.close()
        # print("MySQL connection is closed")

        for record in records:
            record_dict = {}
            for i in range(len(field_names)):
                record_dict[field_names[i]] = record[i]
            res.append(record_dict)
        print(res)
        return res[0]

    def update_record(self, table_name, col_name, value, id_name, id_value):
        connection, cursor = self.create_connection()
        print("id_value", table_name, col_name, value, id_name, id_value)
        mySql_insert_query = """UPDATE {} 
                                SET {} = {}
                                WHERE {} ={} """.format(
            table_name, col_name, ("'" + value + "'"), id_name, ("'" + id_value + "'")
        )
        # print(mySql_insert_query)
        cursor.execute(mySql_insert_query)
        # mySql_insert_query=(mySql_insert_query,data)
        # self.execute_quary(mySql_insert_query, cursor, connection, close=False,need_data=True )
        connection.commit()
        print(cursor.rowcount, "Record Updated successfully ")
        cursor.close()
        return True

    def update_camera_parms(self, table_name, id_number, parms):
        for col in parms.keys():
            self.update_record(
                str(table_name), str(col), str(parms[col]), "id", str(id_number)
            )


if __name__ == "__main__":
    db = dataBase()
    # db.create_connection()
    # db.insert()
    # db.show_row()
    # db.load_parms("cameras")
    # db.update_record('defect', 'no', '50', 'name', '1')
    # parms = {"gain": 20, "exposure": 10}
    # db.update_camera_parms(0, parms)
