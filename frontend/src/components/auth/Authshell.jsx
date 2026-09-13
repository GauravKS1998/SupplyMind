import { useEffect } from "react";
import { Box, Paper, Typography, GlobalStyles } from "@mui/material";

import PublicNavbar from "./PublicNavbar";
import {
  useAuthTokens,
  ensureAuthFontsLoaded,
  authScrollbarSx,
} from "./authStyles";

// -------------------------------------------------------------
// Shared two-column shell for the auth pages: serif headline +
// card on the left, full-bleed image on the right. Login and
// Signup both render into this so they can never drift apart.
// -------------------------------------------------------------

const AuthShell = ({
  headline,
  subtext,
  imageSrc,
  imageAlt = "SupplyMind",
  imageTitle,
  imageSubtitle,
  children,
  footer,
  cardMaxWidth = 460,
}) => {
  useEffect(() => {
    ensureAuthFontsLoaded();
  }, []);

  const authTokens = useAuthTokens();

  // Dynamic gradient target based on mode (dark vs light background)
  const isLight = authTokens.mode === "light";
  const overlayGradient = isLight
    ? "linear-gradient(180deg, rgba(247,244,236,0) 35%, rgba(247,244,236,0.92) 100%)"
    : "linear-gradient(180deg, rgba(11,10,9,0) 35%, rgba(11,10,9,0.92) 100%)";

  return (
    <>
      {/* Target the page level scrollbars */}
      <GlobalStyles
        styles={{
          "html, body": {
            backgroundColor: authTokens.pageBg,
            ...authScrollbarSx(authTokens),
          },
        }}
      />
      <Box
        sx={{
          minHeight: "100vh",
          width: "100%",
          backgroundColor: authTokens.pageBg,
          color: authTokens.textPrimary,
          position: "relative",
          fontFamily: authTokens.fontBody,
          transition: "background-color 0.2s ease, color 0.2s ease",
        }}
      >
        <PublicNavbar />

        <Box
          sx={{
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            alignItems: "stretch",
            minHeight: "100vh",
            maxWidth: "1360px",
            mx: "auto",
            px: { xs: 3, sm: 5, md: 7 },
            pt: { xs: 11, md: 13 },
            pb: { xs: 6, md: 8 },
            gap: { xs: 6, md: 8 },
          }}
        >
          {/* LEFT — headline + card */}
          <Box
            sx={{
              flex: { xs: "none", md: `0 1 ${cardMaxWidth}px` },
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              width: "100%",
            }}
          >
            <Typography
              sx={{
                fontFamily: authTokens.fontDisplay,
                fontWeight: 500,
                fontSize: { xs: "2.3rem", sm: "2.6rem", md: "2.85rem" },
                lineHeight: 1.08,
                letterSpacing: "-0.01em",
                mb: 1.5,
                color: authTokens.textPrimary,
              }}
            >
              {headline}
            </Typography>

            {subtext && (
              <Typography
                sx={{
                  fontSize: "1rem",
                  lineHeight: 1.5,
                  color: authTokens.textSecondary,
                  mb: 4,
                  maxWidth: 420,
                }}
              >
                {subtext}
              </Typography>
            )}

            <Paper
              elevation={0}
              sx={{
                backgroundColor: authTokens.fieldFill,
                border: `1px solid ${authTokens.cardBorder}`,
                borderRadius: "18px",
                p: { xs: 3, sm: 4 },
                width: "100%",
                maxWidth: cardMaxWidth,
              }}
            >
              {children}
            </Paper>

            {footer && (
              <Box sx={{ mt: 3, maxWidth: cardMaxWidth, textAlign: "center" }}>
                {footer}
              </Box>
            )}
          </Box>

          {/* RIGHT — image panel */}
          <Box
            sx={{
              display: { xs: "none", md: "block" },
              flex: 1,
              position: "relative",
              borderRadius: "22px",
              overflow: "hidden",
              minHeight: 560,
            }}
          >
            <Box
              component="img"
              src={imageSrc}
              alt={imageAlt}
              sx={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                display: "block",
              }}
            />

            {(imageTitle || imageSubtitle) && (
              <Box
                sx={{
                  position: "absolute",
                  inset: 0,
                  background: overlayGradient,
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "flex-end",
                  p: 5,
                  transition: "background 0.2s ease",
                }}
              >
                {imageTitle && (
                  <Typography
                    sx={{
                      fontFamily: authTokens.fontDisplay,
                      fontWeight: 500,
                      fontSize: "1.65rem",
                      mb: 0.75,
                      color: authTokens.textPrimary,
                    }}
                  >
                    {imageTitle}
                  </Typography>
                )}

                {imageSubtitle && (
                  <Typography
                    sx={{
                      fontSize: "0.95rem",
                      lineHeight: 1.6,
                      color: authTokens.textSecondary,
                      maxWidth: 360,
                    }}
                  >
                    {imageSubtitle}
                  </Typography>
                )}
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </>
  );
};

export default AuthShell;
