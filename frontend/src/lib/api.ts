import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL;

export interface SearchResult {
  id: string;
  entity_type: string;
  provider_id: number;
  provider_name: string;
  recreation_area_id: string | null;
  recreation_area_name: string | null;
  campground_id: string | null;
  campground_name: string | null;
}

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
