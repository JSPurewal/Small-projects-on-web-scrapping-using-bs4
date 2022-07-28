import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def stock_info(sym,col):
    val=yf.Ticker(sym)
    row=[sym]
    for x in range(len(col)):
        row.append(val.info.get(col[x]))
    return row


def main():
    r=requests.get("https://www.slickcharts.com/sp500",headers= {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'})
    soup=bs(r.content,('html.parser'))
    table=soup.find("table",{"class":"table table-hover table-borderless table-sm"})
    
    
    column_names=["Company","Symbol","Price"]
    col1=[]

    col2=[]
    c1=table.find_all("a")
    for x in range(len(c1)):
        if(x%2==0):
            col1.append(c1[x].text)
        else:
            col2.append(c1[x].text)
    col3=[]
    c3=table.find_all("td",{"class":"text-nowrap"})
    for x in range(len(c3)):
        if(x%3==0):
            col3.append(c3[x].text[3:])
    data=[]
    for x in range(len(col1)):
        data.append([col1[x],col2[x],col3[x]])
    DF1=pd.DataFrame(data,columns=column_names)
    
    
    
    
    col_names2=["zip","fullTimeEmployees","currentPrice","returnOnAssets","averageVolume"]
    data2=[]
    for y in range(DF1.shape[0]):
        data2.append(stock_info(DF1["Symbol"][y],col_names2))
    col_names2.insert(0,"Symbol")
    DF2=pd.DataFrame(data2,columns=col_names2)
    
    
    DF3=pd.merge(DF1,DF2,on="Symbol")
    
    
    print(DF3)
    
    print(DF3[["fullTimeEmployees","currentPrice","returnOnAssets","averageVolume"]].describe().apply(lambda s: s.apply('{0:,.0f}'.format)))
    
    #DF3.to_csv("Stock_info.csv")
    
    
if __name__ == "__main__":
    main()