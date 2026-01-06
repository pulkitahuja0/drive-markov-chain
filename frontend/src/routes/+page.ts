import { getKey } from '$lib/helpers';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const nextPlayStates = await (await fetch('/data/output_all_freq.json')).json();
	const endStates = await (await fetch('/data/output_all_end_prob.json')).json();
	const nCounts = await (await fetch('/data/n_counts.json')).json();

	const currentNextPlayStates = nextPlayStates[getKey(nextPlayStates, 1, 10, 75)];
	const currentEndStates = endStates[getKey(endStates, 1, 10, 75)];

	const meta = await (await fetch('/data/meta.json')).json();

	return {
		nextPlayStates,
		endStates,
		nCounts,
		meta,
		currentEndStates,
		currentNextPlayStates
	};
};
