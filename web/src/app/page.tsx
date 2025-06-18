"use client";

import Image from "next/image";
import React, { useEffect, useState } from "react";
import { useItemList } from "@/api-sdk/hooks/item.hook";
import Spinner from "@/components/spinner";
import { Item } from "@/api-sdk/models/item";
import WSService from "@/services/websocket.service";
import { PriceWS } from "@/api-sdk/models/price";

export default function PriceTable() {
  const { items: swrItems, isLoading, isError, mutate } = useItemList();

  // Local state that holds items with updated prices merged in
  const [items, setItems] = useState<Item[]>([]);

  // Sync local state when SWR items change (initial load or refetch)
  useEffect(() => {
    if (swrItems) {
      setItems(swrItems);
    }
  }, [swrItems]);

  useEffect(() => {
    const ws = WSService.getInstance();

    const handleNewPrices = (newPrices: PriceWS[]) => {
      setItems((prevItems) => {
        const itemsMap = new Map(prevItems.map((item) => [item.id, item]));

        // For each updated price, merge price info into matching item
        newPrices.forEach((priceUpdate) => {
          const item = itemsMap.get(priceUpdate.item_id);
          if (item) {
            // Create a new item object with updated price
            itemsMap.set(priceUpdate.item_id, {
              ...item,
              price: {
                ...item.price,
                ...priceUpdate,
              },
            });
          }
        });

        return Array.from(itemsMap.values());
      });
    };

    ws.addMessageListener(handleNewPrices);

    return () => {
      ws.removeMessageListener(handleNewPrices);
    };
  }, []);

  if (isLoading) {
    return <Spinner />;
  }

  if (!items || items.length === 0) {
    return (
      <p className="flex items-center justify-center h-screen">Such empty</p>
    );
  }

  return (
    <div className="overflow-x-auto p-4">
      <table className="min-w-full table-auto border-collapse border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            <th className="border border-gray-300 px-4 py-2 text-left"></th>
            <th className="border border-gray-300 px-4 py-2 text-left">ID</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Name</th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              Members
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              Limit
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              Value
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              High Alch
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              Low Alch
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              High Price
            </th>
            <th className="border border-gray-300 px-4 py-2 text-left">
              Low Price
            </th>
          </tr>
        </thead>
        <tbody>
          {items.map((item: Item) => (
            <tr key={item.id} className="hover:bg-gray-50">
              <td className="border border-gray-300 px-4 py-2">
                <img
                  src={`https://oldschool.runescape.wiki/images/${encodeURIComponent(
                    item.icon.replace(/ /g, "_")
                  )}`}
                  alt={`${item.name}'s avatar`}
                  className="w-10 h-10 rounded-full object-cover"
                />
              </td>
              <td className="border border-gray-300 px-4 py-2">{item.id}</td>
              <td className="border border-gray-300 px-4 py-2">{item.name}</td>
              <td className="border border-gray-300 px-4 py-2">
                {item.members ? "✅" : "❌"}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {item.limit || "-"}
              </td>
              <td className="border border-gray-300 px-4 py-2">{item.value}</td>
              <td className="border border-gray-300 px-4 py-2">
                {item.highalch ?? "-"}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {item.lowalch ?? "-"}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {item.price?.high ?? "-"}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {item.price?.low ?? "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
