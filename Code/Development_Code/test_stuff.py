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

    p1name = []
    p1side = []
    p1champ = []
    p1lane = []
    p1role = []
    p1gold = []
    p1win = []


    for i in range(len(sub_list)):
        match = riotapi.get_match(match_list[i])

        matchid.append(match.id)
        versionpatch.append(match.version)
        maptype.append(match.map)
        queue.append(match.queue)

        p1name.append(match.participants[0].summoner_name)
        p1side.append(match.participants[0].side)
        p1champ.append(match.participants[0].champion.name)
        p1lane.append(match.participants[0].timeline.lane)
        p1role.append(match.participants[0].timeline.role)
        p1gold.append(match.participants[0].stats.gold_earned)
        p1win.append(match.participants[0].stats.win)

    filename = "test_data.csv"
    columns = ['matchid', 'versionpatch', 'maptype', 'queue', 'p1name', 'p1side', 'p1champ', 'p1lane', 'p1role', 'p1gold', 'p1win']
    df = pd.DataFrame([matchid, versionpatch, maptype, queue, p1name, p1side, p1champ, p1lane, p1role, p1gold, p1win], index = columns)

    df = df.T
    df.to_csv(filename)

    print(df)

if __name__ == "__main__":
    main()
