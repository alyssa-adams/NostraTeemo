"""
This example is one of the simplest but most useful.
It creates a dictionary mapping of champion IDs to champion names,
and simply prints that dictionary.
"""

import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    os.environ["DEV_KEY"] = "94e831f6-ef9f-4823-81fc-cfc9342f4428"
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    champions = riotapi.get_champions()
    mapping = {champion.name for champion in champions}

    print(mapping)


if __name__ == "__main__":
    main()
