import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import qwikidata
import qwikidata.sparql

def get_city_pop(city, country):
    query = """
    SELECT ?population
    WHERE
    {
      ?city rdfs:label '%s'@en.
      ?city wdt:P1082 ?population.
      ?city wdt:P17 ?country.
      ?city rdfs:label ?cityLabel.
      ?country rdfs:label ?countryLabel.
      FILTER(LANG(?cityLabel) = "en").
      FILTER(LANG(?countryLabel) = "en").
      FILTER(CONTAINS(?countryLabel, "%s")).
    }
    """ % (city, country)

    res = qwikidata.sparql.return_sparql_query_results(query)
    try:
        out = res['results']['bindings'][0]
    except:
        return None
    return int(out['population']['value'])

def get_weather(city_name):
    api_key="a9fe161146a5004137fa51873f164072"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    try:
        y=x['main']
    except:
        return [None,None,None,None]
    current_temperature = y["temp"]
    current_humidity = y["humidity"]
    z = x["weather"]
    weather_description = z[0]["description"]
    ans=[city_name,current_temperature,current_humidity,weather_description]
    return ans

    

def main():
    r1=requests.get("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area",headers= {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'})
    soup1=bs(r1.content,'html.parser')
    table1=soup1.find("table")
    t1_coln=["City","Country","Total Area(in sq. km)"]
    t1c1=table1.find_all("td")
    
    t1col1=[]
    t1col2=[]
    t1col3=[]
    i=1
    for x in range(len(t1c1)):
        if(x%10==1):
            ci=t1c1[x].text
            cii=ci.replace('[note {}]'.format(i),'')
            cii=cii.replace('*','')
            if('note' in ci):
                i=i+1
            t1col1.append(cii)
        if(x%10==2):
            t1col2.append("USA")
        if(x%10==8):
            ar=t1c1[x].text
            arr=ar.replace(',','')
            t1col3.append(float(arr[:-1]))
    
    dataa1=[]
    for x in range(len(t1col1)):
        dataa1.append([t1col1[x],t1col2[x],t1col3[x]])
    df1_1=pd.DataFrame(dataa1,columns=t1_coln)
    
    
    
    r2=requests.get("http://www.citymayors.com/statistics/largest-cities-area-125.html",headers= {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'})
    soup2=bs(r2.content,'html.parser')
    table2=soup2.find("table",{"width":"430"})
    t2c1=table2.find_all("font")
    t2col1=[]
    t2col2=[]
    t2col3=[]
    t2col=[]

    for x in range(len(t2c1)):
        val=t2c1[x].text
        t2col.append(val)
    
    t2col=t2col[6:]
    x=0
    while(x<len(t2col)):
        if(x%6==2):
            t2col2.append(t2col[x])
        if(x%6==1):
            t2col1.append(t2col[x])
        if(x%6==4):
            a=t2col[x]
            a=a.replace(',','')
            t2col3.append(float(a))
        x=x+1
    dataa2=[]
    for x in range(len(t2col1)):
        dataa2.append([t2col1[x],t2col2[x],t2col3[x]])
    df1_2=pd.DataFrame(dataa2,columns=t1_coln)
    df1_2=df1_2[df1_2['Country'] != 'Australia']#To exclude repeats
    df1_2=df1_2[df1_2['Country'] != 'USA']#To exclude repeats
    
    r3=requests.get("https://architectureau.com/articles/australian-cities-among-the-largest-and-least-densely-settled-in-the-world/",headers= {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'})
    soup3=bs(r3.content,'html.parser')
    table3=soup3.find("table")
    t3c1=table3.find_all("h3")
    t3col1=[]
    t3col3=[]
    for x in range(len(t3c1)):
        t3col1.append(t3c1[x].text)
    t3c3=table3.find_all("tr")
    vval=t3c3[2].text
    vval=vval.replace('\n','')
    vval=vval.replace(',','')
    vval=vval.replace('km2','k')
    x=0
    while(x<len(vval)):
        if(vval[x] in ['0','1','2','3','4','5','6','7','8','9']):
            y=x+1
            while(y<len(vval)):
                if(vval[y]=='k'):
                    break
                y=y+1
            t3col3.append(float(vval[x:y]))
            x=y+1
        x=x+1
        
    dataa3=[]
    for x in range(len(t3col1)):
        dataa3.append([t3col1[x],"Australia",t3col3[x]])
    df1_3=pd.DataFrame(dataa3,columns=t1_coln)
    
    DF1=pd.concat([df1_1,df1_2,df1_3])
    DF1.reset_index(inplace=True)
    DF1.drop(columns=["index"],inplace=True)
    
    
    
    c_name=["City","Temperature(in K)","Humidity(in %)","Description"]
    dataa4=[]
    for x in range(DF1.shape[0]):
        dataa4.append(get_weather(DF1['City'][x]))
    DF2=pd.DataFrame(dataa4,columns=c_name)
    
    dataa5=[]
    for x in range(DF1.shape[0]):
        dataa5.append(get_city_pop(DF1['City'][x],DF1['Country'][x]))
    DF4=pd.DataFrame(dataa5,columns=['City',"Population"])
    
    mer=pd.merge(DF1,DF2,on="City")
    DF3=pd.merge(mer,DF4,on="City")
    
    print(DF3.head(10))
    
    print(DF3[["Population","Temperature"]].describe().apply(lambda s: s.apply('{0:,.0f}'.format)))
    
    DF3.to_csv("City_Stats.csv")
    
    sp=DF3.plot.scatter(x='City',y='Humidity(in %)',c='DarkBlue')
    hs=DF3.plot.bar(x="City",y="Population",rot=0)
    lc=DF3.plot.line(x="City",y="Temperature(in K)")
    
    print(sp)
    print(hs)
    print(lc)
    
    print(DF3.plot(hs=lc))
    
    


if __name__ == "__main__":
    main()