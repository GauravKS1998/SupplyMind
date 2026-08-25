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

const ProfileSummaryCard = ({ profile, currentUser }) => {
  const user = profile || currentUser;

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
      sx={{ border: 1, borderColor: "divider", borderRadius: 2 }}
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
              bgcolor: "primary.main",
              color: "primary.contrastText",
            }}
          >
            {getInitials(user?.full_name)}
          </Avatar>

          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              textAlign: "center",
            }}
          >
            {user?.full_name || "User"}
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              textAlign: "center",
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
            sx={{ fontWeight: 600, fontSize: "0.75rem" }}
          />
        </Stack>

        <Divider sx={{ my: 3 }} />

        <Stack spacing={2}>
          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block" }}
            >
              Account ID
            </Typography>
            <Typography variant="body2" sx={{ fontWeight: 500 }}>
              #{user?.id ?? "-"}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
            >
              Email
            </Typography>
            <Typography
              variant="body2"
              sx={{ wordBreak: "break-all", fontWeight: 500 }}
            >
              {user?.email || "-"}
            </Typography>
          </Box>

          <Box>
            <Typography
              variant="caption"
              color="text.secondary"
              display="block"
            >
              Account Status
            </Typography>
            <Typography
              variant="body2"
              sx={{ fontWeight: 500 }}
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
