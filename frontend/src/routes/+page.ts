import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const nextPlayStates = await (await fetch('/data/output_all_freq.json')).json();
	const endStates = await (await fetch('/data/output_all_end_prob.json')).json();
	const nCounts = await (await fetch('/data/n_counts.json')).json();

	const meta = await (await fetch('/data/meta.json')).json();

	return {
		nextPlayStates,
		endStates,
		nCounts,
		meta
	};
};
