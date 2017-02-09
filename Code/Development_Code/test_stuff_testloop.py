import os
import datetime
import pandas as pd
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy

def main():

    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    os.environ["DEV_KEY"] = "94e831f6-ef9f-4823-81fc-cfc9342f4428"
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.eager)

    gigglepuss = riotapi.get_summoner_by_name("GigglePuss")

    match_list = riotapi.get_match_list(gigglepuss)
    sub_list = match_list[:10]
    matchid = []
    versionpatch = []
    maptype = []
    queue = []

    p_names = []
    p_sides = []
    p_champs = []
    p_lanes = []
    p_roles = []
    p_golds = []
    p_wins= []


    for i in range(len(sub_list)):
        match = riotapi.get_match(match_list[i])

        matchid.append(match.id)
        versionpatch.append(match.version)
        maptype.append(match.map)
        queue.append(match.queue)

        p1name = []
        p1side = []
        p1champ = []
        p1lane = []
        p1role = []
        p1gold = []
        p1win = []

        for part in match.participants:
            print(part.summoner_name)
            p1name.append(part.summoner_name)
            p1side.append(part.side)
            p1champ.append(part.champion.name)
            p1lane.append(part.timeline.lane)
            p1role.append(part.timeline.role)
            p1gold.append(part.stats.gold_earned)
            p1win.append(part.stats.win)

        p_names.append(p1name)
        p_sides.append(p1side)
        p_champs.append(p1champ)
        p_lanes.append(p1lane)
        p_roles.append(p1role)
        p_golds.append(p1gold)
        p_wins.append(p1win)

    filename = "test_data.csv"
    columns = ['matchid', 'versionpatch', 'maptype', 'queue', 'p_names', 'p_sides', 'p_champs', 'p_lanes', 'p_roles', 'p_golds', 'p_wins']
    df = pd.DataFrame([matchid, versionpatch, maptype, queue, p_names, p_sides, p_champs, p_lanes, p_roles, p_golds, p_wins], index = columns)

    df = df.T
    df.to_csv(filename)

    print(df)

if __name__ == "__main__":
    main()
