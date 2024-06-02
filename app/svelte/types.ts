export type Story = {
    id: string;
    timestamp: number;
    sender: {
        name: string;
        number: string;
    }
    media: {
        type: "image" | "video";
        filename: string;
    };
    caption: string;
    viewed: boolean;
}