import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from io import StringIO

def fetchData(url):
    try: 
        #try to get html
        response = requests.get(url)
        response.raise_for_status()
        #we got it
        html=response.content
        return html
    except requests.Exceptions.RequestException as e:
        #we aint go it
        print(f"Error1: {e}")
        return None
    
def parseTable(html):
    try: 
        #soup to parse html
        soup = bs(html, "html.parser")
        table = soup.find("table")
        if not table:
            print("REEEEEEEEEEE")
            return None, 0, 0
        gridData= {}
        maxX, maxY = 0, 0
           
        rows = table.find_all("tr")[1:] #exclude header
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 3:
                try:
                    #set vals
                    x=int(cells[0].text.strip())
                    char=cells[1].text.strip()
                    y=int(cells[2].text.strip())
                    #set gridData
                    gridData[(x,y)]=char
                    maxX=max(maxX, x)
                    maxY=max(maxY, y)
                except ValueError as e:
                    print(f"Error 2: {e}")
                    
        return gridData, maxX,maxY
    except Exception as e:
        print(f"Error 3: {e}")
        return None, 0, 0
                
def printSecret(gridData, maxX, maxY):
    if not gridData:
        print("Error 4:")
        return

    # makin empty grid
    grid = [[" " for _ in range(maxX + 1)] for _ in range(maxY + 1)]

    #fill it
    for (x, y), char in gridData.items():
        grid[y][x] = char  

    #print it
    for row in grid:
        print("".join(row))
#main
def showsecrets(url):
    html = fetchData(url)
    if html:
        gridData, maxX, maxY = parseTable(html)
        printSecret(gridData, maxX, maxY)
    else:
        print("Failed to retrieve or process the document.")

        
showsecrets("")

    
    
    
    

