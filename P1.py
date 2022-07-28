import requests
from bs4 import BeautifulSoup as bs
from typing import Dict, Callable, List
from pandas import DataFrame


def lis(soup: bs):
    return {row.find("h3").text.strip(): change_q_h(row.find("span", {"class": "sidearm-roster-player-height"}).text) for row in soup.find_all("div", {"class": "sidearm-roster-player-pertinents"})}


def tab(soup: bs):
    return {row.find("td", {"class": "sidearm-table-player-name"}).text.strip(): change_l_h(row.find("td", {"class": "height"}).text) for row in soup.find("div", {"data-bind": "if: active_template().id == 2, css: {'sidearm-roster-template-active': active_template().id == 2}"}).find("tbody").find_all("tr")}


urls: Dict[str, List[Callable[[bs], Dict[str, int]]]] = {
    "https://yorkathletics.com/sports/mens-volleyball/roster": tab,
    "https://yorkathletics.com/sports/mens-swimming-and-diving/roster": tab,
    "https://queensknights.com/sports/womens-swimming-and-diving/roster": tab,
    "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster/2019": lis,
    "https://www.brooklyncollegeathletics.com/sports/womens-volleyball/roster/2019": lis,
    "https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster": lis,
    "https://athletics.baruch.cuny.edu/sports/womens-volleyball/roster": lis,
    "https://johnjayathletics.com/sports/womens-volleyball/roster": lis,
    "https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster": lis,
    "https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster": lis,
    "https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster": lis,
    "https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster": lis,
    
}

def change_q_h(org: str):
    return (int(org[0])*12 + int(org[2 : -1]))


def change_l_h(org: str):
    if(org[0])=='-':
        return 70
    return (int(org[0])*12 + int(org[(org.index('-')+1):]))


mens_swim: DataFrame
mens_vol: DataFrame
womens_swim: DataFrame
womens_vol: DataFrame


def scrap_mens_swim():
    urld: Dict[str, Callable[[bs], Dict[str, int]]] = {url: val for url, val in urls.items() if "/mens-s" in url}
    df: DataFrame = DataFrame()
    global mens_swim
    for url, method in urld.items():
        df = df.append(get_heights(url, method))
    df = df.sort_values(by="Height")
    mens_swim = df
    return
def scrap_mens_vol():
    urld: Dict[str, Callable[[bs], Dict[str, int]]] = {url: val for url, val in urls.items() if "/mens-v" in url}
    df: DataFrame = DataFrame()
    global mens_vol
    for url, method in urld.items():
        df = df.append(get_heights(url, method))
    df = df.sort_values(by="Height")
    mens_vol = df
    return

def scrap_womens_swim():
    urld: Dict[str, Callable[[bs], Dict[str, int]]] = {url: val for url, val in urls.items() if "/womens-s" in url}
    df: DataFrame = DataFrame()
    global womens_swim
    for url, method in urld.items():
        df = df.append(get_heights(url, method))
    df = df.sort_values(by="Height")
    womens_swim = df
    return


def scrap_womens_vol():
    urld: Dict[str, Callable[[bs], Dict[str, int]]] = {url: val for url, val in urls.items() if "/womens-v" in url}
    df: DataFrame = DataFrame()
    global womens_vol
    for url, method in urld.items():
        df = df.append(get_heights(url, method))
    df = df.sort_values(by="Height")
    womens_vol = df
    return


def get_heights(url: str,parse: Callable[[bs], Dict[str, int]]) -> DataFrame:
    soup: bs = bs(requests.get(url).content, "html.parser")
    r: Dict[str, int] = parse(soup)
    ans=DataFrame({"Name of Player": r.keys(), "Height": r.values()})
    return ans

def Average_height():
    print("Mens Volleyball Average: {} inches".format(mens_vol['Height'].mean()))
    print("Mens Swimming Average: {} inches".format(mens_swim['Height'].mean()))
    print("Womens Volleyball Average: {} inches".format(womens_vol['Height'].mean()))
    print("Womens Swimming Average: {} inches".format(womens_swim['Height'].mean()))
    return


def extremes():
    print("Men's Volleyball (shortest)", mens_vol.head(5), sep='\n')
    print("Men's Volleyball (tallest)", mens_vol.tail(5),sep='\n')
    print("Men's Swimming (shortest)", mens_swim.head(5), sep='\n')
    print("Men's Swimming (tallest)", mens_swim.tail(5),sep='\n')
    print("Women's Volleyball (shortest)", womens_vol.head(5),sep='\n')
    print("Women's Volleyball (tallest)", womens_vol.tail(5),sep='\n')
    print("Women's Swimming (shortest)", womens_swim.head(5),sep='\n')
    print("Women's Swimming (tallest)", womens_swim.tail(5),sep='\n')
    return


if __name__ == "__main__":
    for met in [scrap_mens_swim, scrap_womens_swim, scrap_womens_vol, scrap_mens_vol, Average_height, extremes]:
        met()
    print("In general, A volleyball player is taller than a Swimmer.")
