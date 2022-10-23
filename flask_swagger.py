import sqlite3
import pandas as pd
from flask import Flask, request, jsonify, make_response
from data_cleansing import process_file, process_text
from flask_swagger_ui import get_swaggerui_blueprint

#Init app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#Database
db_conn = sqlite3.connect('cleansingdata.db', check_same_thread=False)
#db_conn.row.factory = sqlite3.row()
mycursor = db_conn.cursor()

#Flask swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Twish!'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

#Homepage
@app.route('/', methods=['GET'])
def get():
    return "Welcome to Twish!"


#Tweet
@app.route('/tweet', methods=['GET','POST'])
def tweet():
    if request.method == 'POST':
        input_text = str(request.form["text"])
        output_text = process_text(input_text)

        insert_tweet = 'insert into master_tweet(tweet_raw, tweet_clean) values(?,?)'
        values = (input_text, output_text)
        mycursor.execute(insert_tweet, values)
        db_conn.commit()
        print(input_text)
        print(output_text)

        return 'Input Data Success'
    
    elif request.method == 'GET':
        query_tweet = 'select* from master_tweet'
        select_tweet = mycursor.execute(query_tweet)
        tweet = [
            dict(tweet_id=row[0], raw_tweet=row[1], clean_tweet= row[2])
            for row in select_tweet.fetchall()

        ]
        return jsonify(tweet)


@app.route('/tweet/<string:tweet_id>', methods=['GET','PUT','DELETE'])
def tweet_id(tweet_id):
    if request.method == 'GET':

        query_text = 'select * from master_tweet where tweet_id = ?'
        value = str(tweet_id)
        select_tweet = mycursor.execute(query_text,[value])
        tweet = [
            dict(tweet_id=row[0], raw_tweet=row[1], clean_tweet= row[2])
            for row in select_tweet.fetchall()
        ]
        print(tweet)

        return jsonify(tweet)

    elif request.method == 'DELETE':

        query_text = 'delete from master_tweet where tweet_id = ?'
        value = tweet_id
        mycursor.execute(query_text,[value])
        db_conn.commit()

        return 'Success Delete Data'

    elif request.method == 'PUT':

        input_text = str(request.form['text'])
        output_text = process_text(input_text)
        query_text = 'update master_tweet set tweet_raw = ?, tweet_clean = ? where tweet_id = ?'
        value = (input_text, output_text, tweet_id)
        mycursor.execute(query_text,value)
        db_conn.commit()

        return 'Success Update Data'


#Upload File
@app.route('/tweet/file/', methods=['POST'])
def tweet_csv():
    if request.method == 'POST':
        file = request.files['file']

        try:
            data = pd.read_csv(file)
        except:
            data = pd.read_csv(file, encoding='utf-8')
        process_file(data)

        return 'Done Process File'


#Error
@app.errorhandler(400)
def handle_err_400(_error):
    'Return a http 400 error to client'
    
    return make_response(jsonify({'error': 'Misunderstood'}), 400)

@app.errorhandler(401)
def handle_err_401(_error):
    'Return a http 401 error to client'
    
    return make_response(jsonify({'error': 'Unauthorized'}), 401)

@app.errorhandler(404)
def handle_err_404(_error):
    'Return a http 404 error to client'
    
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def handle_err_400(_error):
    'Return a http 500 error to client'
    
    return make_response(jsonify({'error': 'Server error'}), 500)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)





