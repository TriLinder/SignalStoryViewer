<script lang="ts">
    import { onMount } from "svelte";

    export let timestamp: Date | number;

    let timeString: string;

    function update() {
        const dateObject = new Date(timestamp);
        const secondsSinceDate = (new Date().getTime() - dateObject.getTime()) / 1000;

        const hours = Math.floor(secondsSinceDate / 3600);
        const minutes = Math.floor(secondsSinceDate / 60) % 60;
        const seconds = Math.floor(secondsSinceDate) % 60;

        timeString = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

        setTimeout(update, 750);
    }

    onMount(update);
</script>

{timeString}