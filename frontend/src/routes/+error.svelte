<script>
    import { page } from '$app/state';
</script>

<div class="flex flex-col items-center justify-center min-h-screen gap-4 text-center">
    <h1 class="text-4xl font-bold m-0">Oops!</h1>
    <p class="text-lg text-gray-600 my-2">{page.status} - {page.error?.message || 'Something went wrong'}</p>
    <a href="/" class="mt-4 px-6 py-3 bg-blue-600 text-white rounded transition-colors hover:bg-blue-700">Go back home</a>
</div>