import { SearchResult } from "@/lib/api";
import { Mountain, Tent, Loader2 } from "lucide-react";
import { toTitleCase } from "@/lib/utils";
import { useEffect, useRef } from "react";

interface SearchDropdownProps {
  results: SearchResult[];
  isLoading: boolean;
  error: Error | null;
  query: string;
  isOpen: boolean;
  onSelect: (result: SearchResult) => void;
  isFetching?: boolean;
  selectedIndex?: number;
}

export function SearchDropdown({
  results,
  isLoading,
  error,
  query,
  isOpen,
  onSelect,
  isFetching,
  selectedIndex = -1,
}: SearchDropdownProps) {
  const itemRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Scroll selected item into view
  useEffect(() => {
    if (selectedIndex >= 0 && selectedIndex < itemRefs.current.length) {
      const selectedElement = itemRefs.current[selectedIndex];
      if (selectedElement) {
        selectedElement.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
        });
      }
    }
  }, [selectedIndex]);

  // Always render the dropdown container to prevent layout shifts
  return (
    <div
      className={`absolute top-full left-0 right-0 mt-1 bg-background border border-border rounded-md shadow-lg z-50 max-h-80 overflow-y-auto transition-all duration-200 ${
        isOpen && query.trim().length >= 2
          ? "opacity-100 visible transform scale-100"
          : "opacity-0 invisible transform scale-95 pointer-events-none"
      }`}
    >
      {query.trim().length >= 2 && (
        <>
          {/* Only show loading spinner if we have no data and are loading */}
          {isLoading && results.length === 0 ? (
            <div className="flex items-center justify-center p-4">
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
              <span className="text-sm text-muted-foreground">
                Searching campgrounds...
              </span>
            </div>
          ) : error ? (
            <div className="p-4">
              <p className="text-sm text-red-600 text-center">
                Failed to search campgrounds. Please try again.
              </p>
            </div>
          ) : results.length === 0 && !isLoading ? (
            <div className="p-4">
              <p className="text-sm text-muted-foreground text-center">
                No campgrounds found for "{query}". Try a different search term.
              </p>
            </div>
          ) : (
            <div className="py-1 relative">
              {/* Subtle loading indicator when fetching new data */}
              {isFetching && results.length > 0 && (
                <div className="absolute top-1 right-2 z-10">
                  <Loader2 className="h-3 w-3 animate-spin text-muted-foreground" />
                </div>
              )}
              {results.map((result, index) => (
                <div
                  key={result.id}
                  ref={(el) => (itemRefs.current[index] = el)}
                  className={`px-4 py-3 cursor-pointer transition-colors border-b last:border-b-0 ${
                    index === selectedIndex
                      ? "bg-primary/15 ring-1 ring-primary/20"
                      : "hover:bg-muted"
                  } ${isFetching ? "opacity-75" : "opacity-100"}`}
                  onClick={() => onSelect(result)}
                >
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 mt-0.5">
                      {result.entity_type === "RecreationArea" ? (
                        <Mountain className="h-4 w-4 text-primary" />
                      ) : (
                        <Tent className="h-4 w-4 text-primary" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-foreground truncate">
                        {toTitleCase(
                          result.entity_type === "RecreationArea"
                            ? result.recreation_area_name || ""
                            : result.campground_name || "",
                        )}
                      </h4>
                      <p className="text-xs text-muted-foreground">
                        {toTitleCase(result.provider_name)}
                      </p>
                      {result.entity_type === "Campground" &&
                        result.recreation_area_name && (
                          <p className="text-xs text-muted-foreground">
                            in {toTitleCase(result.recreation_area_name)}
                          </p>
                        )}
                    </div>
                    <div className="flex-shrink-0">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary">
                        {result.entity_type === "RecreationArea"
                          ? "Area"
                          : "Camp"}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
