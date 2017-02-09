"""
This example starts by getting the summoner information for every summoner in the
Masters tier. It then goes through those summoners, pulls their matchlist (getting
all matches after patch 5.14 started), and then goes through their matchlist and
pulls every game.
In addition, we definte a helpful get_match function that automatically retries a
failed match request.
"""

from cassiopeia import riotapi
from datetime import datetime
import pandas as pd
import datreant.core as dtr


def main():
    riotapi.set_region("NA")
    riotapi.set_api_key("94e831f6-ef9f-4823-81fc-cfc9342f4428")

    masters = [entry.summoner for entry in riotapi.get_challenger()]
    matches = dtr.Tree('Challenger_Patch6.24')
    matches.make()

    for master in masters[93:]:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {champion}".format(champion=master.name))
        matchlist = master.match_list(begin_time=datetime(2016, 12, 7), end_time=datetime(2016, 12, 21))
        print(len(matchlist))

        for game in matchlist:
            match = game.match()
            path0 = matches[str(match.id) + '/']
            path0
            m0 = dtr.Treant(path0)
            m0.path

            m0.categories['MatchID'] = match.id
            m0.categories['VersionPatch'] = match.version
            m0.categories['Year'] = match.creation.year
            m0.categories['Month'] = match.creation.month
            m0.categories['Day'] = match.creation.day
            m0.categories['Hour'] = match.creation.hour
            m0.categories['Duration'] = str(match.duration)
            m0.categories['Map'] = str(match.map)
            m0.categories['Mode'] = str(match.mode)
            m0.categories['Type'] = str(match.type)
            m0.categories['Platform'] = str(match.platform)
            m0.categories['Queue'] = str(match.queue)
            m0.categories['Region'] = str(match.region)
            m0.categories['Season'] = str(match.season)
            m0.categories['Red Ban 1'] = [ban.champion.name for ban in match.red_team.bans][0]
            m0.categories['Red Ban 2'] = [ban.champion.name for ban in match.red_team.bans][1]
            if len([ban.champion.name for ban in match.red_team.bans]) > 2:
                m0.categories['Red Ban 3'] = [ban.champion.name for ban in match.red_team.bans][2]
            m0.categories['Blue Ban 1'] = [ban.champion.name for ban in match.blue_team.bans][0]
            if len([ban.champion.name for ban in match.blue_team.bans]) > 1:
                m0.categories['Blue Ban 2'] = [ban.champion.name for ban in match.blue_team.bans][1]
            if len([ban.champion.name for ban in match.blue_team.bans]) > 2:
                m0.categories['Blue Ban 3'] = [ban.champion.name for ban in match.blue_team.bans][2]

            p1 = []
            p1champ = []
            p1win = []
            p1side = []
            p1kills = []
            p1deaths = []
            p1assists = []
            p1kda = []
            p1cs = []
            p1spell1 = []
            p1spell2 = []
            p1level = []
            p1fb = []
            p1gold = []
            p1spent = []
            p1item1 = []
            p1item2 = []
            p1item3 = []
            p1item4 = []
            p1item5 = []
            p1item6 = []
            p1mdamage = []
            p1pdamage = []
            p1lane = []
            p1role = []

            for participant in match.participants:

                p1.append(participant.summoner_name)
                p1champ.append(participant.champion.name)
                p1win.append(participant.stats.win)
                p1side.append(participant.side)
                p1kills.append(participant.stats.kills)
                p1deaths.append(participant.stats.deaths)
                p1assists.append(participant.stats.assists)
                p1kda.append(participant.stats.kda)
                p1cs.append(participant.stats.cs)
                p1spell1.append(participant.summoner_spell_d)
                p1spell2.append(participant.summoner_spell_f)
                p1level.append(participant.stats.champion_level)
                p1fb.append(participant.stats.first_blood)
                p1gold.append(participant.stats.gold_earned)
                p1spent.append(participant.stats.gold_spent)
                items = [item.name if item is not None else None for item in participant.stats.items]
                p1item1.append(items[0])
                p1item2.append(items[1])
                p1item3.append(items[2])
                p1item4.append(items[3])
                p1item5.append(items[4])
                p1item6.append(items[5])
                p1mdamage.append(participant.stats.magic_damage_dealt)
                p1pdamage.append(participant.stats.physical_damage_dealt)
                p1lane.append(participant.timeline.lane)
                p1role.append(participant.timeline.role)


            columns = ['Player Name', 'Champion', 'Win', 'Side', 'Kills', 'Deaths', 'Assists', 'KDA', 'CS', 'SSpell 1', 'SSpell 2', 'End Level', 'First Blood?', 'Gold Earned', 'Gold Spent', 'Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Magic Dmg', 'Physical Dmg', 'Lane', 'Role']
            df = pd.DataFrame([p1, p1champ, p1win, p1side, p1kills, p1deaths, p1assists, p1kda, p1cs, p1spell1, p1spell2, p1level, p1fb, p1gold, p1spent, p1item1, p1item2, p1item3, p1item4, p1item5, p1item6, p1mdamage, p1pdamage, p1lane, p1role], index = columns)
            df = df.T

            m0.draw()
            m0['match.csv']
            filename = "match.csv"
            df.to_csv(m0[filename].abspath)

            #save df to csv with Treants tag
            #one file per match


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
            print(master.name)
            for index, master in enumerate(masters):
                print(index, master)


if __name__ == "__main__":
    main()
