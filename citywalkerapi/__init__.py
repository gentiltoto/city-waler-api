import flask
from flask import request, jsonify, render_template
from twitterscraper import query_tweets
import datetime as dt
import re

NO_QUERY_ERROR = [
    {
    'error': 'No query provided'
    }
]

DATE_ERROR = [
    {
        'error': 'invalid token in the date format'
    }
]

def create_app():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    @app.route('/api/v1/resources/tweets', methods=['GET'])
    def api_query():
        ### DEFINE PARAMETERS ###

        # Check if a query has been provided
        # If so, assign it to query
        # If not, return the no query error
        if 'query' in request.args:
            query = request.args['query']
        else:
            return jsonify(NO_QUERY_ERROR)

        # Check if a limit has been provided
        # If so, assign it to the limit
        # If not, set limit to None
        if 'limit' in request.args:
            limit = int(request.args['limit'])
        else:
            limit = None

        # Check if a begin date has been provided
        # If so, assign it to the the date
        # If not, set the begin date to 2006-3-21
        if 'begindate' in request.args:
            # Create a list of the numbers in the date
            findall = re.findall(r"\d+", request.args['begindate'])
            for number in findall:
                # Replace the first 0 if forgotten and convert in integer
                number = int(re.sub(r'^0', '', number))
            try:
                begindate = dt.date(findall[0], findall[1], findall[2])
            except SyntaxError:
                return jsonify(DATE_ERROR)
        else:
            begindate = dt.date(2006, 3, 21)

        # Check if a end date has been provided
        # If so, assign it to the the date
        # If not, set the end date to 2006-3-21
        if 'enddate' in request.args:
            # Create a list of the numbers in the date
            findall = re.findall(r"\d+", request.args['enddate'])
            for number in findall:
                # Replace the first 0 if forgotten and convert in integer
                number = int(re.sub(r'^0', '', number))
            try:
                enddate = dt.date(findall[0], findall[1], findall[2])
            except SyntaxError:
                return jsonify(DATE_ERROR)
        else:
            enddate = dt.date.today()

        # Create the result list
        results = []

        tweets = query_tweets(query, begindate = begindate, enddate = enddate)

        for tweet in tweets:
            results.append(
                {
                    "fullname": tweet.fullname,
                    "likes": tweet.likes,
                    "replies": tweet.replies,
                    "retweets": tweet.retweets,
                    "text": tweet.text,
                    "timestamp" : tweet.timestamp
                }
            )

        return jsonify(results)

    return app
