<script lang="ts">
	import DataBox from '$lib/components/DataBox.svelte';
	import { createKey, downToText, stateMatcher } from '$lib/helpers.js';

	const getKey = (
		states: Record<string, Record<string, number>>,
		down: number,
		yardsToGo: number,
		yardline: number
	) => {
        // If state is already present in data, use it
		if (states.hasOwnProperty(createKey(down, yardsToGo, yardline))) {
			return createKey(down, yardsToGo, yardline);
		}

		const sameDownStates = Object.keys(states).filter((string) => string.startsWith(`${down}.0`));

        // Find state that is closest in yards to go and yards from endzone
		let closestState = [Infinity, Infinity];
		let currClosestDistance = Infinity;

		sameDownStates.map((state) => {
			const [, yardsToGo1, yardline1] = stateMatcher(state);
			const distance = Math.sqrt((yardsToGo - yardsToGo1) ** 2 + (yardline - yardline1) ** 2);

			if (distance < currClosestDistance) {
				currClosestDistance = distance;
				closestState = [yardsToGo1, yardline1];
			}
		});

		return createKey(down, closestState[0], closestState[1]);
	};

	let down = $state(1);
	let yardsToGo = $state(10);
	let yardsFromEndZone = $state(75);

	let { data } = $props();
	let nextPlayStates = data.freqs;
	let endStates = data.endStates;

	let currentNextPlayStates = $state({});
	let currentEndStates = $state({});

    // Variable to help track if using closest state instead of direct state
	let currentlyDisplaying = $state('');

	$effect(() => {
		currentNextPlayStates =
			nextPlayStates[getKey(nextPlayStates, down, yardsToGo, yardsFromEndZone)];
		currentEndStates = endStates[getKey(nextPlayStates, down, yardsToGo, yardsFromEndZone)];

		currentlyDisplaying = getKey(nextPlayStates, down, yardsToGo, yardsFromEndZone);
	});

    // Ensure input is valid
	$effect(() => {
		if (yardsFromEndZone > 100) yardsFromEndZone = 99;
		if (yardsFromEndZone < 0) yardsFromEndZone = 0;
		if (typeof yardsFromEndZone != 'number') yardsFromEndZone = 0;
	});
</script>

{#if currentlyDisplaying !== createKey(down, yardsToGo, yardsFromEndZone)}
	<div class="m-6 text-center text-lg text-red-500">
		Displaying {downToText(down)} & {(() => {
			const [, y, y2] = stateMatcher(currentlyDisplaying);
			return `${y} ${y2} yards from the end zone.`;
		})()}
	</div>
{/if}

{#if nextPlayStates && endStates}
	<div class="m-8">
		<div class="grid gap-2 sm:grid-cols-1 md:grid-cols-3">
			<div class="self-start border-2 border-black">
				<div class="m-3">
					<select
						bind:value={down}
						class="rounded-lg border border-gray-400 bg-gray-50 p-1 focus:border-gray-400"
					>
						<option value={1} selected>1st</option>
						<option value={2}>2nd</option>
						<option value={3}>3rd</option>
						<option value={4}>4th</option>
					</select>
					&
					<input
						bind:value={yardsToGo}
						defaultValue={10}
						step={1}
						type="number"
						class="w-1/10 rounded-lg border border-gray-400 bg-gray-50 p-1 text-center focus:border-gray-400"
					/>
					<input
						bind:value={yardsFromEndZone}
						defaultValue={75}
						type="number"
						min={0}
						max={99}
						step={1}
						class="w-1/8 rounded-lg border border-gray-400 bg-gray-50 p-1 text-center focus:border-gray-400"
					/> yards from the end zone.
				</div>
			</div>
			<DataBox label={'Next play/position probabilities:'} bind:data={currentNextPlayStates} />
			<DataBox label={'End of drive probabilities:'} bind:data={currentEndStates} />
		</div>
	</div>
{/if}
