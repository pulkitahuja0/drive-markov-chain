from collections import defaultdict
import json
import sys
import os

from helpers import most_recent_nfl_szn
import polars as pl
import nflreadpy as nfl

latest_szn = most_recent_nfl_szn()
first_szn = sys.argv[1] if len(sys.argv) > 1 else 2015

# TODO: Parallelize over seasons, merge all scripts into one (only one IO operation per CI job)

for year in range(first_szn, latest_szn + 1):
    pbp = nfl.load_pbp([year]).filter(~pl.col("play_type").is_in(["no_play", "kickoff", "extra_point"]))

    data = defaultdict(lambda: defaultdict(int))

    end_states = set(["touchdown", "made_fg", "bad_fg", "turnover", "punt"])

    for drive_df in pbp.partition_by(["game_id", "drive"], maintain_order=True):
        if drive_df.select(pl.col("play_type").is_in(["qb_kneel"]).any()).item():
            continue

        last_play = drive_df.row(drive_df.height - 1, named=True)

        # If a drive doesn't end with a turnover, score or punt, shouldn't be used in data
        if not (last_play["play_type"] == "punt" or last_play["touchdown"] == 1 or last_play["play_type"] == "field_goal" or last_play["interception"] == 1 or last_play["fumble_lost"] == 1 or last_play["fourth_down_failed"] == 1):
            continue

        for i in range(drive_df.height):
            play = drive_df.row(i, named=True)
            play_id = f"{play["down"]}_{play["ydstogo"]}_{play["yardline_100"]}"

            if play["extra_point_attempt"] == 1 or play["two_point_attempt"] == 1: # Skip xp or 2pt plays
                continue

            if (i != 0):
                prev_play = drive_df.row(i - 1, named=True)
                prev_play_id = f"{prev_play["down"]}_{prev_play["ydstogo"]}_{prev_play["yardline_100"]}"
                data[prev_play_id][play_id] += 1

            # Check interception first to mark pick six as turnover
            if play["interception"] == 1:
                data[play_id]["turnover"] += 1
                continue

            # Check field goal before fumble to mark blocked/recovered FG as bad fg instead of turnover
            if play["play_type"] == "field_goal":
                if play["field_goal_result"] == "made":
                    data[play_id]["made_fg"] += 1
                else:
                    data[play_id]["bad_fg"] += 1
                continue

            # Check punt before fumble to mark muffed punt as punt instead of turnover
            if play["play_type"] == "punt":
                data[play_id]["punt"] += 1
                continue

            # Check fumble lost before touchdown to mark fumble six as turnover instead of touchdown
            if play["fumble_lost"] == 1:
                data[play_id]["turnover"] += 1
                continue

            if play["touchdown"] == 1:
                data[play_id]["touchdown"] += 1
                continue
            elif play["safety"] == 1:
                data[play_id]["safety"] += 1
                continue


            if play["fourth_down_failed"] == 1:
                data[play_id]["turnover_on_downs"] += 1
                continue


    file_name = f"output_{year}_szn.json"
    filepath = os.path.join("output", file_name)

    os.makedirs("output", exist_ok=True)

    with open(filepath, "w") as json_file:
        json.dump(data, json_file, separators=(",", ":"))

    print(f"Dumped {len(data.keys())} play by play data state transitions from the {year} season.")