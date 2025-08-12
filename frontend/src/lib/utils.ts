import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import DOMPurify from "dompurify";

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

export function sanitizeAndRenderHTML(html: string | null | undefined): {
  __html: string;
} {
  if (!html) return { __html: "" };

  // Check if the content contains HTML tags
  const hasHTML = /<[a-z][\s\S]*>/i.test(html);

  if (hasHTML) {
    // Sanitize HTML content
    const clean = DOMPurify.sanitize(html, {
      ALLOWED_TAGS: [
        "p",
        "br",
        "strong",
        "em",
        "u",
        "a",
        "ul",
        "ol",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
      ],
      ALLOWED_ATTR: ["href", "target", "rel"],
    });
    return { __html: clean };
  } else {
    // Plain text - convert to title case and return
    return { __html: toTitleCase(html) };
  }
}

export function isHTMLContent(content: string | null | undefined): boolean {
  if (!content) return false;
  return /<[a-z][\s\S]*>/i.test(content);
}
