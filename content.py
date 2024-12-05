from urllib import request
import random
import json
import csv
import datetime

def get_random_quote(quotes_file='quotes.csv'): # we will get random quotes from this function
    
    try:
        with open(quotes_file) as csvfile:
            fi = csv.reader(csvfile,delimiter='|')
            #print(fi)
            print(fi.line_num)
            quotes = [{'author':line[0],'quote':line[1]} for line in csv.reader(csvfile,delimiter='|')]
    except Exception as e :
        print(e)
        quotes = [{'author':'APJ Abdul Kalam','Quote':'If you want to shine like a Sun, you must first burn like a sun'}]
    
    return random.choice(quotes)

def get_email_content():
    pass

def get_weather_forecast(cord ={'lat':'28.98','long':'77.70'}):
    try:
        api_key = 'API_KEY_WILL_BE_HERE'
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={cord["lat"]}&lon={cord["long"]}&appid={api_key}'
        data = json.load(request.urlopen(url))

        forcast = {'city':data['city']['name'],  #city name
                   'country':data['city']['country'],  #country name
                   'periods':list()}  #list to hold forcast data for future use   
        
        for period in data['list'][0:9]:   #fetch forcast data for next 9 periods
            forcast['periods'].append({'timestamp':datetime.datetime.fromtimestamp(period['dt']),
                                       'temp':round(period['main']['temp']),
                                       'description':period['weather'][0]['description'].title(),
                                       'icon':f'http://openweathermap.org/img/wn/{period["weather"]}',
                                       'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        return forcast
    except Exception as e:
        print(e)

def get_twitter_trends():
    pass

def get_wikipedia_article():
    try:
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {
            'title':data['title'],
            'extract':data['extract'],
            'url':data['content_urls']['desktop']['page']
        }
    except Exception as e:
        print(e)



if __name__=='__main__':
    ''''
     # checking weather forcast is available or not

    forcast = get_weather_forcast()

    if forcast is None:
        print('Invalid co-oridinates')
    else:
        city = forcast['city']
        country = forcast['country']
        print(f' for {city} - and country {country}')
        for info in forcast['periods']:
            #print(info['temp'])
            temp = float(info['temp']) - 273
            print('time - ',info['timestamp'],' temperature - ',temp,'C',info['description'])
    '''

    # checking wikipeida content
    '''
    data = get_wikipedia_article()

    if data is None:
        print('Page not Found')
    else:
        for d in data:
            print(f'{d} - {data[d]}')
            '''

