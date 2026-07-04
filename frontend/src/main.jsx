import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider } from "@mui/material";
import { Provider } from "react-redux";

import AppRoutes from "./routes/AppRoutes";
import { store } from "./store/store";
import theme from "./theme/theme";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <AppRoutes />
      </ThemeProvider>
    </Provider>
  </StrictMode>,
);
