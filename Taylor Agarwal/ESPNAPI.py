#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pprint
import requests
import pandas as pd

class League:
    
    def __init__(self, year, leagueID, espn_s2, swid):
        self.year = str(year)
        self.leagueID = str(leagueID)
        self.espn_s2 = espn_s2
        self.swid = swid

    def fetch(self, view):
        URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + self.year + "/segments/0/leagues/" + self.leagueID + "?view=" + view
        r = requests.get(URL, cookies={"espn_s2": self.espn_s2, "swid": self.swid})
        data = r.json()
        return data

    def fetch_teams(self):
        team_data = self.fetch("mTeam")
        Teams = dict()
        members = team_data['members']
        member_lookup = dict()
        for member in members:
            member_lookup[member['id']] = member['firstName'] + ' ' + member['lastName']
        teams = team_data['teams']
        team_id = 1
        for team in teams:
            Teams[team_id] = {'ownerNames': ', '.join([member_lookup[member_id] for member_id in team['owners']]),
                              'teamName': team['location'] + " " + team['nickname'],
                              'record': str(team['record']['overall']['wins']) + '-' + str(team['record']['overall']['ties']) + '-' + str(team['record']['overall']['losses']),
                              'winPercentage': team['record']['overall']['percentage'],
                              'pointsAgainst': team['record']['overall']['pointsAgainst'],
                              'pointsFor': team['record']['overall']['pointsFor'],
                              'drops': team['transactionCounter']['drops'],
                              'acquisitions': team['transactionCounter']['acquisitions'],
                              'trades': team['transactionCounter']['trades']
                              }
            team_id += 1
        #return self.fetch("mTeam")
        return Teams
    
    def fetch_rosters(self):
        roster_data = self.fetch("mRoster")
        Rosters = dict()
        teams = roster_data['teams']
        for team in teams:
            team_id = team['id']
            roster_entries = team['roster']['entries']
            Rosters[team_id] = {'players': [entry['playerPoolEntry']['player']['fullName'] for entry in roster_entries],
                                'positions': [entry['playerPoolEntry']['player']['defaultPositionId'] for entry in roster_entries]}
        return Rosters
    
    def fetch_draft(self):
        #TODO
        return self.fetch("mDraftDetail")
    
    def fetch_matchups(self):
        matchup_data = self.fetch("mMatchup")
        Matchups = dict()
        matchups = matchup_data['schedule']
        for matchup in matchups:
            matchup_id = matchup['id']
            Matchups[matchup_id] = {'week': matchup['matchupPeriodId'],
                                    'homeTeam': matchup['home']['teamId'],
                                    'homeScore': matchup['home']['totalPoints'],
                                    'awayTeam': matchup['away']['teamId'],
                                    'awayScore': matchup['away']['totalPoints'],
                                    'winner': matchup['home']['teamId'] if matchup['winner'] == "HOME" else matchup['away']['teamId']}
        return Matchups


# In[ ]:




