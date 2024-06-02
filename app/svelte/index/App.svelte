<script lang="ts">
	import { currentPageStore } from "../stores";

	import Overview from "./pages/Overview.svelte";
</script>

<style>
	.center {
		display: flex;
		justify-content: center;
	}

	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		max-width: 800px;
		width: 100%;
		height: 100vh;
	}
</style>

<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</svelte:head>

<div class="center">
	<div class="content">
		{#if $currentPageStore == "overview"}
			<Overview/>
		{/if}
	</div>
</div>