<script lang="ts">
	import { pushState, replaceState } from '$app/navigation';
	import { page } from '$app/state';
	import DataBox from '$lib/components/DataBox.svelte';
	import { createKey, downToText, getKey, stateMatcher } from '$lib/helpers.js';

	const clamp = (n: number) => Math.min(99, Math.max(0, isNaN(n) ? 0 : n));

	const DEFAULT_PAGE_STATE: Required<App.PageState> = {
		down: 1,
		yardsToGo: '10',
		yardsFromEndZone: '75'
	};

	const currState = $derived({ ...DEFAULT_PAGE_STATE, ...page.state });

	// Number derivations for calculations and lookup
	const yardsToGoNum = $derived(+currState.yardsToGo);
	const yardsFromEndZoneNum = $derived(+currState.yardsFromEndZone);

	const updateState = (partial: App.PageState, { push = false } = {}) => {
		const next = { ...currState, ...partial };
		if (push) {
			pushState('', next);
		} else {
			replaceState('', next);
		}
	};

	const values = {
		get down() {
			return currState.down;
		},
		set down(val: number) {
			updateState({ down: val });
		},
		get yardsToGo() {
			return `${clamp(yardsToGoNum)}`;
		},
		set yardsToGo(val: string) {
			updateState({ yardsToGo: val });
		},
		get yardsFromEndZone() {
			return `${clamp(yardsFromEndZoneNum)}`;
		},
		set yardsFromEndZone(val: string) {
			updateState({ yardsFromEndZone: val });
		}
	};

	let { data } = $props();

	const { meta, nextPlayStates, endStates, nCounts } = data;

	// Get the closest matching state key
	const {
		key: currKey,
		yardsToGo: currYardsToGo,
		yardline: currYardsFromEndZone
	} = $derived(getKey(nextPlayStates, currState.down, yardsToGoNum, yardsFromEndZoneNum));

	const currentNextPlayStates = $derived(nextPlayStates[currKey]);

	const currentEndStates = $derived(endStates[currKey]);

	const nCount = $derived(nCounts[currKey] || 0);

	const selectState = (key: string) => {
		const [newDown, newYardsToGo, newYardline] = stateMatcher(key);
		updateState(
			{ down: newDown, yardsToGo: `${newYardsToGo}`, yardsFromEndZone: `${newYardline}` },
			{ push: true }
		);
	};
</script>

<svelte:head>
	<script type="application/ld+json">
		{
			"@context": "https://schema.org",
			"@type": "WebSite",
			"name": "NFL Drives",
			"description": "An interactive tool for analyzing football drive probabilities using Markov chains.",
			"url": "https://drives.ahujapulkit.com",
			"author": {
				"@type": "Person",
				"name": "Pulkit Ahuja",
				"gender": "Male",
				"url": "https://ahujapulkit.com"
			}
		}
	</script>
</svelte:head>

<div class="flex min-h-screen flex-col">
	<div class="grow">
		{#if nextPlayStates && endStates}
			<div class="m-8">
				<div class="grid gap-2 sm:grid-cols-1 md:grid-cols-3">
					<div class="self-start border-2 border-black">
						<div class="m-3">
							<select
								bind:value={values.down}
								class="rounded-lg border border-gray-400 bg-gray-50 p-1 focus:border-gray-400"
								aria-label="Down"
							>
								<option value={1} selected>1st</option>
								<option value={2}>2nd</option>
								<option value={3}>3rd</option>
								<option value={4}>4th</option>
							</select>
							&
							<!-- TODO: check if data will have & inches as 0 or 1 yards -->
							<input
								bind:value={values.yardsToGo}
								defaultValue={10}
								step={1}
								min={0}
								max={99}
								type="number"
								class="w-1/10 rounded-lg border border-gray-400 bg-gray-50 p-1 text-center focus:border-gray-400"
								aria-label="Yards from first down/goal"
							/>
							<input
								bind:value={values.yardsFromEndZone}
								defaultValue={75}
								type="number"
								min={0}
								max={99}
								step={1}
								class="w-1/8 rounded-lg border border-gray-400 bg-gray-50 p-1 text-center focus:border-gray-400"
								aria-label="Yards from end zone"
							/> yards from the end zone.
						</div>
					</div>
					<DataBox
						label={'Next play/position probabilities'}
						data={currentNextPlayStates}
						n={nCount}
						onSelectState={selectState}
					/>
					<DataBox label={'End of drive probabilities'} data={currentEndStates} />
				</div>
			</div>
		{/if}

		{#if currKey !== createKey(currState.down, yardsToGoNum, yardsFromEndZoneNum)}
			<div class="m-6 text-center text-lg text-red-500">
				Displaying {downToText(currState.down)} & {currYardsToGo}
				{currYardsFromEndZone} yards from the end zone
			</div>
		{/if}
	</div>

	<footer class="mb-6 w-full text-center">
		Data from {meta.first_szn} - {meta.latest_szn} seasons. Check it out on
		<a
			href="https://github.com/pulkitahuja0/drive-markov-chain"
			target="_blank"
			rel="noopener noreferrer"
			class="text-blue-400 underline hover:text-blue-600">GitHub.</a
		>
	</footer>
</div>
