import axios from "axios";
import { SearchResult } from "@/lib/structs.ts";

const apiUrl = import.meta.env.VITE_API_URL;

// Configure axios with base URL
const api = axios.create({
  baseURL: apiUrl || "/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export async function searchCampgrounds(
  query: string,
  limit: number = 20,
): Promise<SearchResult[]> {
  if (!query.trim()) {
    return [];
  }

  const response = await api.get<SearchResult[]>("/search", {
    params: {
      query: query.trim(),
      limit,
    },
  });

  return response.data;
}
