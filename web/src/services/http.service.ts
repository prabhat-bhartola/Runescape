import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

class HttpService {
  private static client: AxiosInstance;
  private static instance: HttpService;

  private initClient() {
    return axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_V1_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  public static getInstance(): HttpService {
    if (!HttpService.instance) {
      HttpService.instance = new HttpService();
    }
    return HttpService.instance;
  }

  public static getClient(): AxiosInstance {
    if (!HttpService.client) {
      HttpService.client = HttpService.getInstance().initClient();
    }
    return HttpService.client;
  }

  public static async get<T>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<T> {
    try {
      const res = await HttpService.getClient().get<T>(url, config);
      return res.data;
    } catch (error) {
      console.log(error);
      throw error;
    }
  }

  public static async fetcher(url: string) {
    const res = await HttpService.getClient().get(url);
    return res.data;
  }

  public static getFetcher<T>() {
    const fetcher = async (url: string) => {
      return await HttpService.getClient()
        .get(url)
        .then((res) => res.data);
    };

    return fetcher;
  }
}

export default HttpService;
