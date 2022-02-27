import pandas as pd
from zipfile import ZipFile

#Extract .zip file
with ZipFile('exhibitA-input.zip', 'r') as zipObj:
    zipObj.extract("exhibitA-input.csv") 

#Read input data from .csv file and save as dataframe
df = pd.read_csv('exhibitA-input.csv',delimiter="\t")

#Get final data (It can be a single line instead of the following 4 lines. I just wanted it to be more understandable)
df=df[df["PLAY_TS"].str.contains("10/08/2016")] #Filter for desired date
df=df[["CLIENT_ID","SONG_ID"]].drop_duplicates()  #Drop duplicate songs that each client listened to
df=df.groupby("CLIENT_ID")["CLIENT_ID"].size().reset_index(name="DISTINCT_PLAY_COUNT") #Get number of distinct songs for each client
df=df.groupby("DISTINCT_PLAY_COUNT")["DISTINCT_PLAY_COUNT"].size().reset_index(name="CLIENT_COUNT") #Get final data
#df=df[df["PLAY_TS"].str.contains("10/08/2016")][["CLIENT_ID","SONG_ID"]].drop_duplicates().groupby("CLIENT_ID")["CLIENT_ID"].size().reset_index(name="DISTINCT_PLAY_COUNT").groupby("DISTINCT_PLAY_COUNT")["DISTINCT_PLAY_COUNT"].size().reset_index(name="CLIENT_COUNT")

#Save final data to result.csv file
df.to_csv('result.csv',index=False)
