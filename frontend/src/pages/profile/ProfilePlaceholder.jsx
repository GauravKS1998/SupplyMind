import { Box, Paper, Typography } from "@mui/material";

const ProfilePlaceholder = () => {
  return (
    <Box>
      <Paper
        sx={{
          p: 5,
          textAlign: "center",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: 700 }}>
          Profile
        </Typography>

        <Typography color="text.secondary" sx={{ mt: 1 }}>
          Profile management will be available soon.
        </Typography>
      </Paper>
    </Box>
  );
};

export default ProfilePlaceholder;
