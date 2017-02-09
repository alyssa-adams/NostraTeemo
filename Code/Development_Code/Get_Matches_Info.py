""" Prints a selection of information about GigglePuss' last match.  """

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
    match = riotapi.get_match(match_list[0])

    print("  Match ID: {0}".format(match.id))
    print("  Version/Patch: {0}".format(match.version))
    print("  Map: {0}".format(match.map))
    print("  Queue: {0}".format(match.queue))

    print()

    # Print participant information (not summoner information)
    for participant in match.participants:
        print("  {0}".format(participant.summoner_name))
        print("  {0}".format(participant.summoner_id))
        print("    Champion: {0}".format(participant.champion.name))
        print("    Won: {0}".format(participant.stats.win))
        print("    Side: {0}".format(participant.side))
        print("    Gold earned: {0}".format(participant.stats.gold_earned))
        print("    Lane: {0}".format(participant.timeline.lane))
        print("    Role: {0}".format(participant.timeline.role))










    matchid = []
	versionpatch = []
	maptype = []
	queue = []

	p1name = []
    p1id = []
    p1champ = []
    p1win = []
    p1side = []
    p1goldearned = []
    p1lane = []
    p1role = []

    p2name = []
    p2id = []
    p2champ = []
    p2win = []
    p2side = []
    p2goldearned = []
    p2lane = []
    p2role = []

    p3name = []
    p3id = []
    p3champ = []
    p3win = []
    p3side = []
    p3goldearned = []
    p3lane = []
    p3role = []

    p4name = []
    p4id = []
    p4champ = []
    p4win = []
    p4side = []
    p4goldearned = []
    p4lane = []
    p4role = []

    p5name = []
    p5id = []
    p5champ = []
    p5win = []
    p5side = []
    p5goldearned = []
    p5lane = []
    p5role = []

    p6name = []
    p6id = []
    p6champ = []
    p6win = []
    p6side = []
    p6goldearned = []
    p6lane = []
    p6role = []

    p7name = []
    p7id = []
    p7champ = []
    p7win = []
    p7side = []
    p7goldearned = []
    p7lane = []
    p7role = []

    p8name = []
    p8id = []
    p8champ = []
    p8win = []
    p8side = []
    p8goldearned = []
    p8lane = []
    p8role = []

    p9name = []
    p9id = []
    p9champ = []
    p9win = []
    p9side = []
    p9goldearned = []
    p9lane = []
    p9role = []

    p10name = []
    p10id = []
    p10champ = []
    p10win = []
    p10side = []
    p10goldearned = []
    p10lane = []
    p10role = []

    sub_list = match_list[:10]
	for match in sub_list:

		matchid.append(match.id)
		versionpatch.append(match.version)
		maptype.append(match.map)
		queue.append(match.queue)

        p1name.append(Drunk.alpha)
        p1id.append(Drunk.alpha)
        p1champ.append(Drunk.alpha)
        p1win.append(Drunk.alpha)
        p1side.append(Drunk.alpha)
        p1goldearned.append(Drunk.alpha)
        p1lane.append(Drunk.alpha)
        p1role.append(Drunk.alpha)

	filename = "%i_final_data.csv" %exp
	columns = ['alphas', 'strategies', 'payoffs', 'beers', 'cooperator_alphas' ]
	df = pd.DataFrame([alphas, strategies, payoffs, beers, cooperator_alphas], index = columns)

	df = df.T
	df.to_csv(filename)

	print df








if __name__ == "__main__":
    main()
