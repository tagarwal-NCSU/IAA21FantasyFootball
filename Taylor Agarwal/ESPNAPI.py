#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pprint
import requests
import pandas as pd
from ESPNIDs import POSITION_MAP
import json

class League:
    
    def __init__(self, year, leagueID, espn_s2, swid):
        self.year = str(year)
        self.leagueID = str(leagueID)
        self.espn_s2 = espn_s2
        self.swid = swid

    def fetch_raw(self, view, headers=None):
        URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/" + self.year + "/segments/0/leagues/" + self.leagueID + "?view=" + view
        r = requests.get(URL, cookies={"espn_s2": self.espn_s2, "swid": self.swid}, headers=headers)
        data = r.json()
        return data

    def fetch_teams(self):
        team_data = self.fetch_raw("mTeam")
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
        return Teams
    
    def fetch_rosters(self):
        roster_data = self.fetch_raw("mRoster")
        Rosters = dict()
        teams = roster_data['teams']
        for team in teams:
            team_id = team['id']
            roster_entries = team['roster']['entries']
            Rosters[team_id] = {'roster': [entry['playerPoolEntry']['player']['fullName'] for entry in roster_entries],
                                'defaultPosition': [entry['playerPoolEntry']['player']['defaultPositionId'] for entry in roster_entries]}
            Rosters[team_id]['defaultPosition'] = [POSITION_MAP[pos] for pos in Rosters[team_id]['defaultPosition']]
        return Rosters
    
    def fetch_draft(self):
        #TODO
        return self.fetch_raw("mDraftDetail")
    
    def fetch_free_agents(self):
        #TODO
        filters = {"players":{"filterStatus":{"value":["FREEAGENT","WAIVERS"]}, 
                              "limit":50,
                              "sortPercOwned":{"sortPriority":1,
                                               "sortAsc":False},
                              "sortDraftRanks":{"sortPriority":100,
                                                "sortAsc":True,
                                                "value":"STANDARD"}
                             }
                  }
        headers = {'x-fantasy-filter': json.dumps(filters)}
        Free_Agents = dict()
        free_agent_data = self.fetch_raw("kona_player_info&scoringPeriodId="+str(i), headers)
        for i, player in enumerate(free_agent_data['players']):
            Free_Agents[j+1] = {'fullName': player['player']['fullName'],
                                       'injured': player['player']['injured'],
                                       'percentOwned': player['player']['ownership']['percentOwned'],
                                       'eligibleSlots': player['player']['eligibleSlots']
                                      }
            Free_Agents[j+1]['eligibleSlots'] = [POSITION_MAP[pos] for pos in Free_Agents[j+1]['eligibleSlots']]
        
        return Free_Agents
        #return self.fetch_raw("kona_player_info", headers)
    
    def fetch_matchup_rosters(self):
        Matchups = dict()
        for i in range(1, 20):
            matchup_data = self.fetch_raw("mMatchup&scoringPeriodId=" + str(i))
            matchups = matchup_data['schedule']
            #reader = pprint.PrettyPrinter()
            #reader.pprint(matchups)
            for matchup in matchups:
                matchup_id = matchup['id']
                if 'rosterForCurrentScoringPeriod' not in matchup['home'].keys():
                    continue
                Matchups[matchup_id] = {'week': matchup['matchupPeriodId'],
                                        'homeTeamId': matchup['home']['teamId'],
                                        'homeScore': matchup['home']['totalPoints'],
                                        'homeRoster': [entry['playerPoolEntry']['player']['fullName'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'homeLineup': [entry['lineupSlotId'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'homeRosterScore': [round(entry['playerPoolEntry']['appliedStatTotal'], 2) for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'homeRosterEligibleSlots': [entry['playerPoolEntry']['player']['eligibleSlots'] for entry in matchup['home']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayTeamId': matchup['away']['teamId'],
                                        'awayScore': matchup['away']['totalPoints'],
                                        'awayRoster': [entry['playerPoolEntry']['player']['fullName'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayLineup': [entry['lineupSlotId'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayRosterScore': [round(entry['playerPoolEntry']['appliedStatTotal'],2) for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'awayRosterEligibleSlots': [entry['playerPoolEntry']['player']['eligibleSlots'] for entry in matchup['away']['rosterForCurrentScoringPeriod']['entries']],
                                        'winner': matchup['home']['teamId'] if matchup['winner'] == "HOME" else matchup['away']['teamId']
                                       }
                Matchups[matchup_id]['homeLineup'] = [POSITION_MAP[pos] for pos in Matchups[matchup_id]['homeLineup']]
                Matchups[matchup_id]['homeRosterEligibleSlots'] = [[POSITION_MAP[pos] for pos in lst] for lst in Matchups[matchup_id]['homeRosterEligibleSlots']]
                Matchups[matchup_id]['awayLineup'] = [POSITION_MAP[pos] for pos in Matchups[matchup_id]['awayLineup']]
                Matchups[matchup_id]['awayRosterEligibleSlots'] = [[POSITION_MAP[pos] for pos in lst] for lst in Matchups[matchup_id]['awayRosterEligibleSlots']]
        return Matchups
    
    def fetch_matchups(self):
        matchup_data = self.fetch_raw("mMatchup")
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

