import xml.etree.ElementTree as etree
import urllib.request
import textwrap
import configparser
from random import randint

def weatherdata():
    url = 'http://weather.yahooapis.com/forecastrss?w=' + str(config['INFO']['WOEID']) + '&u=' + str(config['INFO']['UNITS'])
    #print(url)
    root = returnroot(url)
    day0 = root[0][12][7].attrib #Today, magically pulled from xml file
    day1 = root[0][12][8].attrib
    day2 = root[0][12][9].attrib
    day3 = root[0][12][10].attrib
    wind0 = root[0][8].attrib
    hold = [wind0, day0, day1, day2, day3]
    return hold



def message(data): #Generate small message to summarize weather (mostly based on tempurature and windspeed)
    day0 = data[1]
    windchill = int(data[0]['chill'])
    windspeed = float(data[0]['speed'])
    high = int(day0['high'])
    low = int(day0['low'])
    weather = list((low, high))
    #conditions = day0['text']
    message = []
    b = lambda x, a, b: True if x > a and x <= b else False # b = Between
    scarf = True if windspeed > 15 and low <= 0 else False  #Check if it's cold and windy
    ## Starting statement about weather
    if low < -20 or windchill < -20:
        if scarf:
            message.append("It's extremely cold, You will need a good jacket and a scarf.")
        else:
            message.append("It's extremely cold, You will need to wear a jacket and maybe a scarf.")   
    elif b(low, -20, 0) or b(windchill, -20, 0):
        if scarf:
            message.append("It's pretty cold, You'll need a good jacket and a scarf.")
        else:
            message.append("It's pretty cold, You'll need a good jacket.")
    elif b(low, 0, 15) or b(windchill, 0, 15):
        message.append("It's cool, You'll need a jacket")
    elif b(low, 15, 25) or b(windchill, 15, 25):
        message.append("It's pretty warm, you'll survive in a t-Shirt.")
    elif low > 25 or windchill > 25:
        message.append("It's pretty hot, wear something light.")  
    
    ## Check if there's a large difference in high/low
    if abs(high) - abs(low) > 10:
        message.append("You may also want to dress in layers, the tempurature changes a lot")
    messStr = ''
    for i in message:
        messStr = messStr + i
    
    return str(messStr), list(weather)

def quotes():
    root = returnroot('http://www.quotesdaddy.com/feed')
    quotes = []
    for n in root.iter('description'):
        quotes.append(n.text)
    return quotes[len(quotes)-1]
       
def returnroot(url):
    try:
        xmltext = (urllib.request.urlretrieve(url))
    except:
        print('Internet connection or WOEID is not valid')
    root = (etree.parse(xmltext[0])).getroot()
    return root
         
def currentx():
    units = str(config['INFO']['UNITS'])
    city = str(config['INFO']['CITY'])
    country = str(config['INFO']['COUNTRY'])
    if units == 'c':
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=metric&mode=xml'
    else:
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&units=imperial&mode=xml'
    root = returnroot(url)
    currWind = round(float(root[4][0].attrib['value'])) # Current wind speed, magic'd from the xml file
    currWDir = root[4][1].attrib['code'] # Current wind direction
    currCond = root[7].attrib['value'] # Current sky conditions
    currTemp = round(float(root[1].attrib['value'])) # Current Tempurature
    hold = [currTemp, currCond, currWind, currWDir]
    return hold

def forecastx(data):
    day = [data[2], data[3], data[4]]
    
    hold = []
    for i in range(0, len(day)):
        hold.append((str(day[i]['day']), str(day[i]['high']), str(day[i]['low']), str(day[i]['text'])))
    return hold
    
def drawmenu(message, weather, quote, current, forecast):
    lnc = int(eval(config['INFO']['LINE'])) #How many characters you want the screen to be wide (Line Count)
    high = weather[1]
    low = weather[0]
    genline = lambda mes: print(' '*((lnc - len(mes) -1)//2) + mes + ' '*((lnc - len(mes) -1)//2)) #Centre text on screen based on lnc
    
    ## Regular lines
    wind = str(current[2]) + ' km/H ' + str(current[3]) + ' | ' + str(current[1]).capitalize()
    weatherline = "High: " + str(high) + u'°' + "C" + " " + "Low: " + str(low) + u'°' + "C"  + ' | ' + wind
    Bweather = textwrap.wrap(weatherline, lnc - 5)#Ensure that lines fit line character limit
    Bmessage = textwrap.wrap(message, lnc - 5)
    #print(quote)
    try:
        Bquote = textwrap.wrap(quote, lnc - 5)
    except:
        Bquote = textwrap.wrap('Feed a man a fish, he will eat for a day. Teach a man to fish, and he eat for a lifetime. - Bible Proverb', lnc-5)
        
    ## Current conditions
    temp = 'Current Temperature: ' + str(current[0]) + u'°' + "C"
    
    Btemp = textwrap.wrap(temp, lnc - 5)
    #Bwind = textwrap.wrap(wind, lnc - 5)

    ### Forcast
    Fdata = []
    #print(forecast[2])
    for i in range(0, len(forecast)):
        Fdata.append(str(forecast[i][0]) + ' == ' + ' High: ' + str(forecast[i][1]) + u'°' + "C" + ' Low: ' + str(forecast[i][2]) + u'°' + "C " + str(forecast[i][3])) 
     
    BFdata0 = textwrap.wrap(Fdata[0], lnc - 5)
    BFdata1 = textwrap.wrap(Fdata[1], lnc - 5)
    BFdata2 = textwrap.wrap(Fdata[2], lnc - 5)

    ## Draw screen
    
    print('='*lnc) # 63 characters long
    print('')
    for i in Btemp:
        genline(i)

    print('')
    for i in Bweather:
        genline(i)
    
    print('')
    
    for i in Bmessage:
        genline(i)
    print('')
    genline('Forcast:')
    #print('')
    for i in BFdata0:
        genline(i)
    for i in BFdata1:
        genline(i)
    for i in BFdata2:
        genline(i)
        
    print('='*lnc)
    print('')
    genline('Quote:')
    print('')
    for i in Bquote:
        genline(i)
    print('')
    print('='*lnc)
    

def main():
    data = weatherdata()
    #print(data)
    messagex, weather = message(data)
    forecast = forecastx(data)
    quote = quotes()
    current = currentx()
    drawmenu(messagex, weather, quote, current, forecast)

global config
configx = configparser.ConfigParser()
configx.read('config.ini')
config = configx


main()
