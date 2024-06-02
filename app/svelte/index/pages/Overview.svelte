<script lang="ts">
    import { onMount } from "svelte";
    import type { Story } from "../../types";

    import StoryCard from "../../components/StoryCard.svelte";

    let stories: Story[] | null = null;

    async function loadStories() {
        const response = await fetch("/stories");
        stories = await response.json();
    }

    onMount(loadStories);
</script>

<style>
    .stories {
        display: flex;
        flex-direction: column;
        gap: 15px;
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
            There currently aren't any stories. Check back later! :)
        {/each}
    </div>
{/if}