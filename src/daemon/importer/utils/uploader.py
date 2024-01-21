import psycopg2

USER = "is"
PASSWORD = "is"
HOST = "db-xml"
PORT = "10001"
DBNAME = "is"

connection = None
cursor = None

def upload_file_to_db(name: str, data: str) -> bool:
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      dbname=DBNAME)

        cursor = connection.cursor()
        higienized = data.replace("'", "&apos;")
        cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)", (name, higienized))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to fetch data with {error}")
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Inserted document into database")
            return True

def get_documents_from_db():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      dbname=DBNAME)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM imported_documents")
        documents = cursor.fetchall()
        return documents

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to fetch data with {error}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Fetched documents from database")
            return documents

def set_document_as_converted(src, file_size, dst) -> bool:
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      dbname=DBNAME)

        cursor = connection.cursor()
        cursor.execute("INSERT INTO converted_documents (src, file_size, dst) VALUES (%s, %s, %s)", (src, file_size, dst))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to fetch data with {error}")
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Inserted document into database")
            return True

def get_documents_from_converted_documents():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      dbname=DBNAME)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM converted_documents")
        documents = cursor.fetchall()
        return documents

    except (Exception, psycopg2.Error) as error:
        print(f"Failed to fetch data with {error}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Fetched documents from database")
            return documents