import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";

import AppRoutes from "./routes/AppRoutes";
import { store } from "./store/store";
import ThemeContextProvider from "./theme/ThemeContext";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <ThemeContextProvider>
        <AppRoutes />
      </ThemeContextProvider>
    </Provider>
  </StrictMode>,
);
