import xml.etree.ElementTree as etree
import urllib.request
import textwrap
from random import randint

def weatherdata():
    url = 'http://weather.yahooapis.com/forecastrss?w=6&u=c'
    try:
        xmltext = (urllib.request.urlretrieve(url))
    except:
        print('Internet connection or WOEID is not valid')
    root = (etree.parse(xmltext[0])).getroot()
    day0 = root[0][12][7].attrib #Today, magically pulled from xml file
    day1 = root[0][12][8].attrib
    day2 = root[0][12][9].attrib
    wind0 = root[0][8].attrib
    hold = [wind0, day0, day1, day2]
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
        message.append(" You may also want to dress in layers, the tempurature changes a lot")
    messStr = ''
    for i in message:
        messStr = messStr + i
    
    return str(messStr), list(weather)

def quotes():
    url = 'http://www.quotesdaddy.com/feed'
    try:
        xmltext = (urllib.request.urlretrieve(url))
    except:
        print('Internet connection is not valid')
    root = (etree.parse(xmltext[0])).getroot()
    quotes = []
    for n in root.iter('description'):
        quotes.append(n.text)
    return quotes[1]
       
            
        

def drawmenu(message, weather, quote):
    lnc = 63 #How many characters you want the screen to be wide (Line Count)
    high = weather[0]
    low = weather[1]
    genline = lambda mes: print(' '*((lnc - len(mes) -1)//2) + mes + ' '*((lnc - len(mes) -1)//2)) #Centre text on screen based on lnc
    weatherline = "High: " + str(high) + u'°' + "C" + "   " + "Low: " + str(low) + u'°' + "C" 

    Bweather = textwrap.wrap(weatherline, lnc - 5)
    Bmessage = textwrap.wrap(message, lnc - 5)
    Bquote = textwrap.wrap(quote, lnc - 5)

   
    #check = True if line[1] != '' else False
    
    
    print('='*lnc) # 63 characters long
    print('')
    for i in Bweather:
        genline(i)
    print('')
    for i in Bmessage:
        genline(i)
    print('')
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
    quote = quotes()
    drawmenu(messagex, weather, quote)
main()
