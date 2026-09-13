import {
  Avatar,
  Box,
  Card,
  CardContent,
  Chip,
  Divider,
  Stack,
  Typography,
} from "@mui/material";
import { ROLE_LABELS } from "../../constants/userConstants";

import { useAuthTokens } from "../../components/auth/authStyles";

const ProfileSummaryCard = ({ profile, currentUser }) => {
  const user = profile || currentUser;

  const brand = useAuthTokens();

  const getInitials = (name) => {
    if (!name) return "?";
    return name
      .split(" ")
      .filter(Boolean)
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();
  };

  const roleLabel = ROLE_LABELS[user?.role] || user?.role || "User";

  return (
    <Card
      elevation={0}
      sx={{
        border: 1,
        borderColor: "divider",
        borderRadius: 5,
        backgroundColor: brand.pageBg,
        transition: "background-color 0.2s ease, color 0.2s ease",
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack
          spacing={1.5}
          sx={{
            alignItems: "center",
          }}
        >
          <Avatar
            sx={{
              width: 88,
              height: 88,
              fontSize: "2rem",
              fontWeight: 700,
              fontFamily: brand.fontDisplay,
              bgcolor: brand.accent,
              color: brand.ctaText,
            }}
          >
            {getInitials(user?.full_name)}
          </Avatar>

          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              textAlign: "center",
              fontFamily: brand.fontDisplay,
            }}
          >
            {user?.full_name || "User"}
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              textAlign: "center",
              fontFamily: brand.fontBody,
            }}
          >
            {user?.email || ""}
          </Typography>

          {/* Clean, subtle role badge instead of heavy full-width block */}
          <Chip
            label={roleLabel}
            size="small"
            color="primary"
            variant="outlined"
            sx={{
              mt: 1.5,
              borderRadius: 1.5,
              fontWeight: 600,
              fontSize: "0.75rem",
              fontFamily: brand.fontBody,
              borderColor: brand.accent,
              color: brand.accent,
            }}
          />
        </Stack>

        <Divider sx={{ my: 3 }} />

        <Stack spacing={2}>
          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", fontFamily: brand.fontBody }}
            >
              Account ID
            </Typography>
            <Typography
              variant="body2"
              sx={{ fontWeight: 500, fontFamily: brand.fontBody }}
            >
              #{user?.id ?? "-"}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
              sx={{ fontFamily: brand.fontBody }}
            >
              Email
            </Typography>
            <Typography
              variant="body2"
              sx={{
                wordBreak: "break-all",
                fontWeight: 500,
                fontFamily: brand.fontBody,
              }}
            >
              {user?.email || "-"}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
              sx={{ fontFamily: brand.fontBody }}
            >
              Account Status
            </Typography>
            <Typography
              variant="body2"
              sx={{ fontWeight: 500, fontFamily: brand.fontBody }}
              color={user?.is_active ? "success.main" : "error.main"}
            >
              {user?.is_active ? "Active" : "Inactive"}
            </Typography>
          </Box>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ProfileSummaryCard;
