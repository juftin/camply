import { useQuery } from "@tanstack/react-query";
import { searchCampgrounds, SearchResult } from "@/lib/api";

export function useSearch(query: string, enabled: boolean = true) {
  const trimmedQuery = query.trim();
  const shouldSearch = enabled && trimmedQuery.length >= 2;

  return useQuery<SearchResult[]>({
    queryKey: ["search", trimmedQuery],
    queryFn: () => searchCampgrounds(trimmedQuery),
    enabled: shouldSearch,
    staleTime: 5 * 60 * 1000, // Consider data fresh for 5 minutes
    gcTime: 10 * 60 * 1000, // Keep cache for 10 minutes
    refetchOnWindowFocus: false,
    retry: 1,
    // Keep previous data while loading new results to prevent flicker
    placeholderData: (previousData) => previousData,
  });
}
