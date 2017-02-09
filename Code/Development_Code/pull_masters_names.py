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

    # Load and connect to your database. (Comment this code to use local memory. Don't forget to comment db.close() below too.)
    # db = SQLAlchemyDB("mysql+mysqlconnector", "databse_hostname", "database_name", "username", "password")
    # riotapi.set_data_store(db)

    # Gather master names
    master = [entry.summoner for entry in riotapi.get_challenger()]
    print("Pulled Master tier. Got {0} summoners.".format(len(master)))


    gather_start = datetime(2016, 12, 26)
    gather_end = datetime(2016, 12, 27)
    for player in master:
        matches = player.match_list(begin_time=gather_start, end_time=gather_end)
        matchestoday = len(matches)
        print(matchestoday)

        for match in matches:
            for participant in match.participants:
                print(participant.champion.name)



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
