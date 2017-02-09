"""
This example starts by getting the summoner information for every summoner in the
Masters tier. It then goes through those summoners, pulls their matchlist (getting
all matches after patch 5.14 started), and then goes through their matchlist and
pulls every game.
If you have an SQLAlchemy database set up, all of this information will be stored
automatically.
In addition, we definte a helpful get_match function that automatically retries a
failed match request.
"""

import os
from datetime import datetime
import pandas as pd
from cassiopeia import riotapi
import csv
from cassiopeia.type.api.exception import APIError
from cassiopeia.type.core.common import LoadPolicy
from cassiopeia.type.api.store import SQLAlchemyDB

def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    os.environ["DEV_KEY"] = "94e831f6-ef9f-4823-81fc-cfc9342f4428"
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.eager)

    filename = "master_data_26Dec2016.csv"
    data_file = open(filename, 'wt')
    data_out = csv.writer(data_file)
    data_out.writerow(('matchid', 'versionpatch', 'matchdate', 'maptype', 'queue', 'p_names', 'p_sides', 'p_champs', 'p_lanes', 'p_roles', 'p_golds', 'p_wins'))	#'Attributes',

    # Load and connect to your database. (Comment this code to use local memory. Don't forget to comment db.close() below too.)
    # db = SQLAlchemyDB("mysql+mysqlconnector", "databse_hostname", "database_name", "username", "password")
    # riotapi.set_data_store(db)

    # Gather master names
    master = [entry.summoner for entry in riotapi.get_challenger()]
    mastertests = master
    print("Pulled Master tier. Got {0} summoners.".format(len(master)))

    #Make empty lists for match information
    matchid = []
    versionpatch = []
    matchdate = []
    maptype = []
    queue = []

    p_names = []
    p_sides = []
    p_champs = []
    p_lanes = []
    p_roles = []
    p_golds = []
    p_wins= []

    #Define a start date, and then for each player in the master list, get the match ID number
    gather_start = datetime(2016, 12, 26)  # year month date hour minute

    for summoner in master:
        for match in summoner.match_list(begin_time=gather_start):
            # If you are connected to a database, the match will automatically be stored in it without you having to do anything.
            # Simply pull the match, and it's in your database for whenever you need it again!
            # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
            # and therefore will not count against your rate limit. This is true of all datatypes, not just Match.
            match = get_match(match)
            print("Got {0}".format(match))

            #Then save the match information to some empty lists
            matchid.append(match.id)
            versionpatch.append(match.version)
            matchdate.append(match.creation)
            maptype.append(match.map)
            queue.append(match.queue)

            #Now make empty lists for the player information
            p1name = []
            p1side = []
            p1champ = []
            p1lane = []
            p1role = []
            p1gold = []
            p1win = []

            #Make a loop to get the rest of the participants
            for part in match.participants:
                p1name.append(part.summoner_name)
                p1side.append(part.side)
                p1champ.append(part.champion.name)
                p1lane.append(part.timeline.lane)
                p1role.append(part.timeline.role)
                p1gold.append(part.stats.gold_earned)
                p1win.append(part.stats.win)

            #Save information into the lists
            p_names.append(p1name)
            p_sides.append(p1side)
            p_champs.append(p1champ)
            p_lanes.append(p1lane)
            p_roles.append(p1role)
            p_golds.append(p1gold)
            p_wins.append(p1win)

    #db.close()
    columns = ['matchid', 'versionpatch', 'matchdate', 'maptype', 'queue', 'p_names', 'p_sides', 'p_champs', 'p_lanes', 'p_roles', 'p_golds', 'p_wins']
    df = pd.DataFrame([matchid, versionpatch, matchdate, maptype, queue, p_names, p_sides, p_champs, p_lanes, p_roles, p_golds, p_wins], index = columns)
    df = df.T

    with open(filename, 'a') as f:
        df.to_csv(f, header=False)

    print("Saved to {0}".format(filename))
    #print(df)

    data_file = close()


def get_match(reference):
    """ Try to pull the referenced match from Riot's servers. If we can an error that
        we should retry, we will. If it fails a second time, we just skip it.
    """
    try:
        return riotapi.get_match(reference)
    except APIError as error:
        # Try Again Once
        if error.error_code in [500]:
            try:
                return riotapi.get_match(reference)
            except APIError as another_error:
                if another_error.error_code in [500, 400, 404]:
                    pass
                else:
                    raise another_error

        # Skip
        elif error.error_code in [400, 404]:
            pass

        # Fatal
        else:
            raise error


if __name__ == "__main__":
    main()
