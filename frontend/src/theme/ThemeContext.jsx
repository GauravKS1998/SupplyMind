import { useMemo, useState } from "react";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { ColorModeContext } from "./ColorModeContext";
import { getTheme } from "./theme";

const ThemeContextProvider = ({ children }) => {
  const [mode, setMode] = useState(localStorage.getItem("themeMode") || "dark");

  const toggleTheme = () => {
    const newMode = mode === "dark" ? "light" : "dark";

    setMode(newMode);
    localStorage.setItem("themeMode", newMode);
  };

  const theme = useMemo(() => getTheme(mode), [mode]);

  return (
    <ColorModeContext.Provider value={{ mode, toggleTheme }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default ThemeContextProvider;
