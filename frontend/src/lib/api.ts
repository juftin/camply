import axios from "axios";
import {
  SearchResult,
  RecreationArea,
  Provider,
  Campground,
} from "@/lib/structs.ts";

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

export async function getRecreationArea(
  provider: number,
  id: string,
): Promise<RecreationArea> {
  const response = await api.get<RecreationArea>(`/rec-area/${provider}/${id}`);
  return response.data;
}

export async function getProvider(id: number): Promise<Provider> {
  const response = await api.get<Provider>(`/provider/${id}`);
  return response.data;
}

export async function getCampgrounds(
  provider: number,
  recreationAreaId: string,
): Promise<Campground[]> {
  const response = await api.get<Campground[]>(
    `/rec-area/${provider}/${recreationAreaId}/campgrounds`,
  );
  return response.data;
}

export async function getCampground(
  provider: number,
  campgroundId: string,
): Promise<Campground> {
  const response = await api.get<Campground>(
    `/campground/${provider}/${campgroundId}`,
  );
  return response.data;
}
