<script lang="ts">
    import { onMount } from "svelte";
    import { currentPageStore, storyViewPageStory } from "../../stores";
    
    import RelativeDate from "../../components/RelativeDate.svelte";

    $: story = $storyViewPageStory;
    $: mediaSrc = `/story/${story.id}/media`;

    async function markStoryAsViewed() {
        await fetch(`/story/${story.id}/view`);
    }

    async function reply() {
        const replyBody = prompt();
        await fetch(`/story/${story.id}/reply`, {method: "POST", headers: {"Content-Type": "application/json"}, body:JSON.stringify({"body": replyBody})});
    }

    onMount(markStoryAsViewed);
</script>

<style>
    .content {
        overflow: hidden;
    }

    .navbar-container {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        z-index: 5;

        display: flex;
        justify-content: center;
        align-items: center;
    }

    .navbar {
        background-color: rgba(0, 0, 0, .8);

        color: white;

        display: flex;
        align-items: center;
        gap: 15px;

        margin-top: 15px;
        padding: 15px;
    }

    .buttons {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    button {
        font-size: 18px;
    }

    .text {
        display: flex;
        flex-direction: column;
        text-align: left;
    }

    .caption {
        max-width: 250px;
        word-wrap: break-word;
    }

    .date {
        color: lightgray;
    }

    .media {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: black;

        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    img, video {
        max-width: 100%; /* Ensure the media element does not exceed the width of its container */
        max-height: 100%; /* Ensure the media element does not exceed the height of its container */
        object-fit: contain; /* Preserve aspect ratio and fit the whole image/video inside the container */
    }
</style>

<div class="content">
    <div class="navbar-container">
        <div class="navbar">
            <div class="buttons">
                <button class="back-button" on:click={function() {$currentPageStore = "overview"}}>✖</button>
                <button class="reply-button" on:click={reply}>✉︎</button>
            </div>
            <div class="text">
                <span class="name"><b>{story.sender.name}</b></span>
                <span class="date"><RelativeDate timestamp={story.timestamp}/></span>
                {#if story.caption}
                    <p class="caption">{story.caption}</p>
                {/if}
            </div>
        </div>
    </div>

    <div class="media">
        {#if story.media.type == "image"}
            <img src={mediaSrc} alt="Story content">
        {:else if story.media.type == "video"}
            <!-- svelte-ignore a11y-media-has-caption -->
            <video src={mediaSrc} controls autoplay></video>
        {/if}
    </div>
</div>