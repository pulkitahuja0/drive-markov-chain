<script lang="ts">
	import { keyToLabel } from '$lib/helpers';

	let { label, data = $bindable() } = $props();

	let top10 = $derived.by(() => {
		let a: [string, number][] = [];
		Object.keys(data).map((key) => a.push([key, data[key]]));
		return a.sort((x, y) => y[1] - x[1]).slice(0, 10);
	});

	const isEnd = (key: string) => {
		return (
			key == 'touchdown' ||
			key == 'punt' ||
			key == 'turnover' ||
			key == 'bad_fg' ||
			key == 'made_fg'
		);
	};
</script>

<div class="self-start border-2 border-black">
	<div class="m-3">
		<div class="text-lg">{label}</div>
		<ul>
			{#each top10 as item}
				<li>
					<span class={isEnd(item[0]) ? 'font-bold' : ''}>{keyToLabel(item[0])}</span>: {Math.round(
						item[1] * 1000
					) / 10}%
				</li>
			{/each}
		</ul>
	</div>
</div>
