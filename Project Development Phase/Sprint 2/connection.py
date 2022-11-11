import ibm_db

dsn_hostname = "98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
dsn_uid = "nqr09770"        # e.g. "abc12345"
dsn_pwd = "Fz5zer4LtepyUXhn"      # e.g. "7dBZ3wWt9XN6$o0J"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"            # e.g. "BLUDB"
dsn_port = "30875"                # e.g. "32733"
dsn_protocol = "TCPIP"            # i.e. "TCPIP"
dsn_security = "SSL"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)

# print the connection string to check correct values are specified
# print(dsn)

try:
    conn = ibm_db.connect(dsn, "", "")
    print("Connected to database: ", dsn_database,
          "as User: ", dsn_uid, "on Host: ", dsn_hostname)

except:
    print("Unable to Connect: ", ibm_db.conn_errormsg())


# server = ibm_db.server_info(conn)
# print("Server Info")
# print("DBMS_NAME: ", server.DBMS_NAME)
# print("DBMS_VER:  ", server.DBMS_VER)
# print("DB_NAME:   ", server.DB_NAME)

# client = ibm_db.client_info(conn)
# print("Client Info")
# print("DRIVER_NAME:          ", client.DRIVER_NAME)
# print("DRIVER_VER:           ", client.DRIVER_VER)
# print("DATA_SOURCE_NAME:     ", client.DATA_SOURCE_NAME)
# print("DRIVER_ODBC_VER:      ", client.DRIVER_ODBC_VER)
# print("ODBC_VER:             ", client.ODBC_VER)
# print("ODBC_SQL_CONFORMANCE: ", client.ODBC_SQL_CONFORMANCE)
# print("APPL_CODEPAGE:        ", client.APPL_CODEPAGE)
# print("CONN_CODEPAGE:        ", client.CONN_CODEPAGE)


# stmt = "insert into creds values(default,'test1','test2','3455','pass');"
# res = ibm_db.execute(ibm_db.prepare(conn, stmt))
# print(res)

# stmt = "select email,pass from creds;"
# res = ibm_db.exec_immediate(conn, stmt)
# print("REs")
# print(res)
# dictionary = ibm_db.fetch_both(res)
# while dictionary != False:
#     print("The ID is : ",  dictionary[0])
#     print("The Name is : ", dictionary[1])
#     dictionary = ibm_db.fetch_both(res)

def plasmaMatchCheck(pbgrp, dbgrp):
    if (dbgrp == "AB+" or dbgrp == "AB-"):
        return True
    elif ((dbgrp == "A+" or dbgrp == "A-") and (pbgrp == "A+" or pbgrp == "A-" or pbgrp == "O+" or pbgrp == "O-")):
        return True
    elif ((dbgrp == "B+" or dbgrp == "B-") and (pbgrp == "B+" or pbgrp == "B-" or pbgrp == "O+" or pbgrp == "O-")):
        return True
    elif ((dbgrp == "O+" or dbgrp == "O-") and (pbgrp == "O+" or pbgrp == "O-")):
        return True
    else:
        return False
