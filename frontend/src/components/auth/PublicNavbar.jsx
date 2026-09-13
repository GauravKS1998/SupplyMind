import { useContext } from "react";
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material";
import HubIcon from "@mui/icons-material/Hub";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import { Link } from "react-router-dom";

import { ColorModeContext } from "../../theme/ColorModeContext";
import { useAuthTokens } from "./authStyles";

// A lightweight relative of the app's main Navbar, used on the
// pre-login Login / Signup pages. There's no authenticated user yet,
// so it drops the account menu but keeps the same brand mark and
// the same day/night toggle used elsewhere in the app.
const PublicNavbar = () => {
  const { mode, toggleTheme } = useContext(ColorModeContext);
  const authTokens = useAuthTokens();

  return (
    <AppBar
      position="absolute"
      elevation={0}
      sx={{
        backgroundColor: "transparent",
        backgroundImage: "none",
        boxShadow: "none",
      }}
    >
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          px: { xs: 3, md: 6 },
          py: 1,
        }}
      >
        <Box
          component={Link}
          to="/"
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.1,
            textDecoration: "none",
          }}
        >
          <HubIcon sx={{ fontSize: 26, color: authTokens.accent }} />

          <Typography
            sx={{
              fontFamily: authTokens.fontDisplay,
              fontWeight: 600,
              fontSize: "1.25rem",
              letterSpacing: 0.2,
              color: authTokens.textPrimary,
            }}
          >
            SupplyMind
          </Typography>
        </Box>

        <IconButton
          onClick={toggleTheme}
          aria-label="Toggle theme"
          sx={{
            color: authTokens.textPrimary,
            border: `1px solid ${authTokens.cardBorder}`,
            borderRadius: 1.5,
          }}
        >
          {mode === "dark" ? (
            <LightModeIcon fontSize="small" />
          ) : (
            <DarkModeIcon fontSize="small" />
          )}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default PublicNavbar;
