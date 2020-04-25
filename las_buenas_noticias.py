import feedparser
import json
import urllib.parse
import urllib.request

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

FEEDS = {'bbc':"http://feeds.bbci.co.uk/news/rss.xml",
         'cnn':'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'iol': 'http://www.iol.co.za/cmlink/1.640'}


def get_weather(query):
    # go to this URL to see the used JSON format, cambia q={} por q=London,uk
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=52eae8bbb172a9887578373c388e145f"
    # we make the query part configurable, so the City to retrieve data from is Dynamic
    print('\nquery---\n', query)
    # urllib.parse.quote elimina espacios en blanco; al usuario ingresar nombres de ciudad, le puede poner espacio
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    # we retrieve the JSON data stored in the taret page
    data = urllib.request.urlopen(url).read()
    print('\nurl http json data ---\n', data)
    parsed = json.loads(data)   # json parsing; loads = load string
    weather = None
    # this line is exception handling
    if parsed.get("weather"):
        # this calls the parsed JSON data
        weather = {"description": parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather


@app.route("/")
def get_noticas():
    # request.args grabs get requests, request.form grabs POST requests
    query = request.args.get("publication") # the tag name given in the html form
    if not query or query.lower() not in FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()

    # EXCEPTION HANDLING required
    feed = feedparser.parse(FEEDS[publication])

    # call to get weather data from API
    weather = get_weather("London,UK")

    # MY personal checks
    for key in feed:
        print('\nfeeds keys---\n', key)

    # first arg file, second arg **arguments
    # remember .get() avoids not found mistakes
    return render_template("home.html",
                           publication=publication,
                           articulos=feed['entries'],
                           weather=weather)


if __name__ == "__main__":
    app.run(debug=True)
