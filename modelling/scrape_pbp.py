from collections import defaultdict
import json
import sys
import os

import polars as pl
import nflreadpy as nfl

year = int(sys.argv[1])

pbp = nfl.load_pbp([year]).filter(~pl.col("play_type").is_in(["no_play", "kickoff", "extra_point"]))

data = defaultdict(lambda: defaultdict(int))

grouped = pbp.group_by(["game_id", "drive"], maintain_order=True)

for drive_df in pbp.partition_by(["game_id", "drive"], maintain_order=True):
    if drive_df.select(pl.col("play_type").is_in(["qb_kneel"]).any()).item():
        continue

    for i in range(drive_df.height  - 1):
        prev_play = drive_df.row(i, named=True)
        next_play = drive_df.row(i + 1, named=True)

        prev_play_id = f"{prev_play["down"]}_{prev_play["ydstogo"]}_{prev_play["yardline_100"]}"

        # Check for scoring play
        if next_play["touchdown"] == 1:
            data[prev_play_id]["touchdown"] += 1
            continue
        elif next_play["play_type"] == "field_goal":
            if next_play["field_goal_result"] == "made":
                data[prev_play_id]["made_fg"] += 1
            else:
                data[prev_play_id]["bad_fg"] += 1
            continue

        # Check for turnovers
        if next_play["fourth_down_failed"] == 1 or next_play["interception"] == 1 or next_play["fumble_lost"] == 1:
            data[prev_play_id]["turnover"] += 1
            continue

        if next_play["play_type"] == "pass" or next_play["play_type"] == "rush":
            data[prev_play_id][f"{next_play["down"]}_{next_play["ydstogo"]}_{next_play["yardline_100"]}"] += 1
        elif next_play["play_type"] == "punt":
            data[prev_play_id]["punt"] += 1

file_name = f"output_{year}.json"
filepath = os.path.join("output", file_name)

os.makedirs("output", exist_ok=True)

relative_frequencies = {
    key: {k: v / sum(inner.values()) for k, v in inner.items()}
    for key, inner in data.items()
}

with open(filepath, "w") as json_file:
    json.dump(relative_frequencies, json_file)

print(f"Dumped play by play data state transitions from the {year} season.")