export type Story = {
    id: string;
    timestamp: number;
    sender: {
        name: string;
        number: string;
    }
    media: string;
    caption: string;
    viewed: boolean;
}