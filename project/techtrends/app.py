import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from werkzeug.wrappers import response
from datetime import datetime
import logging
import sys
# Function for Logging

def logmessage(message, code = 0):
    '''
    code 0 : Normal Log
    code 1: Error Log
    Default is 0
    '''
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if code == 0:
        app.logger.info('{time} | {message}'.format(time=time, message=message))
    else:
        app.logger.error('{time} | {message}'.format(time=time, message=message))

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    get_db_connection.counter+=1
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

#Counter to count the number of times get_dp_connection is called.
get_db_connection.counter = 0

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    
    
    connection.close()
    return post



# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    index.count = len(posts)
    connection.close()
    return render_template('index.html', posts=posts)

index.count = 0
# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logmessage('Article id no. "{id}" doesn\'t exist!'.format(id = post_id), 1)
      return render_template('404.html'), 404
    else:
      title = post['title']
      logmessage('Article "{title}" retrieved!'.format(title = title))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logmessage('About US page retrived!')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            logmessage('A new article, with title: "{title}" created!'.format(title = title))

            return redirect(url_for('index'))

    return render_template('create.html')

#the Health checkpoint.
@app.route("/healthz")
def health():
    response = app.response_class(
        response = json.dumps({"result":"OK - Healthy"}),
        status = 200,
        mimetype= 'application/json'
    )

    app.logger.info('Healthz request successfull')
    return response

#Metrics Checkpoint
@app.route("/metrics")
def metrics():
    
    response = app.response_class(
        response = json.dumps({"post_count":index.count ,"db_connection_count":get_db_connection.counter}),
        status = 200,
        mimetype= 'application/json'
    )
    return response

# start the application on port 3111
if __name__ == "__main__":
    file = logging.FileHandler('app.log')
    streamout = logging.StreamHandler(sys.stdout)
    streamerr = logging.StreamHandler(sys.stderr)
    handlers = [streamerr,streamout,file]
    logging.basicConfig(handlers = handlers, level=logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
