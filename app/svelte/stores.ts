import { writable } from 'svelte/store';
import type { Story } from "./types";

export const currentPageStore = writable<"overview" | "storyView">("overview");
export const storyViewPageStory = writable<Story | null>(null);