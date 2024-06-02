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

{#if stories === null}
    Loading..
{:else}
    {#each stories as story}
        <StoryCard {story}/>
    {:else}
        There currently aren't any stories. Check back later! :)
    {/each}
{/if}