import feedparser
from flask import Flask

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

    print()
    print('ARTICULO 1')
    articulo_1 = feed['entries'][0]
    for key, val in articulo_1.items():
        print(key, ':', val)

    # DEVELOPMENT, should change
    # remember get avoids not found mistakes
    return f"""<html>
    <body>
        <h1> titulares de noticias de {publication.upper()} </h1>
        <b>{articulo_1.get("title")}</b> <br/>
        <i>{articulo_1.get("published")}</i> <br/>
        <p>{articulo_1.get("summary")}<p/> <br/> """


if __name__ == "__main__":
    app.run(debug=True)
