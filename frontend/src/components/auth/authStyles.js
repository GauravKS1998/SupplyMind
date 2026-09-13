// -------------------------------------------------------------
// Shared design tokens for the auth experience (Login / Signup).
// Keeping these in one place means the two pages can never
// visually drift apart.
//
// Day/night support: only "normal" surface + text colors switch
// between modes (page/card backgrounds, field fills, borders,
// dividers, body/label text). Accent, links, and button colors
// are intentionally identical in both modes — untouched by the
// theme toggle, per request.
// -------------------------------------------------------------

import { useContext } from "react";
import { ColorModeContext } from "../../theme/ColorModeContext";

// Shared design constants
const constantTokens = {
  accent: "#C08552",
  accentSoft: "rgba(192, 133, 82, 0.16)",
  errorBg: "rgba(214, 90, 70, 0.12)",
  errorText: "#E8A08F",
  errorBorder: "rgba(214, 90, 70, 0.28)",
  fontDisplay: "'Fraunces', 'Georgia', serif",
  fontBody: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
};

// Dark Mode Surface Tokens
const darkSurface = {
  mode: "dark",
  pageBg: "#0B0A09",
  ctaBg: "#F5F1E9",
  ctaBgHover: "#E7E0D2",
  ctaText: "#141311", // Dark text on cream button
  disabledBg: "rgba(255, 255, 255, 0.08)",
  disabledText: "rgba(255, 255, 255, 0.30)",
  checkboxUnchecked: "rgba(255, 255, 255, 0.38)",
  cardBorder: "rgba(255, 255, 255, 0.10)",
  fieldFill: "rgba(255, 255, 255, 0.05)",
  fieldFillHover: "rgba(255, 255, 255, 0.08)",
  fieldBorder: "rgba(255, 255, 255, 0.12)",
  fieldBorderHover: "rgba(255, 255, 255, 0.20)",
  divider: "rgba(255, 255, 255, 0.12)",
  textPrimary: "#F5F1E9",
  textSecondary: "rgba(245, 241, 233, 0.60)",
  textMuted: "rgba(245, 241, 233, 0.42)",
  scrollbarThumb: "rgba(255, 255, 255, 0.16)",
  scrollbarThumbHover: "rgba(255, 255, 255, 0.28)",
  menuPaperBg: "#161513",
};

// Light Mode Surface Tokens
const lightSurface = {
  mode: "light",
  pageBg: "#F7F4EC",
  ctaBg: "#C08552", // Matches accent brand color
  ctaBgHover: "#A66E3F",
  ctaText: "#FFFFFF", // White text on warm brown CTA for optimal contrast
  disabledBg: "rgba(23, 21, 18, 0.08)",
  disabledText: "rgba(23, 21, 18, 0.35)",
  checkboxUnchecked: "rgba(23, 21, 18, 0.38)",
  cardBorder: "rgba(23, 21, 18, 0.10)",
  fieldFill: "rgba(23, 21, 18, 0.035)",
  fieldFillHover: "rgba(23, 21, 18, 0.06)",
  fieldBorder: "rgba(23, 21, 18, 0.12)",
  fieldBorderHover: "rgba(23, 21, 18, 0.20)",
  divider: "rgba(23, 21, 18, 0.12)",
  textPrimary: "#171512",
  textSecondary: "rgba(23, 21, 18, 0.62)",
  textMuted: "rgba(23, 21, 18, 0.42)",
  scrollbarThumb: "rgba(23, 21, 18, 0.16)",
  scrollbarThumbHover: "rgba(23, 21, 18, 0.28)",
  menuPaperBg: "#FFFFFF",
};

export const getAuthTokens = (mode) => ({
  ...constantTokens,
  ...(mode === "light" ? lightSurface : darkSurface),
});

// Reads the app's current day/night mode (same ColorModeContext the
// rest of the app uses) and returns the matching token set.
export const useAuthTokens = () => {
  const context = useContext(ColorModeContext);
  const mode = context?.mode === "light" ? "light" : "dark";
  return getAuthTokens(mode);
};

// Static dark-mode export, kept only for backward compatibility with
// any file that still imports `authTokens` directly. Prefer
// `useAuthTokens()` inside components so the page reacts to the
// theme toggle.
export const authTokens = getAuthTokens("dark");

