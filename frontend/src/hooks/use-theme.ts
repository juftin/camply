import * as React from "react";

type Theme = "dark" | "light" | "system";
type UserTheme = "dark" | "light";

type ThemeProviderState = {
  theme: Theme;
  userTheme: UserTheme;
  setTheme: (theme: UserTheme) => void;
  toggleTheme: () => void;
};

const initialState: ThemeProviderState = {
  theme: "system",
  userTheme: "light",
  setTheme: () => null,
  toggleTheme: () => null,
};

export const ThemeProviderContext =
  React.createContext<ThemeProviderState>(initialState);

export const useTheme = () => {
  const context = React.useContext(ThemeProviderContext);

  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider");

  return context;
};
