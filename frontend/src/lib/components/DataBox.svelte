<script lang="ts">
	import { keyToLabel } from '$lib/helpers';

	let { label, data = $bindable() } = $props();
</script>

<div class="self-start border-2 border-black">
	<div class="m-3">
		<div class="text-lg">{label}</div>
		<ul>
			{#each Object.keys(data).slice(0, 10) as key}
				<li>{keyToLabel(key)}: {Math.round(data[key] * 1000) / 10}%</li>
			{/each}
		</ul>
	</div>
</div>
