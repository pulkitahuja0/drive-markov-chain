<script>
	import { page } from '$app/state';
</script>

<div class="flex min-h-screen flex-col items-center justify-center gap-4 text-center">
	<h1 class="m-0 text-4xl font-bold">Oops!</h1>
	<p class="my-2 text-lg text-gray-600">
		{page.status} - {page.error?.message || 'Something went wrong'}
	</p>
	<a
		href="/"
		class="mt-4 rounded bg-blue-600 px-6 py-3 text-white transition-colors hover:bg-blue-700"
		>Go back home</a
	>
</div>
