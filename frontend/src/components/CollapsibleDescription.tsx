import { useState, useEffect } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { sanitizeAndRenderHTML, isHTMLContent, toTitleCase } from "@/lib/utils";

interface CollapsibleDescriptionProps {
  description: string | null | undefined;
  fallback?: string;
  maxLines?: number;
}

function extractFirstParagraph(htmlContent: string): string {
  // Create a temporary div to parse the HTML
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = htmlContent;

  // Find the first paragraph or meaningful content
  const firstP = tempDiv.querySelector("p");
  if (firstP) {
    return firstP.outerHTML;
  }

  // If no <p> tag, take first meaningful text node or first element
  const firstElement = tempDiv.firstElementChild;
  if (firstElement) {
    return firstElement.outerHTML;
  }

  // Fallback: take first 150 characters
  const textContent = tempDiv.textContent || "";
  if (textContent.length > 150) {
    return `<p>${textContent.substring(0, 150)}...</p>`;
  }

  return htmlContent;
}

export function CollapsibleDescription({
  description,
  fallback = "No description available",
  maxLines = 3,
}: CollapsibleDescriptionProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [shouldCollapse, setShouldCollapse] = useState(false);
  const [previewContent, setPreviewContent] = useState<string>("");

  useEffect(() => {
    if (description) {
      const isHTML = isHTMLContent(description);
      let needsCollapse = false;

      if (isHTML) {
        // For HTML, extract first paragraph and check if there's more content
        const sanitized = sanitizeAndRenderHTML(description).__html;
        const preview = extractFirstParagraph(sanitized);
        setPreviewContent(preview);

        // Simple heuristic: if sanitized content is much longer than preview, collapse
        needsCollapse = sanitized.length > preview.length * 1.5;
      } else {
        // For plain text, check word count
        const words = description.split(" ");
        needsCollapse = words.length > 50; // More than ~50 words

        if (needsCollapse) {
          setPreviewContent(words.slice(0, 40).join(" ") + "...");
        }
      }

      setShouldCollapse(needsCollapse);
    }
  }, [description, maxLines]);

  if (!description) {
    return <span className="text-muted-foreground italic">{fallback}</span>;
  }

  const isHTML = isHTMLContent(description);

  return (
    <div className="space-y-3">
      <div className="transition-all duration-300">
        {shouldCollapse && !isExpanded ? (
          // Show preview content when collapsed
          isHTML ? (
            <div
              dangerouslySetInnerHTML={{ __html: previewContent }}
              className="prose prose-sm max-w-none dark:prose-invert [&>h1:first-child]:mt-4 [&>h2:first-child]:mt-4 [&>h3:first-child]:mt-4 [&>h4:first-child]:mt-4 [&>h5:first-child]:mt-4 [&>h6:first-child]:mt-4"
            />
          ) : (
            <span>{previewContent || toTitleCase(description)}</span>
          )
        ) : // Show full content when expanded or doesn't need collapsing
        isHTML ? (
          <div
            dangerouslySetInnerHTML={sanitizeAndRenderHTML(description)}
            className="prose prose-sm max-w-none dark:prose-invert [&>h1:first-child]:mt-4 [&>h2:first-child]:mt-4 [&>h3:first-child]:mt-4 [&>h4:first-child]:mt-4 [&>h5:first-child]:mt-4 [&>h6:first-child]:mt-4"
          />
        ) : (
          <span>{toTitleCase(description)}</span>
        )}
      </div>

      {shouldCollapse && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="inline-flex items-center space-x-2 px-3 py-2 text-sm font-medium text-primary bg-primary/10 hover:bg-primary/20 border border-primary/20 hover:border-primary/30 rounded-md transition-all duration-200 hover:shadow-sm"
        >
          {isExpanded ? (
            <>
              <span>Show less</span>
              <ChevronUp className="w-4 h-4" />
            </>
          ) : (
            <>
              <span>Show more</span>
              <ChevronDown className="w-4 h-4" />
            </>
          )}
        </button>
      )}
    </div>
  );
}
