# Add year to help with Unique Identifier
MATCHUP_DATA_2018$Year <- 2018
MATCHUP_DATA_2018 <- MATCHUP_DATA_2018[,c(9, 1, 2, 3, 4, 5, 6, 7)]

MATCHUP_DATA_2019$Year <- 2019
MATCHUP_DATA_2019 <- MATCHUP_DATA_2019[,c(9, 1, 2, 3, 4, 5, 6, 7)]

MATCHUP_DATA_2020$Year <- 2020
MATCHUP_DATA_2020 <- MATCHUP_DATA_2020[,c(9, 1, 2, 3, 4, 5, 6, 7)]

MATCHUP_DATA_2021$Year <- 2021
MATCHUP_DATA_2021 <- MATCHUP_DATA_2021[,c(9, 1, 2, 3, 4, 5, 6, 7)]

#MATCHUP_DATA_2022$Year <- 2022
#MATCHUP_DATA_2022 <- MATCHUP_DATA_2022[,c(9, 1, 2, 3, 4, 5, 6, 7)]

ALL_MATCHUP_DATA <- rbind(MATCHUP_DATA_2018, MATCHUP_DATA_2019, MATCHUP_DATA_2020, MATCHUP_DATA_2021)
write.csv(ALL_MATCHUP_DATA,"/Users/wolschlag/Documents/GitHub/IAA21FantasyFootball/Andrew Wolschlag/ALL_MATCHUP_DATA.csv", row.names = FALSE)
# Can also create more views of matchups
# All REGULAR SEASON
REG_SZN_2018 <- MATCHUP_DATA_2018 %>%
  filter(Week <= 12)
REG_SZN_2019 <- MATCHUP_DATA_2019 %>%
  filter(Week <= 12)
REG_SZN_2020 <- MATCHUP_DATA_2020 %>%
  filter(Week <= 11)
REG_SZN_2021 <- MATCHUP_DATA_2021 %>%
  filter(Week <= 11)

ALL_REG_SZN <- rbind(REG_SZN_2018, REG_SZN_2019, REG_SZN_2020, REG_SZN_2021)
# ALL post RRR Era
ALL_POST_RRR <- rbind(REG_SZN_2020, REG_SZN_2021)

# Use DPLYR to create unique views
# Transaction Log of where a player has been every week
    # From there you can get point total by owner
        # Comparison of performance for one team vs another
    # Benched vs Active
    # Points for 

# Player's Fantasy Career
# All Weekly Moves for a player
Career_Tracker <- ALL_MATCHUP_DATA %>% 
  filter(Player == "Austin Ekeler")
# Points by Team
Career_Tracker <- ALL_MATCHUP_DATA %>% 
  filter(Player == "Austin Ekeler") %>%
  group_by(Team) %>%
  summarize(tot_pts = sum(Points))

# Avg Start v Bench Scoring
Career_Tracker <- ALL_MATCHUP_DATA %>% 
  filter(Player == "Austin Ekeler") %>%
  group_by(Slot) %>%
  summarize(avg_score = mean(Points))

# Plotting
summary(Career_Tracker)
plot(Career_Tracker$Points)
hist(Career_Tracker$Points)