// Injects the two Google Fonts used by the auth pages exactly once,
// so the pages work as drop-in files without editing index.html.
export const ensureAuthFontsLoaded = () => {
  if (typeof document === "undefined") return;
  if (document.getElementById("auth-fonts-link")) return;

  const link = document.createElement("link");
  link.id = "auth-fonts-link";
  link.rel = "stylesheet";
  link.href =
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap";
  document.head.appendChild(link);
};

// Shared sx for outlined text fields sitting on the auth card.
// Takes the current token set so it follows the theme toggle.
export const authFieldSx = (tokens) => ({
  "& .MuiOutlinedInput-root": {
    backgroundColor: tokens.fieldFill,
    borderRadius: "10px",
    color: tokens.textPrimary,
    fontFamily: tokens.fontBody,
    transition: "background-color 0.15s ease",

    "&:hover": {
      backgroundColor: tokens.fieldFillHover,
    },

    "& fieldset": {
      borderColor: tokens.fieldBorder,
    },
    "&:hover fieldset": {
      borderColor: tokens.fieldBorderHover,
    },
    "&.Mui-focused fieldset": {
      borderColor: tokens.accent,
      borderWidth: "1px",
    },
  },

  "& .MuiInputLabel-root": {
    color: tokens.textSecondary,
    fontFamily: tokens.fontBody,
  },
  "& .MuiInputLabel-root.Mui-focused": {
    color: tokens.accent,
  },

  "& .MuiInputBase-input::placeholder": {
    color: tokens.textMuted,
    opacity: 1,
  },
});

// Shared sx for the outlined Select (country code).
export const authSelectSx = (tokens) => ({
  backgroundColor: tokens.fieldFill,
  borderRadius: "10px",
  color: tokens.textPrimary,
  fontFamily: tokens.fontBody,

  // Label styles
  "& .MuiInputLabel-root": {
    color: tokens.textSecondary, // Default label color
    fontFamily: tokens.fontBody,
  },
  "& .MuiInputLabel-root.Mui-focused": {
    color: tokens.accent, // Label color when field is active/focused
  },
  "&:hover .MuiInputLabel-root": {
    color: tokens.textPrimary, // Optional: Label color when hovering the select
  },

  // Border & outline styles
  "& .MuiOutlinedInput-notchedOutline": {
    borderColor: tokens.fieldBorder,
  },
  "&:hover .MuiOutlinedInput-notchedOutline": {
    borderColor: tokens.fieldBorderHover,
  },
  "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
    borderColor: tokens.accent,
  },

  // Icon styles
  "& .MuiSvgIcon-root": {
    color: tokens.textSecondary,
  },
  "&.Mui-focused .MuiSvgIcon-root": {
    color: tokens.accent,
  },

  // Select inner input
  "& .MuiSelect-select": {
    display: "flex",
    alignItems: "center",
    py: "8.5px", // Matches standard small TextField input height
  },
});

export const authScrollbarSx = (tokens) => ({
  scrollbarWidth: "thin",
  scrollbarColor: `${tokens.scrollbarThumb} transparent`,
  "&::-webkit-scrollbar": { width: "6px" },
  "&::-webkit-scrollbar-track": { background: "transparent" },
  "&::-webkit-scrollbar-thumb": {
    backgroundColor: tokens.scrollbarThumb,
    borderRadius: "10px",
  },
  "&::-webkit-scrollbar-thumb:hover": {
    backgroundColor: tokens.scrollbarThumbHover,
  },
});

// Shared sx for the dropdown menu paper (Select menu).
export const authMenuPaperSx = (tokens) => ({
  backgroundColor: tokens.pageBg,
  border: `1px solid ${tokens.cardBorder}`,
  backgroundImage: "none",
  borderRadius: "10px",
  fontFamily: tokens.fontBody,
  
  // Style the individual dropdown items
  "& .MuiMenuItem-root": {
    fontFamily: tokens.fontBody,
    fontSize: "0.875rem",
    color: tokens.textPrimary,
    borderRadius: "6px",
    mx: 0.5,
    my: 0.25,
    transition: "background-color 0.15s ease",

    "&:hover": {
      backgroundColor: tokens.fieldFillHover,
    },
    "&.Mui-selected": {
      backgroundColor: tokens.fieldFillHover,
      color: tokens.accent,
      fontWeight: 600,
      "&:hover": {
        backgroundColor: tokens.fieldFillHover,
      },
    },
  },
});