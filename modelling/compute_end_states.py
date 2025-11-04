import os
import json

import numpy as np

with open(os.path.join("output", "output_all_freq.json"), "r") as json_file:
    transitions = json.load(json_file)

all_states = set(transitions.keys())
for nxt in transitions.values():
    all_states |= nxt.keys()
all_states = sorted(all_states)

absorbing = [s for s in all_states if s not in transitions or len(transitions[s]) == 0]
transient = [s for s in all_states if s not in absorbing]

# map states → matrix row/col
idx = {s: i for i, s in enumerate(all_states)}

n = len(all_states)
P = np.zeros((n, n))

for s, nxt in transitions.items():
    i = idx[s]
    for t, p in nxt.items():
        P[i, idx[t]] = p

# absorbing states get identity rows
for s in absorbing:
    i = idx[s]
    P[i, i] = 1.0

# reorder: transient first, then absorbing
order = transient + absorbing
idx2 = {s: i for i, s in enumerate(order)}

P2 = P[
    np.ix_([idx[s] for s in order],
           [idx[s] for s in order])
]

t = len(transient)
Q = P2[:t, :t]
R = P2[:t, t:]

I = np.eye(Q.shape[0])
N = np.linalg.inv(I - Q)
B = N @ R   # absorption probabilities matrix

# ---------- FUNCTION (cheap calls) ----------

def end_probs(state):
    if state in absorbing:
        return {state: 1.0}
    
    si = transient.index(state)
    result = {absorbing[j]: float(B[si, j]) for j in range(len(absorbing))}
    return {
        "touchdown": result["touchdown"],
        "punt": result["punt"],
        "bad_fg": result["bad_fg"],
        "made_fg": result["made_fg"],
        "turnover": result["turnover"],
    }

result = {}

for state in transitions.keys():
    result[state] = end_probs(state)

with open(os.path.join("output", "output_all_end_prob.json"), "w") as json_file:
    json.dump(result, json_file)

print("Dumped end state probabilities to output_all_end_prob.json")