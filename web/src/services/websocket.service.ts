import { Price, PriceWS } from "@/api-sdk/models/price";

class WSService {
  private static instance: WSService | null = null;
  private socket: WebSocket | null = null;

  private constructor() {}

  public static getInstance(): WSService {
    if (!WSService.instance) {
      WSService.instance = new WSService();
      WSService.instance.initialize();
    }

    return WSService.instance;
  }

  private initialize() {
    this.socket = new WebSocket(`${process.env.NEXT_PUBLIC_WS_V1_BASE_URL}ws`);

    this.socket.onmessage = this.onMessage;
    this.socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
    this.socket.onclose = () => {
      console.log("WebSocket connection closed");
    };
  }

  private messageListeners: Array<(msg: PriceWS[]) => void> = [];

  public onMessage(event: MessageEvent) {
    const msg: Array<PriceWS> = JSON.parse(event.data);
    this.messageListeners.forEach((listener) => listener(msg));
  }

  public addMessageListener(listener: (msg: PriceWS[]) => void) {
    this.messageListeners.push(listener);
  }

  public removeMessageListener(listener: (msg: PriceWS[]) => void) {
    this.messageListeners = this.messageListeners.filter((l) => l !== listener);
  }

  public close() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}

export default WSService;
