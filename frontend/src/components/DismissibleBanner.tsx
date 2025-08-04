import * as React from "react";
import { X, LucideIcon } from "lucide-react";

interface DismissibleBannerProps {
  id: string;
  children: React.ReactNode;
  className?: string;
  closeButtonClassName?: string;
  showCondition?: boolean;
  icon?: LucideIcon;
  storageType?: "session" | "local";
  dismissible?: boolean;
}

export function DismissibleBanner({
  id,
  children,
  className = "",
  closeButtonClassName = "",
  showCondition = true,
  icon: Icon,
  storageType = "session",
  dismissible = true,
}: DismissibleBannerProps) {
  const [isVisible, setIsVisible] = React.useState(() => {
    if (!dismissible) return true;
    if (typeof window !== "undefined") {
      const storage = storageType === "local" ? localStorage : sessionStorage;
      return storage.getItem(`banner-dismissed-${id}`) !== "true";
    }
    return true;
  });

  const handleDismiss = () => {
    if (!dismissible) return;
    setIsVisible(false);
    const storage = storageType === "local" ? localStorage : sessionStorage;
    storage.setItem(`banner-dismissed-${id}`, "true");
  };

  if (!showCondition || !isVisible) {
    return null;
  }

  return (
    <div className={className}>
      <div className="container mx-auto relative">
        <div className="flex items-center justify-center gap-2">
          {Icon && <Icon className="h-5 w-5 flex-shrink-0" />}
          {children}
          {Icon && <Icon className="h-5 w-5 flex-shrink-0" />}
        </div>
        {dismissible && (
          <button
            onClick={handleDismiss}
            className={`absolute right-0 top-1/2 -translate-y-1/2 p-1 rounded ${closeButtonClassName}`}
            aria-label="Close banner"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
    </div>
  );
}
