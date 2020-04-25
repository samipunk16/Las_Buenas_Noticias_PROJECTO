import feedparser

from flask import Flask
from flask import render_template

app = Flask(__name__)

FEEDS = {'bbc':"http://feeds.bbci.co.uk/news/rss.xml",
         'cnn':'http://rss.cnn.com/rss/edition.rss',
        'fox': 'http://feeds.foxnews.com/foxnews/latest',
        'iol': 'http://www.iol.co.za/cmlink/1.640'}


@app.route("/")
@app.route("/<publication>")    # anything passed here is 'publication', YOU ARE CREATING A VARIABLE to hold a string
def get_noticas(publication="bbc"):  # if nothing passed here, publication is BBC
    # EXCEPTION HANDLING required
    feed = feedparser.parse(FEEDS[publication])

    # MY personal checks
    for key in feed:
        print(key)

    # first arg file, second arg **arguments
    # remember .get() avoids not found mistakes
    return render_template("home.html",
                           publication=publication,
                           articulos=feed['entries'])


if __name__ == "__main__":
    app.run(debug=True)
