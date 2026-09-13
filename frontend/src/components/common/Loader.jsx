import { Box, Typography } from "@mui/material";

// -------------------------------------------------------------
// SupplyMindLoader — a small "hub and nodes" spinner that echoes
// the app's HubIcon branding: three nodes orbit a pulsing center,
// like shipments circling a distribution hub. Pure SVG + CSS
// keyframes, no animation library, so it's cheap to render inline
// in a button or full-page.
// -------------------------------------------------------------

const SupplyMindLoader = ({ size = 22, color = "currentColor" }) => {
  const nodeR = 2.6;
  const hubR = 3.4;

  return (
    <Box
      component="svg"
      viewBox="0 0 36 36"
      role="status"
      aria-label="Loading"
      sx={{
        width: size,
        height: size,
        display: "block",
        flexShrink: 0,
        overflow: "visible",

        "@keyframes supplymind-spin": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "@keyframes supplymind-pulse": {
          "0%, 100%": { opacity: 0.6, transform: "scale(0.88)" },
          "50%": { opacity: 1, transform: "scale(1.08)" },
        },
      }}
    >
      {/* faint orbit ring */}
      <circle
        cx="18"
        cy="18"
        r="15"
        fill="none"
        stroke={color}
        strokeOpacity="0.18"
        strokeWidth="1.5"
      />

      {/* central hub, gently pulsing */}
      <circle
        cx="18"
        cy="18"
        r={hubR}
        fill={color}
        style={{
          transformOrigin: "18px 18px",
          animation: "supplymind-pulse 1.3s ease-in-out infinite",
        }}
      />

      {/* three nodes orbiting the hub, 120° apart */}
      <g
        style={{
          transformOrigin: "18px 18px",
          animation: "supplymind-spin 1s linear infinite",
        }}
      >
        <circle cx="18" cy="3" r={nodeR} fill={color} />
        <circle cx="31" cy="25.5" r={nodeR} fill={color} />
        <circle cx="5" cy="25.5" r={nodeR} fill={color} />
      </g>
    </Box>
  );
};

// Full-area variant for page/section loading states — centers the
// spinner with an optional caption. Use this for route transitions,
// data fetches, or anywhere a whole panel is waiting on something.
export const PageLoader = ({
  label = "Loading",
  size = 34,
  color = "currentColor",
  minHeight = 240,
}) => (
  <Box
    sx={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 1.5,
      minHeight,
      width: "100%",
    }}
  >
    <SupplyMindLoader size={size} color={color} />
    {label && (
      <Typography variant="body2" sx={{ color: "text.secondary" }}>
        {label}
      </Typography>
    )}
  </Box>
);

export default SupplyMindLoader;
