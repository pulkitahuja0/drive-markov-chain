<script lang="ts">
	import { keyToLabel } from '$lib/helpers';

	let { label, data, n = undefined } = $props();

	// Slices the top 10 next states by probability to display
	// TODO: show more than 10 states if screen space is available
	let top10 = $derived.by(() => {
		let a: [string, number][] = Object.keys(data).map((key) => [key, data[key]]); // [state, prob][]
		return a.sort((x, y) => y[1] - x[1]).slice(0, 10); // Top 10 by probability
	});

	const isEnd = (key: string) => {
		return (
			key == 'touchdown' ||
			key == 'punt' ||
			key == 'turnover' ||
			key == 'bad_fg' ||
			key == 'made_fg' ||
			key == 'safety' ||
			key == 'turnover_on_downs'
		);
	};
</script>

<div class="self-start border-2 border-black">
	<div class="m-3">
		<div class="text-lg">
			{#if n !== undefined}
				{label} (<i>N</i> = {n}):
			{:else}
				{label}:
			{/if}
		</div>
		<ul>
			{#each top10 as item}
				<li>
					<span class={isEnd(item[0]) ? 'font-bold' : ''}>{keyToLabel(item[0])}:</span>
					{Math.round(item[1] * 1000) / 10}%
				</li>
			{/each}
		</ul>
	</div>
</div>
