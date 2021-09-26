# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 17:12:22 2021

@author: liamd
"""
from espn_api.football import League
import pprint
import pandas as pd
from datetime import date

path = "C:/Users/liamd/Documents/GitHub/IAA21FantasyFootball/Liam Dao/Data/"

year = "2021"
leagueID = "522234"
espn_s2 = "AEBHzXFf5A%2BhxSUDLS8y%2BtkFZkKrm6VImICI2tx7dEcqBzbSVTHgDejFIzSqb8x7kW16CLcveQBnWFiS93HLLvvyhbW17Dl6tPhpjVg%2FaJvxhI%2FeZaIx1V0DQx61gIYjjTTGIvEX%2BSliWTXZDSwAcX3hEe1KzKwe4ATMJqSaEYRI1cJsHq1EkhzcLgaz29Ij3d2QdFXA3EpZ1V199kqsk%2FU8ZMV%2FH3Q60OJMcuUAIT3JMdZTf6q01FbFIhTuiX%2B6JaZCPsbVqpgiEu7554B6AtSr"
swid = "{512E3572-523B-484E-AE35-72523BD84E7E}"


TwelveAM_League = League(year, leagueID, espn_s2, swid)  

#TODO:
week_1 = date(2021, 9, 8)
today = date.today()
this_week = (abs(today - week_1).days // 7) + 1

#Fetch rosters and teams
matchup_rosters = TwelveAM_League.fetch_matchup_rosters()
teams = TwelveAM_League.fetch_teams()

reader = pprint.PrettyPrinter()

first = True
for key, matchup in matchup_rosters.items():
    if matchup['week'] == this_week:
        week = matchup['week']
        home_team = teams[matchup['homeTeamId']]['teamName']
        away_team = teams[matchup['awayTeamId']]['teamName']
        n_players = len(matchup['homeRoster'])
        home_dict = {'Week': [week] * n_players,
                     'MatchupId': [key] * n_players,
                     'Home/Away': ["Home"] * n_players,
                     'Team': [home_team] * n_players,
                     'Player': matchup['homeRoster'],
                     'Slot': matchup['homeLineup'],
                     'Points': matchup['homeRosterScore'],
                     'Eligible Slots': [", ".join(lst) for lst in matchup['homeRosterEligibleSlots']]
                    }
        n_players = len(matchup['awayRoster'])
        away_dict = {'Week': [week] * n_players,
                     'MatchupId': [key] * n_players,
                     'Home/Away': ["Away"] * n_players,
                     'Team': [away_team] * n_players,
                     'Player': matchup['awayRoster'],
                     'Slot': matchup['awayLineup'],
                     'Points': matchup['awayRosterScore'],
                     'Eligible Slots': [", ".join(lst) for lst in matchup['awayRosterEligibleSlots']]
                    }
        home_df = pd.DataFrame(home_dict)
        away_df = pd.DataFrame(away_dict)
        if first:
            df = pd.concat([home_df, away_df])
            first = False
        else:
            df = pd.concat([df, home_df, away_df])
df.to_csv(path + "12AngryMen_MATCHUP_DATA_WEEK_" + str(this_week) + ".csv", index=False)