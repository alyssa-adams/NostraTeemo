"""
This example does a summmoner lookup on Dyrus, then pulls his most recent 20 games.
This data is used to calculate Dyrus' total kills, deaths, assists and average KDA
over those 20 games.
The stats endpoint is then called to lookup this information using Dyrus' entire
ranked history.
"""

import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy, StatSummaryType


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    os.environ["DEV_KEY"] = "94e831f6-ef9f-4823-81fc-cfc9342f4428"
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    gigglepuss = riotapi.get_summoner_by_name("GigglePuss")  # SummonerID is 5908
    # dyrus = riotapi.get_summoner_by_id(5908)  # You could use this as well

    match_list = riotapi.get_match_list(gigglepuss)

    num_matches = 20

    kills = 0
    deaths = 0
    assists = 0

    print("Calculating K/D/A from the past {0} matches...".format(num_matches))

    for i, match_reference in enumerate(match_list[0:num_matches]):
        match = riotapi.get_match(match_reference)
        for participant in match.participants:
            if participant.summoner_id == gigglepuss.id:
                kills += participant.stats.kills
                deaths += participant.stats.kills
                assists += participant.stats.assists
        kda = (kills + assists) / deaths
        print("Rolling K/D/A for {0}:  {1}/{2}/{3} == {4} over most recent {5} matches".format(gigglepuss.name, kills, deaths, assists, round(kda, 3), i + 1))

    print("Final average K/D/A:  {0}/{1}/{2} == {3} over past {4} matches".format(kills, deaths, assists, round(kda, 3), num_matches))

    print()
    print("If we want K/D/A we really should be using the /stats/ endpoint, but it seems to be inaccurate or missing key information.")
    stats = riotapi.get_stats(gigglepuss)
    stats = stats[StatSummaryType.ranked_fives].stats
    print("Total ranked K/D/A for {0}:  {1}/{2}/{3} == {4}".format(gigglepuss.name, stats.kills, stats.deaths, stats.assists, round(stats.kda, 3)))


if __name__ == "__main__":
    main()
