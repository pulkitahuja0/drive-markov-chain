<script lang="ts">
	import DataBox from '$lib/components/DataBox.svelte';
	import { createKey, downToText, getKey, stateMatcher } from '$lib/helpers.js';

	// Use string representations for inputs to remove leading zeroes
	let yardsToGoRaw = $state('10');
	let yardsFromEndZoneRaw = $state('75');

	let down = $state(1);
	// Number derivations for calculations and lookup
	const yardsToGoNum = $derived.by(() => +yardsToGoRaw);
	const yardsFromEndZoneNum = $derived.by(() => +yardsFromEndZoneRaw);

	const values = {
		get yardsToGo() {
			return `${clamp(yardsToGoNum)}`;
		},
		set yardsToGo(val: string) {
			yardsToGoRaw = val;
		},
		get yardsFromEndZone() {
			return `${clamp(yardsFromEndZoneNum)}`;
		},
		set yardsFromEndZone(val: string) {
			yardsFromEndZoneRaw = val;
		}
	};

	const clamp = (n: number) => Math.min(99, Math.max(0, isNaN(n) ? 0 : n));

	let { data } = $props();

	const { meta, nextPlayStates, endStates, nCounts } = data;

	const currentNextPlayStates = $derived.by(
		() => nextPlayStates[getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum)]
	);

	const currentEndStates = $derived.by(
		() => endStates[getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum)]
	);

	const nCount = $derived.by(() => {
		const key = getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum);
		return nCounts[key] || 0;
	});

	// Variable to help track if using closest state instead of direct state
	const currentlyDisplaying = $derived.by(() =>
		getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum)
	);
</script>

<div class="flex min-h-screen flex-col">
	<div class="grow">
		{#if nextPlayStates && endStates}
			<div class="m-8">
				<div class="grid gap-2 sm:grid-cols-1 md:grid-cols-3">
					<div class="self-start border-2 border-black">
						<div class="m-3">
							<select
								bind:value={down}
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
							<!-- TODO: change 0EXX or X-XX number-like values as 0 -->
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
					/>
					<DataBox label={'End of drive probabilities'} data={currentEndStates} n={nCount} />
				</div>
			</div>
		{/if}

		{#if currentlyDisplaying !== createKey(down, yardsToGoNum, yardsFromEndZoneNum)}
			<div class="m-6 text-center text-lg text-red-500">
				Displaying {downToText(down)} & {(() => {
					const [, y, y2] = stateMatcher(currentlyDisplaying);
					return `${y} ${y2} yards from the end zone`;
				})()}
			</div>
		{/if}
	</div>

	<footer class="mb-6 w-full text-center">
		Data from {meta.first_szn} - {meta.latest_szn} seasons. Check it out on
		<a
			href="https://github.com/pulkitahuja0/drive-markov-chain"
			class="text-blue-400 underline hover:text-blue-600">GitHub.</a
		>
	</footer>
</div>
