import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { SnackbarProvider } from "notistack";

import AppRoutes from "./routes/AppRoutes";
import { store } from "./store/store";
import ThemeContextProvider from "./theme/ThemeContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <ThemeContextProvider>
        <SnackbarProvider
          maxSnack={3}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          autoHideDuration={4000}
        >
          <AppRoutes />
        </SnackbarProvider>
      </ThemeContextProvider>
    </Provider>
  </StrictMode>,
);
