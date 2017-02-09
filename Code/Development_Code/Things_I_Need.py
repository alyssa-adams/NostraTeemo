""" Prints a selection of information about Dyrus' last match.  """

import os
import datetime
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    os.environ["DEV_KEY"] = "94e831f6-ef9f-4823-81fc-cfc9342f4428"
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    gigglepuss = riotapi.get_summoner_by_name("GigglePuss")  # SummonerID is 5908

    match_list = riotapi.get_match_list(gigglepuss)
    match = riotapi.get_match(match_list[0])

    print("Basic match information:")
    print("  Match ID: {0}".format(match.id))
    print("  Version/Patch: {0}".format(match.version))
    print("  Creation date: {0}  (which was {1} ago)".format(match.creation, datetime.datetime.now() - match.creation))
    print("  Duration: {0}".format(match.duration))
    print("  Map: {0}".format(match.map))
    print("  Mode: {0}".format(match.mode))
    print("  Type: {0}".format(match.type))
    print("  Platform: {0}".format(match.platform))
    print("  Queue: {0}".format(match.queue))
    print("  Region: {0}".format(match.region))
    print("  Season: {0}".format(match.season))
    print("  Red Team Bans: {0}".format([ban.champion.name for ban in match.red_team.bans]))
    print("  Blue Team Bans: {0}".format([ban.champion.name for ban in match.blue_team.bans]))

    print()

    champion = match.participants["GigglePuss"].champion

    print("You can use special key-words/key-objects to lookup the participants in the match.")
    print("  Lookup via Summoner:        {0}".format(match.participants[gigglepuss]))
    print("  Lookup via summoner name:   {0}".format(match.participants["GigglePuss"]))
    print("  Lookup via Champion played: {0}".format(match.participants[champion]))
    print("  Lookup via champion name:   {0}".format(match.participants[champion.name]))
