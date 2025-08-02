import * as React from "react";
import { ThemeProviderContext } from "@/hooks/use-theme";

type Theme = "dark" | "light" | "system";
type UserTheme = "dark" | "light";

type ThemeProviderProps = {
  children: React.ReactNode;
  storageKey?: string;
};

export function ThemeProvider({
  children,
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [userTheme, setUserTheme] = React.useState<UserTheme>(() => {
    const stored = localStorage.getItem(storageKey) as Theme;
    if (stored === "light" || stored === "dark") {
      return stored;
    }
    // Default to system preference if no user preference stored
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  });

  React.useEffect(() => {
    const root = window.document.documentElement;

    root.classList.remove("light", "dark");
    root.classList.add(userTheme);
  }, [userTheme]);

  const toggleTheme = () => {
    const newTheme = userTheme === "light" ? "dark" : "light";
    setUserTheme(newTheme);
    localStorage.setItem(storageKey, newTheme);
  };

  const handleSetTheme = (newTheme: UserTheme) => {
    setUserTheme(newTheme);
    localStorage.setItem(storageKey, newTheme);
  };

  const value = {
    theme: "system" as Theme,
    userTheme,
    setTheme: handleSetTheme,
    toggleTheme,
  };

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  );
}
