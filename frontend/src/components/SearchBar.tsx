import React, { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";
import { SearchDropdown } from "@/components/SearchDropdown";
import { useSearch } from "@/hooks/useSearch";
import { SearchResult } from "@/lib/api";
import { toTitleCase } from "@/lib/utils";

interface SearchBarProps {
  placeholder?: string;
  className?: string;
}

export function SearchBar({
  placeholder = "Search campgrounds...",
  className = "max-w-2xl mx-auto",
}: SearchBarProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  // Debounce search query to avoid making too many API calls
  useEffect(() => {
    const trimmedQuery = searchQuery.trim();
    const timer = setTimeout(() => {
      setDebouncedQuery(trimmedQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  const {
    data: searchResults = [],
    isLoading,
    error,
    isFetching,
  } = useSearch(debouncedQuery);

  // Open dropdown when we have a query and close when empty
  useEffect(() => {
    const trimmedQuery = searchQuery.trim();
    const shouldOpen = trimmedQuery.length >= 2;
    setIsDropdownOpen(shouldOpen);
    // Only reset selected index when dropdown closes or opens from closed state
    if (!shouldOpen) {
      setSelectedIndex(-1);
    }
  }, [searchQuery]);

  // Reset selected index when results change due to new query
  useEffect(() => {
    setSelectedIndex(-1);
  }, [debouncedQuery]);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        searchRef.current &&
        !searchRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSearchResultSelect = (result: SearchResult) => {
    const displayName =
      result.entity_type === "RecreationArea"
        ? result.recreation_area_name
        : result.campground_name;

    setSearchQuery(toTitleCase(displayName || ""));
    setIsDropdownOpen(false);
    setSelectedIndex(-1);

    // Navigate to the appropriate page based on entity type
    if (result.entity_type === "RecreationArea" && result.recreation_area_id) {
      navigate(`/rec-areas/${result.provider_id}/${result.recreation_area_id}`);
    } else if (result.entity_type === "Campground" && result.campground_id) {
      navigate(`/campgrounds/${result.provider_id}/${result.campground_id}`);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isDropdownOpen || searchResults.length === 0) return;

    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        setSelectedIndex((prev) =>
          prev < searchResults.length - 1 ? prev + 1 : 0,
        );
        break;
      case "ArrowUp":
        event.preventDefault();
        setSelectedIndex((prev) =>
          prev > 0 ? prev - 1 : searchResults.length - 1,
        );
        break;
      case "Enter":
        event.preventDefault();
        if (selectedIndex >= 0 && selectedIndex < searchResults.length) {
          handleSearchResultSelect(searchResults[selectedIndex]);
        }
        break;
      case "Escape":
        event.preventDefault();
        setIsDropdownOpen(false);
        setSelectedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  return (
    <div className={className}>
      <div className="relative" ref={searchRef}>
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-muted-foreground h-5 w-5" />
            <Input
              ref={inputRef}
              placeholder={placeholder}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => {
                if (searchQuery.trim().length >= 2) {
                  setIsDropdownOpen(true);
                }
              }}
              className="pl-12 h-12 text-lg bg-gray-50 border-gray-300 dark:bg-background dark:border-border"
            />
          </div>
        </div>

        {/* Search Dropdown */}
        <SearchDropdown
          results={searchResults}
          isLoading={isLoading}
          error={error}
          query={debouncedQuery}
          isOpen={isDropdownOpen}
          onSelect={handleSearchResultSelect}
          isFetching={isFetching}
          selectedIndex={selectedIndex}
        />
      </div>
    </div>
  );
}
