export type Story = {
    id: string;
    timestamp: number;
    sender: {
        name: string;
        // number: string; The user's phone number, omitted by the server 
    }
    media: {
        type: "image" | "video";
        filename: string;
    };
    caption: string;
    viewed: boolean;
}