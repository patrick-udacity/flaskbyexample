import datetime
import feedparser
from flask import Flask,  make_response, render_template, request
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
WEATHER_URL = ("http://api.openweathermap.org/data/2.5/weather?q={}" +
    "&units=imperial&appid=da5610aabb7d8e2e8ec57ef2a74a263c"
)

#Currency APPID
CURRENCY_URL = ("https://openexchangerates.org//api/latest.json" + 
    "?app_id=b23c94daab584f4580e4e2bf75cbcf7e")

DEFAULTS = {'publication': 'bbc',
            'city': 'Memphis,US',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }
@app.route("/")
def home():

    # get customized headlines, based on user input or default
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    # get customized weather based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    #This will provide an additional temperature listing in celcius
    temperatureCel =  (weather['temperature'] - 32) * 5.0/9.0
    temperatureCel= str(round(temperatureCel, 2))

    # get customised currency based on user input or default
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(
        render_template("home.html",
            publication = publication,
            articles=articles,
            weather=weather,
            temperatureCel=temperatureCel,
            currency_from=currency_from,
            currency_to=currency_to,
            rate=rate,
            currencies=sorted(currencies)
        )
    )
    #pdb.set_trace()
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from",
    currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    #pdb.set_trace();
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country'],
                   'sunrise': datetime.datetime.fromtimestamp(parsed['sys']['sunrise']).strftime('%I:%M%p'),
                   'sunset': datetime.datetime.fromtimestamp(parsed['sys']['sunset']).strftime('%I:%M%p')
                   }
    return weather

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
