import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function toTitleCase(str: string): string {
  return str
    .toLowerCase()
    .split(" ")
    .map((word) => {
      // Handle common abbreviations and prepositions
      const lowerWord = word.toLowerCase();
      const exceptions = [
        "of",
        "the",
        "and",
        "in",
        "on",
        "at",
        "to",
        "for",
        "with",
        "by",
      ];

      // Always capitalize first word and words that aren't exceptions
      if (word === str.split(" ")[0] || !exceptions.includes(lowerWord)) {
        return word.charAt(0).toUpperCase() + word.slice(1);
      }

      return lowerWord;
    })
    .join(" ");
}

export function toSlug(str: string): string {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "") // Remove special characters except spaces and hyphens
    .trim()
    .replace(/\s+/g, "-") // Replace spaces with hyphens
    .replace(/-+/g, "-"); // Replace multiple hyphens with single hyphen
}
