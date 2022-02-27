import sqlite3
import pandas as pd
from zipfile import ZipFile


#Extract .zip file
with ZipFile('exhibitA-input.zip', 'r') as zipObj:
    zipObj.extract("exhibitA-input.csv") 


#Read data from .csv file and save as dataframe
df = pd.read_csv('exhibitA-input.csv',delimiter="\t")


#Create a SQL database
conn = sqlite3.connect(":memory:")
cur = conn.cursor()


#Copy input data from DataFrame to SQL table
df.to_sql(name='sql_table', con=conn, if_exists='append',index=False)
conn.commit()


#Execute SQL query
cur.execute("""SELECT DISTINCT_PLAY_COUNT, count(CLIENT_ID) as CLIENT_COUNT FROM
(SELECT CLIENT_ID, count(SONG_ID) as DISTINCT_PLAY_COUNT FROM
(SELECT DISTINCT CLIENT_ID, SONG_ID FROM sql_table
where PLAY_TS like "10/08/2016%")
GROUP BY CLIENT_ID)
GROUP BY DISTINCT_PLAY_COUNT""")
query_result=cur.fetchall()


#Create a new DataFrame in order to save final data to result.csv file
DISTINCT_PLAY_COUNT=[]
CLIENT_COUNT=[]
for i,j in query_result:
    DISTINCT_PLAY_COUNT.append(i)
    CLIENT_COUNT.append(j)
data = {'DISTINCT_PLAY_COUNT': DISTINCT_PLAY_COUNT,
        'CLIENT_COUNT': CLIENT_COUNT
        }
df = pd.DataFrame(data, columns= ['DISTINCT_PLAY_COUNT', 'CLIENT_COUNT'])
df.to_csv('result.csv',index=False)


#Close database connection
conn.close()
