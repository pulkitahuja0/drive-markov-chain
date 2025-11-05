<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.ico';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<meta name="description" content="Markov chain modelling for National Football League (NFL) drives" />
	<title>NFL Drives</title>
</svelte:head>

{@render children()}
