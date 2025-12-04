import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const res1 = await (await fetch('/data/output_all_freq.json')).json();
	const res2 = await (await fetch('/data/output_all_end_prob.json')).json();

	const meta = await (await fetch('/data/meta.json')).json();

	return {
		freqs: res1,
		endStates: res2,
		meta
	};
};
