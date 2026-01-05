import os
import json
from collections import defaultdict

merged_data = defaultdict(lambda: defaultdict(int))

for filename in os.listdir("output"):
    if filename.endswith("szn.json"):
        filepath = os.path.join("output", filename)
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
            for prev_state, _ in data.items():
                for next_state, occurences in data[prev_state].items():
                    merged_data[prev_state][next_state] += occurences

relative_frequencies = {
    k: {ik: iv / sum(inner.values()) if sum(inner.values()) else 0 for ik, iv in inner.items()} for k, inner in merged_data.items()
}

with open(os.path.join("output", "output_all_freq.json"), "w") as json_file:
    json.dump(relative_frequencies, json_file, separators=(",", ":"))

n_counts = { k: sum(v.values()) for k, v in merged_data.items() }

print("Merged all seasons relative frequencies in output_all_freq.json")

with open(os.path.join("output", "n_counts.json"), "w") as json_file:
    json.dump(n_counts, json_file, separators=(",", ":"))

print("Merged all seasons N counts in n_counts.json")
print(f"Total of {len(merged_data.keys())} transient states")
