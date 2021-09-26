import pprint
import requests
import pprint

leagueID = "522234"

view = "mDraftDetail"

#URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/" + leagueID + "?view=mTeam"
#URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/" + leagueID + "?view=mRoster"
#URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/" + leagueID + "?view=mDraftDetail"
#URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/" + leagueID + "?view=mMatchup"

URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2021/segments/0/leagues/" + leagueID + "?view="+view


r = requests.get(URL,
                cookies={"espn_s2": "AEBHzXFf5A%2BhxSUDLS8y%2BtkFZkKrm6VImICI2tx7dEcqBzbSVTHgDejFIzSqb8x7kW16CLcveQBnWFiS93HLLvvyhbW17Dl6tPhpjVg%2FaJvxhI%2FeZaIx1V0DQx61gIYjjTTGIvEX%2BSliWTXZDSwAcX3hEe1KzKwe4ATMJqSaEYRI1cJsHq1EkhzcLgaz29Ij3d2QdFXA3EpZ1V199kqsk%2FU8ZMV%2FH3Q60OJMcuUAIT3JMdZTf6q01FbFIhTuiX%2B6JaZCPsbVqpgiEu7554B6AtSr",
                         "swid": "{512E3572-523B-484E-AE35-72523BD84E7E}"})
data = r.json()

reader = pprint.PrettyPrinter()
reader.pprint(data)
# for player in data['players']:
#     reader.pprint(player['player']['fullName'])