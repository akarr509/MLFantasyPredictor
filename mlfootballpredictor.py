import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression


url = "https://www.pro-football-reference.com/years/2022/scrimmage.htm"

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

playertable_wrapper = soup.find('div', id = 'div_receiving_and_rushing')
mainplayertable = playertable_wrapper.find('tbody')

playerbaseurl = "https://www.pro-football-reference.com/"

dataset = []
dataset2 = []
dataset3 = []



def statgetter (attribute, list1):
    if (line.find('td', attrs={ 'data-stat': attribute}).text) == "":
        list1.append(0)
    else:
        list1.append(float(line.find('td', attrs={ 'data-stat': attribute}).text))







for playerrow in mainplayertable.find_all('tr', attrs={'class':False})[:400]:
    if playerrow.find('td', attrs={ 'data-stat': 'pos'}).text == 'WR' or playerrow.find('td', attrs={ 'data-stat': 'pos'}).text == 'TE' or playerrow.find('td', attrs={ 'data-stat': 'pos'}).text == 'RB':
        impsec = playerrow.find('td', attrs={ 'data-stat': 'player'})
        linkextension = impsec.find('a')['href']
        newfullurl = playerbaseurl + str(linkextension)
        r1 = requests.get(newfullurl)
        soup1 = BeautifulSoup(r1.text, 'html.parser')
        meta = soup1.find('div', id="meta")
        playername = meta.find('span').text
        averageGP = []
        averageGS = []
        averageTgts = []
        averageRec = []
        averageRecYds = []
        averageRecTD = []
        averageRecGame = []
        averageYPR = []
        averageYPT = []
        averageRushA = []
        averageRushYDS = []
        averageRushTD = []
        averageRYPerAtt = []
        averageRYPerGame = []
        averageRAperGame = []
        averageScrimTouch = []
        averageTouch = []
        averageScrimYDS = []
        averageFumbles = []
        career_stat_columnnames = ["Average of GP", "Average of GS", "Average of Targets", "Average of Receptions", "Average of Rec Yds", "Average of Rec TDS", "Average of Rec Per Game", "Average of YPR","Average of YPT", "Average of Rush Attempts", "Average of Rush Yards", "Average of Rush TDs", "Average of Rush Y/A", "Average of Rush Y/G", "Average of Rush A/G", "Average of Touches", "Average of Scrimmage Yards", "Average of Fumbles"]
        season_stat_columnnames = ["Games Played", "Games Started", "Targets", "Receptions", "Rec Yds", "Rec TDS", "Rec Per Game", "YPR","YPT", "Rush Attempts", "Rush Yards", "Rush TDs", "Rush Y/A", "Rush Y/G", "Rush A/G", "Touches", "Scrimmage Yards", "Fumbles"]
        stat_list = [averageGP, averageGS, averageTgts, averageRec, averageRecYds, averageRecTD, averageRecGame, averageYPR, averageYPT, averageRushA, averageRushYDS, averageRushTD, averageRYPerAtt, averageRYPerGame, averageRAperGame, averageTouch, averageScrimYDS, averageFumbles ]
        print(playername)
        
        def career_stat_uploader():
            for x in range(len(career_stat_columnnames)):
                test[career_stat_columnnames[x]]= ((sum(stat_list[x][0:i+1]))/(i+1))
        def season_stat_uploader():
            for x in range(len(career_stat_columnnames)):
                test[season_stat_columnnames[x]]= stat_list[x][i]

        if playername == "Taysom Hill" or playername == "Ronnie Rivers" or playername == "Ty Montgomery" or playername == "Montrell Washington" or playername == "DJ Turner" or playername == "Juwann Winfree":
            continue
        if playerrow.find('td', attrs={ 'data-stat': 'pos'}).text == 'RB':
            career_table = soup1.find('div', id="div_rushing_and_receiving")
            body = career_table.find('tbody')
            seasonnum = body.find_all('tr', 'full_table')
            if len(seasonnum) > 1:
                for line in seasonnum[:-1]:
                    statgetter('g', averageGP)
                    statgetter('gs', averageGS)
                    statgetter('targets', averageTgts)
                    statgetter('rec', averageRec)
                    statgetter('rec_yds', averageRecYds)
                    statgetter('rec_td', averageRecTD)
                    statgetter('rec_per_g', averageRecGame)
                    statgetter('rec_yds_per_rec', averageYPR)
                    statgetter('rec_yds_per_tgt', averageYPT)
                    statgetter('rush_att', averageRushA)
                    statgetter('rush_yds', averageRushYDS)
                    statgetter('rush_td', averageRushTD)
                    statgetter('rush_yds_per_att', averageRYPerAtt)
                    statgetter('rush_yds_per_g', averageRYPerGame)
                    statgetter('rush_att_per_g', averageRAperGame)
                    statgetter('touches', averageTouch)
                    statgetter('yds_from_scrimmage', averageScrimYDS)
                    statgetter('fumbles', averageFumbles)
                i = 0
                for line in seasonnum[:-1]:
                    if i == len(seasonnum)-2:
                        test = {}
                        test["Player"] = playername
                        test["Year"] = line.find('a').text
                        career_stat_uploader()
                        season_stat_uploader()
    
                        dataset3.append(test)
                        
                    else:
                        test = {}
                        test["Player"] = playername
                        test["Year"] = line.find('a').text
                        career_stat_uploader()
                        season_stat_uploader()
    
                        dataset.append(test)
                        i+=1
                for line in seasonnum[1:-1]:
                    fantasypoint = {}
                    fpoints = 0
                    if (line.find('td', attrs={ 'data-stat': 'yds_from_scrimmage'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.1*(float(line.find('td', attrs={ 'data-stat': 'yds_from_scrimmage'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rec'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.5*(float(line.find('td', attrs={ 'data-stat': 'rec'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rush_receive_td'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (6*(float(line.find('td', attrs={ 'data-stat': 'rush_receive_td'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'fumbles'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (-2*(float(line.find('td', attrs={ 'data-stat': 'fumbles'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rush_yds'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.1*(float(line.find('td', attrs={ 'data-stat': 'rush_yds'}).text)))
                    
                    fantasypoint["FPoints Predict"] = fpoints
                    dataset2.append(fantasypoint)
            
        else:
            career_table = soup1.find('table', id="receiving_and_rushing")
            body = career_table.find('tbody')
            seasonnum = body.find_all('tr', 'full_table')
            if len(seasonnum) > 1:
                for line in seasonnum[:-1]:
                    statgetter('g', averageGP)
                    statgetter('gs', averageGS)
                    statgetter('targets', averageTgts)
                    statgetter('rec', averageRec)
                    statgetter('rec_yds', averageRecYds)
                    statgetter('rec_td', averageRecTD)
                    statgetter('rec_per_g', averageRecGame)
                    statgetter('rec_yds_per_rec', averageYPR)
                    statgetter('rec_yds_per_tgt', averageYPT)
                    statgetter('rush_att', averageRushA)
                    statgetter('rush_yds', averageRushYDS)
                    statgetter('rush_td', averageRushTD)
                    statgetter('rush_yds_per_att', averageRYPerAtt)
                    statgetter('rush_yds_per_g', averageRYPerGame)
                    statgetter('rush_att_per_g', averageRAperGame)
                    statgetter('touches', averageTouch)
                    statgetter('yds_from_scrimmage', averageScrimYDS)
                    statgetter('fumbles', averageFumbles)
                i = 0
                for line in seasonnum[:-1]:
                    if i == len(seasonnum)-2:
                        test = {}
                        test["Player"] = playername
                        test["Year"] = line.find('a').text
                        career_stat_uploader()
                        season_stat_uploader()

                        dataset3.append(test)

                    else:
                        test = {}
                        test["Player"] = playername
                        test["Year"] = line.find('a').text
                        career_stat_uploader()
                        season_stat_uploader()

                        dataset.append(test)
                        i+=1

                for line in seasonnum[1:-1]:
                    fantasypoint = {}
                    fpoints = 0
                    if (line.find('td', attrs={ 'data-stat': 'yds_from_scrimmage'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.1*(float(line.find('td', attrs={ 'data-stat': 'yds_from_scrimmage'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rec'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.5*(float(line.find('td', attrs={ 'data-stat': 'rec'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rush_receive_td'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (6*(float(line.find('td', attrs={ 'data-stat': 'rush_receive_td'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'fumbles'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (-2*(float(line.find('td', attrs={ 'data-stat': 'fumbles'}).text)))
                    if (line.find('td', attrs={ 'data-stat': 'rush_yds'}).text) == "":
                        fpoints += 0
                    else:
                        fpoints += (.1*(float(line.find('td', attrs={ 'data-stat': 'rush_yds'}).text)))

                    fantasypoint["FPoints Predict"] = fpoints
                    dataset2.append(fantasypoint)

df = pd.DataFrame(dataset)
df2 = pd.DataFrame(dataset2)

df = df.join(df2)
df.to_csv('traindata.csv', index=False)

df3 = pd.DataFrame(dataset3)
df3.to_csv("testdata.csv", index = False)

df = pd.read_csv("traindata.csv")
final = []

df_np = df.to_numpy()

X_train, y_train = df_np[:, 2:38], df_np[:, -1]

reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)

df2 = pd.read_csv("testdata.csv")
df2_np = df2.to_numpy()

ytest = df2_np[:, 2:38]

for i in range(len(ytest)):
  mlpredict = {}
  a = list(ytest[i])
  hey = (reg.predict([a])).tolist()
  mlpredict['Predictions'] = hey[0]
  final.append(mlpredict)

df1 = pd.DataFrame(final)
namescolumn = df2.pop('Player')

df1["Names"] = namescolumn
df1.to_csv('finaloutput.csv', index = False)

