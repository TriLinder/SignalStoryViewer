<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import type { Story } from "../../types";

    import StoryCard from "../../components/StoryCard.svelte";

    let stories: Story[] | null = null;
    let loadStoriesIntervalId: number;

    async function loadStories() {
        const response = await fetch("/stories");
        stories = await response.json();
    }

    onMount(function() {
        loadStories();
        loadStoriesIntervalId = setInterval(loadStories, 30*1000);
    });

    onDestroy(function() {
        clearInterval(loadStoriesIntervalId);
    });
</script>

<style>
    .stories {
        display: flex;
        flex-direction: column;
        gap: 15px;

        max-height: 95vh;
        overflow-y: scroll;
        width: 100%;

        align-items: center;
    }

    .empty-set-symbol {
        font-size: 50px;
        text-align: center;
    }
</style>

{#if stories === null}
    Loading..
{:else}
    <div class="stories">
        {#each stories as story}
            <StoryCard {story}/>
        {:else}
            <span class="empty-set-symbol">∅</span>
            There aren't any stories here at the moment. Check back later! :)
        {/each}
    </div>
{/if}