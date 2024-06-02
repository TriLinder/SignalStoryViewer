<script lang="ts">
	import { onMount } from "svelte";
	import { currentPageStore } from "../stores";

	import Overview from "./pages/Overview.svelte";
	import StoryView from "./pages/StoryView.svelte";

	onMount(function() {
		document.addEventListener("keydown", function(event) {
			if (event.key == "Escape") {
				$currentPageStore = "overview";
			}
		});
	});
</script>

<style>
	:global(*) {
		font-family: sans-serif;
		font-size: 16px;
	}

	.center {
		display: flex;
		justify-content: center;
	}

	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		width: 100%;
		height: 100vh;
	}
</style>

<div class="center">
	<div class="content">
		{#if $currentPageStore == "overview"}
			<Overview/>
		{:else if $currentPageStore == "storyView"}
			<StoryView/>
		{/if}
	</div>
</div>