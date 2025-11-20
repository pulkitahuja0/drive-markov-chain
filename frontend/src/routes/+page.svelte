<script lang="ts">
	import DataBox from '$lib/components/DataBox.svelte';
	import { createKey, downToText, getKey, stateMatcher } from '$lib/helpers.js';

	// Use string representations for inputs to remove leading zeroes
	let yardsToGo = $state("10");
	let yardsFromEndZone = $state("75");

	let down = $state(1);
	// Number derivations for calculations and lookup
	let yardsToGoNum = $derived.by(() => parseInt(yardsToGo));
	let yardsFromEndZoneNum = $derived.by(() => parseInt(yardsFromEndZone));

	let { data } = $props();
	const nextPlayStates = data.freqs;
	const endStates = data.endStates;
	const { meta } = data;

	let currentNextPlayStates = $state({});
	let currentEndStates = $state({});

	// Variable to help track if using closest state instead of direct state
	let currentlyDisplaying = $state('1.0_10.0_75.0');

	$effect(() => {
		currentNextPlayStates =
			nextPlayStates[getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum)];
		currentEndStates = endStates[getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum)];

		currentlyDisplaying = getKey(nextPlayStates, down, yardsToGoNum, yardsFromEndZoneNum);
	});

	$effect(() => {
		yardsToGo = `${Math.min(99, Math.max(0, yardsToGoNum))}`;
	});

	$effect(() => {
		yardsFromEndZone = `${Math.min(99, Math.max(0, yardsFromEndZoneNum))}`;
	});
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
							<!-- TODO: better input validation -->
							<input
								bind:value={yardsToGo}
								defaultValue={10}
								step={1}
								min={0}
								max={99}
								type="number"
								class="w-1/10 rounded-lg border border-gray-400 bg-gray-50 p-1 text-center focus:border-gray-400"
								aria-label="Yards from first down/goal"
							/>
							<input
								bind:value={yardsFromEndZone}
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
					<DataBox label={'Next play/position probabilities:'} bind:data={currentNextPlayStates} />
					<DataBox label={'End of drive probabilities:'} bind:data={currentEndStates} />
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
