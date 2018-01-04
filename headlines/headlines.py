import feedparser
from flask import Flask, render_template
from flask import request
import pdb
app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
    'powershell': 'http://community.idera.com/powershell/rss',
    'reuters': 'http://feeds.reuters.com/Reuters/worldNews'
}
@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    #pdb.set_trace()
    return render_template("home.html",
        articles=feed['entries']
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)