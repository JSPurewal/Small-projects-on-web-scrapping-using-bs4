import requests
from bs4 import BeautifulSoup as bs
from pandas import DataFrame


def col_par(table,at,per):
    c=table.find_all("td",attrs=at)
    col=[]
    for x in c:
        x=x.text
        if(per==0):
            col.append(float(x))
        if(per==1):
            col.append(float(x[:-1]))
    return col
def main() -> None:
    r=requests.get("https://tradingeconomics.com/united-states/stock-market")
    soup=bs(r.content,"html.parser")
    table=soup.find("table",attrs={"class":"table table-hover sortable-theme-minimal table-heatmap"})


    column_name=table.find_all("th")
    col_name=[]
    for x in column_name:
        x=x.text
        col_name.append(x)
    del col_name[0]
    del col_name[2]
    del col_name[2]
    del col_name[-1]
    
    
    col1=[]
    col2=col_par(table,{"id":"p"},0)
    col3=col_par(table,{"id":"nch"},0)
    col4=col_par(table,{"id":"pch"},1)
    
    c1=table.find_all("td",attrs={"class":"hidden-xs"})
    for x in c1:
        x=x.text
        col1.append(x)
    
    col1_up=[]
    for x in range(len(col1)):
        if(x%2==0):
            d=col1[x][2:-2]
            col1_up.append(d)

    

    data=[]
    for x in range(len(col2)):
        row=[col1_up[x],col2[x],col3[x],col4[x]]
        data.append(row)
    df=DataFrame(data, columns=col_name)
    df.to_csv("top_stocks.csv")

    # describe
    print(df[["Price", "Year"]].describe().apply(lambda s: s.apply('{0:,.0f}'.format)))

    return


if __name__ == "__main__":
    main()
