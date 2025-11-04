<script lang="ts">
	import { keyToLabel } from '$lib/helpers';

	let { label, data = $bindable() } = $props();

    let top10 = $derived.by(() => {
        let a: [string, number][] = [];
        Object.keys(data).map(key => a.push([key, data[key]]));
        return a.sort((x, y) => y[1] - x[1]).slice(0, 10);
    });
</script>

<div class="self-start border-2 border-black">
	<div class="m-3">
		<div class="text-lg">{label}</div>
		<ul>
			{#each top10 as item}
				<li>{keyToLabel(item[0])}: {Math.round(item[1] * 1000) / 10}%</li>
			{/each}
		</ul>
	</div>
</div>
