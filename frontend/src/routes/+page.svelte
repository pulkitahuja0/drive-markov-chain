<script lang="ts">
	import DataBox from "$lib/components/DataBox.svelte";

    const createKey = (down: number, yardsToGo: number, yardline: number) => {
        return `${down}.0_${yardsToGo}.0_${yardline}.0`;
    }

    let down = $state(1);
    let yardsToGo = $state(10);
    let yardline = $state(25);

    let { data } = $props();
    let nextPlayStates = data.freqs;
    let endStates = data.endStates;

    let currentNextPlayStates = $state({});
    let currentEndStates = $state({})

    $effect(() => {
        currentNextPlayStates = nextPlayStates[createKey(down, yardsToGo, yardline)];
        currentEndStates = endStates[createKey(down, yardsToGo, yardline)];
        console.log("change")
    })
</script>


{#if (nextPlayStates && endStates)} 
    <div class="m-8">
        <div class="grid grid-cols-3 gap-2">
            <div class="border-black border-2 self-start">
                <div class="m-3">
                    <select bind:value={down} class="border bg-gray-50 rounded-lg p-1 border-gray-400 focus:border-gray-400">
                        <option value={1} selected>
                            1st
                        </option>
                        <option value={2}>
                            2nd
                        </option>
                        <option value={3}>
                            3rd
                        </option>
                        <option value={4}>
                            4th
                        </option>
                    </select> &
                    <input bind:value={yardsToGo} defaultValue={10} type="text" class="text-center border bg-gray-50 rounded-lg p-1 border-gray-400 focus:border-gray-400 w-1/16"> from the
                    <input bind:value={yardline} defaultValue={25} type="text" class="text-center border bg-gray-50 rounded-lg p-1 border-gray-400 focus:border-gray-400 w-1/14"> yardline.
                </div>
            </div>
            <DataBox label={"Next play probabilities:"} bind:data={currentNextPlayStates} />
            <DataBox label={"End of drive probabilities:"} bind:data={currentEndStates} />
        </div>
    </div>
{/if}