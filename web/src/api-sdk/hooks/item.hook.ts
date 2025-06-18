import HttpService from "@/services/http.service";
import ItemService from "../services/item.service";
import useSWR from "swr";

export function useItemList() {
  const key = `${ItemService.basePath}`;

  const { data, error, isLoading, mutate } = useSWR(
    key,
    HttpService.getFetcher()
  );

  return {
    items: data,
    isLoading,
    isError: error,
    mutate,
  };
}
