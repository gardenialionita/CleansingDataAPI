import pandas as pd
import re
import sqlite3

db_conn = sqlite3.connect('cleansingdata.db', check_same_thread=False)
db_conn.text_factory = bytes
mycursor = db_conn.cursor()

#Normalizing Text
def lowercase(text):
    return text.lower()

#Removing Unicode Characters
def remove_unicode_char(text):
    text = re.sub('\n',' ',text)
    text = re.sub(r"((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))",' ',text)
    text = re.sub('  +',' ',text)
    return text

#Removing Non-AlphaNumeric
def remove_non_alphanum(text):
    text = re.sub('[^0-9a-zA-Z]+',' ', text)
    text = re.sub('  +',' ',text)
    return text

#Cleaning Data
def preprocess(text):
    text = lowercase(text)
    text = remove_unicode_char(text)
    text = remove_non_alphanum(text)
    return text

#Process File
def process_file(input_file):
    first_column = input_file.iloc[:, 0]
    print(first_column)

    for tweet in first_column:
        tweet_clean = preprocess(tweet)
        insert_tweet = 'insert into master_tweet (tweet_raw, tweet_clean) values(?, ?)'
        value = (tweet, tweet_clean)
        mycursor.execute(insert_tweet, value)
        db_conn.commit()
        print(tweet)

#Process Text
def process_text(input_text):
    try:
        output_text = preprocess(input_text)
        return output_text
    except:
        print('Your text is unreadable.')








