#!/usr/bin/env python
# coding: utf-8

# In[60]:


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
        return self.fetch("mTeam")
        #return Teams
    
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
    
    def fetch_players(self):
        return self.fetch("mMatchup&scoringPeriodId=1")
    
    def fetch_matchup_rosters(self):
        Matchups = dict()
        for i in range(1, 20):
            matchup_data = self.fetch("mMatchup&scoringPeriodId=" + str(i))
            matchups = matchup_data['schedule']
#             reader = pprint.PrettyPrinter()
#             reader.pprint(matchups)
            for matchup in matchups:
                matchup_id = matchup['id']
                if 'rosterForCurrentScoringPeriod' not in matchup['home'].keys():
                    continue
                Matchups[matchup_id] = {'week': matchup['matchupPeriodId'],
                                        'homeTeamId': matchup['home']['teamId'],
                                        'homeScore': matchup['home']['totalPoints'],
                                        'homeRoster': [entry['playerPoolEntry']['player']['fullName'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'homeLineup': [entry['lineupSlotId'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'homeRosterScore': [entry['playerPoolEntry']['appliedStatTotal'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayTeamId': matchup['away']['teamId'],
                                        'awayScore': matchup['away']['totalPoints'],
                                        'awayRoster': [entry['playerPoolEntry']['player']['fullName'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayLineup': [entry['lineupSlotId'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayRosterScore': [entry['playerPoolEntry']['appliedStatTotal'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'winner': matchup['home']['teamId'] if matchup['winner'] == "HOME" else matchup['away']['teamId']}
        return Matchups
    
    def fetch_matchups(self):
        matchup_data = self.fetch("mMatchup")
        Matchups = dict()
        matchups = matchup_data['schedule']
        for matchup in matchups:
            matchup_id = matchup['id']
            Matchups[matchup_id] = {'week': matchup['matchupPeriodId'],
                                    'homeTeamId': matchup['home']['teamId'],
                                    'homeScore': matchup['home']['totalPoints'],
                                    'awayTeamId': matchup['away']['teamId'],
                                    'awayScore': matchup['away']['totalPoints'],
                                    'winner': matchup['home']['teamId'] if matchup['winner'] == "HOME" else matchup['away']['teamId']}
        return Matchups


# In[61]:


year = "2020"
leagueID = "139889"
espn_s2 = "AEBVAY4IP16BsQVvRgpY1hGOur4OKjZCVh6vfBIibHEoA5BHQCg3rZGBvbNbuESU3bQlfQzdveoAqNcmIhoBoO10gq2K%2FOhtdYamn6aQBihs%2FydsgoJehuJgLwAIdcaXlnehxcpTltR58fP0cX18vjZReJjo0OjZGUSOr3ff0Iuz1Ztt8c4rUkFJVTd8cEd%2BT76%2Bvva8s5iQGAfKTUfPA9P2k6xC33qYcaH%2FIYykwIC00PKoJOlysod9yM5bUrA39lpJ2WZQfdICgqXt5zu%2FYaDpiXVznvExI4BIoEFnEVfs3w%3D%3D"
swid = "{65C194B8-D67C-4A07-8990-988E5F391434}"

My_League = League(year, leagueID, espn_s2, swid)

reader = pprint.PrettyPrinter()
reader.pprint(My_League.fetch_matchup_rosters())


# In[ ]:




