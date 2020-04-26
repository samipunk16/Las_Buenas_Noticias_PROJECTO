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

DEFAULTS = {'publication': 'bbc',
            'city': 'London, UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

# WEATHER_URL = should be move here as a global constant

CURRENCY_URL = 'http://openexchangerates.org//api/latest.json?app_id=f912952226584e9eb60726070557f382'

def get_weather(query):
    # go to this URL to see the used JSON format, cambia q={} por q=London,uk
    weather_api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=52eae8bbb172a9887578373c388e145f"
    # we make the query part configurable, so the City to retrieve data from is Dynamic
    print('\nquery---\n', query)
    # urllib.parse.quote elimina espacios en blanco; al usuario ingresar nombres de ciudad, le puede poner espacio
    query = urllib.parse.quote(query)
    url = weather_api_url.format(query)
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
                   "city": parsed["name"],
                   "country": parsed['sys']['country']
                   } # the API response has the country code listed under 'sys'
    return weather


def get_noticas(query):
    if not query or query.lower() not in FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(FEEDS[publication])
    return feed['entries']

def get_rate(frm, to):
    # open the currency_url so you understand how the currencies json file is configured
    # its only USD from
    all_currency = urllib.request.urlopen(CURRENCY_URL).read()

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate, parsed.keys()  # the keys strs are for forming the lists in the select input html


@app.route("/")
def home():
    # - get customized headlines, based on user input or default
    # request.args grabs get requests, request.form grabs POST requests
    publication = request.args.get("publication")  # the tag name given in the html form
    if not publication:
        publication = DEFAULTS['publication']
    articulos = get_noticas(publication)

    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    # - get customized currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']

    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']

    rate, currencies = get_rate(currency_from, currency_to)

    return render_template("home.html",
                           publication=publication,
                           articulos=articulos,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))


if __name__ == "__main__":
    app.run(debug=True)
