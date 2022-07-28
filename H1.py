import requests as rq
from bs4 import BeautifulSoup as bs
def hei(url):
    li=rq.get(url)
    soup=bs(li.content,'html.parser')
    out=[]
    for h in soup.findAll("span",{"class":"sidearm-roster-player-height"}):
        out.append((int(h.text[0])*12)+int(h.text[2:-1]))
    return out
if __name__ == "__main__":
    urls=['https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster','https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster','https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster','https://athletics.baruch.cuny.edu/sports/womens-volleyball/roster']
    avg_swim_men=sum(hei(urls[0]))/len(hei(urls[0]))
    avg_swim_women=sum(hei(urls[1]))/len(hei(urls[1]))
    avg_vol_men=sum(hei(urls[2]))/len(hei(urls[2]))
    avg_vol_women=sum(hei(urls[3]))/len(hei(urls[3]))
    print("Average height in inches:")
    print("Men's Swimming: {}".format(avg_swim_men))
    print("Women's Swimming: {}".format(avg_swim_women))
    print("Men's Volleyball: {}".format(avg_vol_men))
    print("Women's Volleyball: {}".format(avg_vol_women))
    print("Average of Men's Volleyball team height is greater than Average of Men's Swimming team by {} inches".format(abs(avg_swim_men-avg_vol_men)))
    print("Average of Women's Volleyball team height is greater than Average of Women's Swimming team by {} inches".format(abs(avg_swim_women-avg_vol_women)))
    print("Avg Swimmer height: {} inches".format((avg_swim_men+avg_swim_women)/2))
    print("Avg Volleyball player height: {} inches".format((avg_vol_men+avg_vol_women)/2))
    print("Hence, the average volleyball player is taller than the average swimmer.")