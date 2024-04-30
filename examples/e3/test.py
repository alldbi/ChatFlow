from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import sqlite3
from datetime import date
import os
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

os.environ['OPENAI_API_KEY'] = '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'

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create the "AGENTS" table
    c.execute('''CREATE TABLE IF NOT EXISTS "AGENTS"
                 (
                     "AGENT_CODE" CHAR(6) NOT NULL PRIMARY KEY,
                     "AGENT_NAME" CHAR(40),
                     "WORKING_AREA" CHAR(35),
                     "COMMISSION" DECIMAL(10,2),
                     "PHONE_NO" CHAR(15),
                     "COUNTRY" VARCHAR(25)
                 )''')
    agent_records = [
        ("A007", "Ramasundar", "Bangalore", 0.15, "077-25814763", ""),
        ("A003", "Alex ", "London", 0.13, "075-12458969", ""),
        ("A008", "Alford", "New York", 0.12, "044-25874365", ""),
        ("A011", "Ravi Kumar", "Bangalore", 0.15, "077-45625874", ""),
        ("A010", "Santakumar", "Chennai", 0.14, "007-22388644", ""),
        ("A012", "Lucida", "San Jose", 0.12, "044-52981425", ""),
        ("A005", "Anderson", "Brisban", 0.13, "045-21447739", ""),
        ("A001", "Subbarao", "Bangalore", 0.14, "077-12346674", ""),
        ("A002", "Mukesh", "Mumbai", 0.11, "029-12358964", ""),
        ("A006", "McDen", "London", 0.15, "078-22255588", ""),
        ("A004", "Ivan", "Torento", 0.15, "008-22544166", ""),
        ("A009", "Benjamin", "Hampshair", 0.11, "008-22536178", "")
    ]
    c.executemany("INSERT INTO AGENTS VALUES (?, ?, ?, ?, ?, ?)", agent_records)

    # Create the "CUSTOMER" table
    c.execute('''CREATE TABLE IF NOT EXISTS "CUSTOMER"
                 (
                     "CUST_CODE" VARCHAR(6) NOT NULL PRIMARY KEY,
                     "CUST_NAME" VARCHAR(40) NOT NULL,
                     "CUST_CITY" CHAR(35),
                     "WORKING_AREA" VARCHAR(35) NOT NULL,
                     "CUST_COUNTRY" VARCHAR(20) NOT NULL,
                     "GRADE" INTEGER,
                     "OPENING_AMT" DECIMAL(12,2) NOT NULL,
                     "RECEIVE_AMT" DECIMAL(12,2) NOT NULL,
                     "PAYMENT_AMT" DECIMAL(12,2) NOT NULL,
                     "OUTSTANDING_AMT" DECIMAL(12,2) NOT NULL,
                     "PHONE_NO" VARCHAR(17) NOT NULL,
                     "AGENT_CODE" CHAR(6) NOT NULL,
                     FOREIGN KEY ("AGENT_CODE") REFERENCES "AGENTS"("AGENT_CODE")
                 )''')
    records = [
        ('C00013', 'Holmes', 'London', 'London', 'UK', 2, 6000.00, 5000.00, 7000.00, 4000.00, 'BBBBBBB', 'A003'),
        ('C00001', 'Micheal', 'New York', 'New York', 'USA', 2, 3000.00, 5000.00, 2000.00, 6000.00, 'CCCCCCC', 'A008'),
        ('C00020', 'Albert', 'New York', 'New York', 'USA', 3, 5000.00, 7000.00, 6000.00, 6000.00, 'BBBBSBB', 'A008'),
        ('C00025', 'Ravindran', 'Bangalore', 'Bangalore', 'India', 2, 5000.00, 7000.00, 4000.00, 8000.00, 'AVAVAVA',
         'A011'),
        ('C00024', 'Cook', 'London', 'London', 'UK', 2, 4000.00, 9000.00, 7000.00, 6000.00, 'FSDDSDF', 'A006'),
        ('C00015', 'Stuart', 'London', 'London', 'UK', 1, 6000.00, 8000.00, 3000.00, 11000.00, 'GFSGERS', 'A003'),
        ('C00002', 'Bolt', 'New York', 'New York', 'USA', 3, 5000.00, 7000.00, 9000.00, 3000.00, 'DDNRDRH', 'A008'),
        ('C00018', 'Fleming', 'Brisban', 'Brisban', 'Australia', 2, 7000.00, 7000.00, 9000.00, 5000.00, 'NHBGVFC',
         'A005'),
        (
        'C00021', 'Jacks', 'Brisban', 'Brisban', 'Australia', 1, 7000.00, 7000.00, 7000.00, 7000.00, 'WERTGDF', 'A005'),
        ('C00019', 'Yearannaidu', 'Chennai', 'Chennai', 'India', 1, 8000.00, 7000.00, 7000.00, 8000.00, 'ZZZZBFV',
         'A010'),
        ('C00005', 'Sasikant', 'Mumbai', 'Mumbai', 'India', 1, 7000.00, 11000.00, 7000.00, 11000.00, '147-25896312',
         'A002'),
        ('C00007', 'Ramanathan', 'Chennai', 'Chennai', 'India', 1, 7000.00, 11000.00, 9000.00, 9000.00, 'GHRDWSD',
         'A010'),
        ('C00022', 'Avinash', 'Mumbai', 'Mumbai', 'India', 2, 7000.00, 11000.00, 9000.00, 9000.00, '113-12345678',
         'A002'),
        ('C00004', 'Winston', 'Brisban', 'Brisban', 'Australia', 1, 5000.00, 8000.00, 7000.00, 6000.00, 'AAAAAAA',
         'A005'),
        ('C00023', 'Karl', 'London', 'London', 'UK', 0, 4000.00, 6000.00, 7000.00, 3000.00, 'AAAABAA', 'A006'),
        ('C00006', 'Shilton', 'Torento', 'Torento', 'Canada', 1, 10000.00, 7000.00, 6000.00, 11000.00, 'DDDDDDD',
         'A004'),
        ('C00010', 'Charles', 'Hampshair', 'Hampshair', 'UK', 3, 6000.00, 4000.00, 5000.00, 5000.00, 'MMMMMMM', 'A009'),
        ('C00017', 'Srinivas', 'Bangalore', 'Bangalore', 'India', 2, 8000.00, 4000.00, 3000.00, 9000.00, 'AAAAAAB',
         'A007'),
        ('C00012', 'Steven', 'San Jose', 'San Jose', 'USA', 1, 5000.00, 7000.00, 9000.00, 3000.00, 'KRFYGJK', 'A012'),
        (
        'C00008', 'Karolina', 'Torento', 'Torento', 'Canada', 1, 7000.00, 7000.00, 9000.00, 5000.00, 'HJKORED', 'A004'),
        ('C00003', 'Martin', 'Torento', 'Torento', 'Canada', 2, 8000.00, 7000.00, 7000.00, 8000.00, 'MJYURFD', 'A004'),
        ('C00009', 'Ramesh', 'Mumbai', 'Mumbai', 'India', 3, 8000.00, 7000.00, 3000.00, 12000.00, 'Phone No', 'A002'),
        ('C00014', 'Rangarappa', 'Bangalore', 'Bangalore', 'India', 2, 8000.00, 11000.00, 7000.00, 12000.00, 'AAAATGF',
         'A001'),
        ('C00016', 'Venkatpati', 'Bangalore', 'Bangalore', 'India', 2, 8000.00, 11000.00, 7000.00, 12000.00, 'JRTVFDD',
         'A007'),
        ('C00011', 'Sundariya', 'Chennai', 'Chennai', 'India', 3, 7000.00, 11000.00, 7000.00, 11000.00, 'PPHGRTS',
         'A010')
    ]
    c.executemany("INSERT INTO CUSTOMER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", records)

    # Create the "ORDERS" table
    c.execute('''CREATE TABLE IF NOT EXISTS "ORDERS"
                 (
                     "ORD_NUM" INTEGER PRIMARY KEY,
                     "ORD_AMOUNT" DECIMAL(12,2) NOT NULL,
                     "ADVANCE_AMOUNT" DECIMAL(12,2) NOT NULL,
                     "ORD_DATE" DATE NOT NULL,
                     "CUST_CODE" VARCHAR(6) NOT NULL,
                     "AGENT_CODE" CHAR(6) NOT NULL,
                     "ORD_DESCRIPTION" VARCHAR(60) NOT NULL,
                     FOREIGN KEY ("CUST_CODE") REFERENCES "CUSTOMER"("CUST_CODE"),
                     FOREIGN KEY ("AGENT_CODE") REFERENCES "AGENTS"("AGENT_CODE")
                 )''')
    records = [
        (200100, 1000.00, 600.00, date(2008, 1, 8), 'C00013', 'A003', 'SOD'),
        (200110, 3000.00, 500.00, date(2008, 4, 15), 'C00019', 'A010', 'SOD'),
        (200107, 4500.00, 900.00, date(2008, 8, 30), 'C00007', 'A010', 'SOD'),
        (200112, 2000.00, 400.00, date(2008, 5, 30), 'C00016', 'A007', 'SOD'),
        (200113, 4000.00, 600.00, date(2008, 6, 10), 'C00022', 'A002', 'SOD'),
        (200102, 2000.00, 300.00, date(2008, 5, 25), 'C00012', 'A012', 'SOD'),
        (200114, 3500.00, 2000.00, date(2008, 8, 15), 'C00002', 'A008', 'SOD'),
        (200122, 2500.00, 400.00, date(2008, 9, 16), 'C00003', 'A004', 'SOD'),
        (200118, 500.00, 100.00, date(2008, 7, 20), 'C00023', 'A006', 'SOD'),
        (200119, 4000.00, 700.00, date(2008, 9, 16), 'C00007', 'A010', 'SOD'),
        (200121, 1500.00, 600.00, date(2008, 9, 23), 'C00008', 'A004', 'SOD'),
        (200130, 2500.00, 400.00, date(2008, 7, 30), 'C00025', 'A011', 'SOD'),
        (200134, 4200.00, 1800.00, date(2008, 9, 25), 'C00004', 'A005', 'SOD'),
        (200108, 4000.00, 600.00, date(2008, 2, 15), 'C00008', 'A004', 'SOD'),
        (200103, 1500.00, 700.00, date(2008, 5, 15), 'C00021', 'A005', 'SOD'),
        (200105, 2500.00, 500.00, date(2008, 7, 18), 'C00025', 'A011', 'SOD'),
        (200109, 3500.00, 800.00, date(2008, 7, 30), 'C00011', 'A010', 'SOD'),
        (200101, 3000.00, 1000.00, date(2008, 7, 15), 'C00001', 'A008', 'SOD'),
        (200111, 1000.00, 300.00, date(2008, 7, 10), 'C00020', 'A008', 'SOD'),
        (200104, 1500.00, 500.00, date(2008, 3, 13), 'C00006', 'A004', 'SOD'),
        (200106, 2500.00, 700.00, date(2008, 4, 20), 'C00005', 'A002', 'SOD'),
        (200125, 2000.00, 600.00, date(2008, 10, 10), 'C00018', 'A005', 'SOD'),
        (200117, 800.00, 200.00, date(2008, 10, 20), 'C00014', 'A001', 'SOD'),
        (200123, 500.00, 100.00, date(2008, 9, 16), 'C00022', 'A002', 'SOD'),
        (200120, 500.00, 100.00, date(2008, 7, 20), 'C00009', 'A002', 'SOD'),
        (200116, 500.00, 100.00, date(2008, 7, 13), 'C00010', 'A009', 'SOD'),
        (200124, 500.00, 100.00, date(2008, 6, 20), 'C00017', 'A007', 'SOD'),
        (200126, 500.00, 100.00, date(2008, 6, 24), 'C00022', 'A002', 'SOD'),
        (200129, 2500.00, 500.00, date(2008, 7, 20), 'C00024', 'A006', 'SOD'),
        (200127, 2500.00, 400.00, date(2008, 7, 20), 'C00015', 'A003', 'SOD'),
        (200128, 3500.00, 1500.00, date(2008, 7, 20), 'C00009', 'A002', 'SOD'),
        (200135, 2000.00, 800.00, date(2008, 9, 16), 'C00007', 'A010', 'SOD'),
        (200131, 900.00, 150.00, date(2008, 8, 26), 'C00012', 'A012', 'SOD'),
        (200133, 1200.00, 400.00, date(2008, 6, 29), 'C00009', 'A002', 'SOD')
    ]

    c.executemany("INSERT INTO ORDERS VALUES (?, ?, ?, ?, ?, ?, ?)", records)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("All tables created successfully!")



if __name__ == "__main__":
    # create_database("testDB.db")
    docs_dir = "accessible-customer-service-policy.pdf"
    pers_dir = "policyData"
    loader = PyPDFLoader(docs_dir)
    loaded_document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=10,
                                                   length_function=len,
                                                   is_separator_regex=False)
    documents = text_splitter.split_documents(loaded_document)
    print(type(documents))

    vector_db = Chroma.from_documents(documents=documents,
                                           embedding=OpenAIEmbeddings(),
                                           persist_directory=pers_dir,
                                           collection_name="test-retrieval")
    print(vector_db)

