import cx_Oracle
connection = None
class ConnectionManage:
    def getConnection(self):
        try: 
            connection =  cx_Oracle.connect('dhcnhn/dhcnhn@localhost:1521/db12c')    
        except cx_Oracle.DatabaseError as e: 
            print("There is a problem with Oracle", e)
        return connection