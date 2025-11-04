import os
import json

import numpy as np

with open(os.path.join("output", "output_all.json"), "r") as json_file:
    data = json.load(json_file)

states = list(data.keys())
end_states = ["turnover", "touchdown", "punt", "made_fg", "bad_fg"]
transient_states = [s for s in states if not s in end_states]

P = np.zeros((len(states) + len(end_states), len(states) + len(end_states)))
all_states = states + end_states
state_index = {s: i for i, s in enumerate(all_states)}

for s, nexts in data.items():
    i = state_index[s]
    total = sum(nexts.values())
    if total > 0:
        for next_state, count in nexts.items():
            j = state_index[next_state]
            P[i, j] = count / total
    else:
        P[i, i] = 1.0

t_idx = [state_index[s] for s in transient_states]
e_idx = [state_index[s] for s in end_states]

Q = P[np.ix_(t_idx, t_idx)]
R = P[np.ix_(t_idx, e_idx)]

I = np.eye(len(Q))
B = np.linalg.solve(I - Q, R)

result = {
    transient_states[i]: {end_states[j]: B[i, j] for j in range(len(end_states))} for i in range(len(transient_states))
}

with open(os.path.join("output", "output_all_end_state_freq.json"), "w") as json_file:
    json.dump(result, json_file)

print("Dumped end state probabilities for all seasons in output_all_end_state_freq.json")