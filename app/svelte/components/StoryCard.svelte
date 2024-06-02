<script lang="ts">
    import { currentPageStore, storyViewPageStory } from "../stores";
    import type { Story } from "../types";

    export let story: Story;

    $: timestampText = new Date(story.timestamp).toLocaleString();

    function onClick() {
        $currentPageStore = "storyView";
        $storyViewPageStory = story;
    }
</script>

<style>
    .avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
    }

    .content {
        border-style: solid;
        border-color: gray;
        border-width: 2px;
        border-radius: 25px;
        padding: 15px;
        background-color: transparent;

        display: flex;
        align-items: center;
        gap: 20px;

        transition: all 0.2s;
    }

    .content:hover {
        transform: scale(1.1);
    }

    .viewed {
        filter: opacity(0.5);
    }

    .text {
        display: flex;
        flex-direction: column;
        text-align: left;
    }
</style>

<button class="content" class:viewed={story.viewed} on:click={onClick}>
    <img class="avatar" src={`/story/${story.id}/avatar`} alt={`${story.sender.name}'s avatar`}>

    <div class="text">
        <span class="name"><b>{story.sender.name}</b></span>
        <span class="date">{timestampText}</span>
    </div>
</button>