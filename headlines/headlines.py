import feedparser
from flask import Flask, render_template
from flask import request
import json, urllib2, urllib
import pdb

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640',
    'powershell': 'http://community.idera.com/powershell/rss',
    'reuters': 'http://feeds.reuters.com/Reuters/worldNews'
}

#weather APIID: da5610aabb7d8e2e8ec57ef2a74a263c
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=da5610aabb7d8e2e8ec57ef2a74a263c"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"

DEFAULTS = {'publication': 'bbc',
            'city': 'Memphis,US',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }
@app.route("/")
def home():

    # get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    #This will provide an additional temperature listing in celcius
    temperatureCel =  (weather['temperature'] - 32) * 5.0/9.0
    temperatureCel= str(round(temperatureCel, 2))

    return render_template("home.html", articles=articles,
        weather=weather,
        temperatureCel=temperatureCel)

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
                   }
    return weather

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
