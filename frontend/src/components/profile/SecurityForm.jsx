import { useState } from "react";

import {
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
  IconButton,
  InputAdornment,
} from "@mui/material";

import { Visibility, VisibilityOff } from "@mui/icons-material";

import SecurityIcon from "@mui/icons-material/Security";
import LockIcon from "@mui/icons-material/Lock";
import KeyIcon from "@mui/icons-material/Key";

import { useAuthTokens, authFieldSx } from "../../components/auth/authStyles";

const SecurityForm = ({
  passwordForm,
  handlePasswordChange,
  saving,
  onSubmit,
}) => {
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const brand = useAuthTokens();

  return (
    <Card
      elevation={0}
      sx={{
        border: 1,
        borderColor: "divider",
        borderRadius: 5,
        mb: 3,
        backgroundColor: brand.pageBg,
        transition: "background-color 0.2s ease, color 0.2s ease",
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={1} sx={{ mb: 3, alignItems: "center" }}>
          <SecurityIcon
            sx={{
              color: brand.accent,
            }}
          />
          <Typography
            variant="h6"
            sx={{ fontWeight: 700, fontFamily: brand.fontDisplay }}
          >
            Security
          </Typography>
        </Stack>

        <Box component="form" onSubmit={onSubmit}>
          <Stack spacing={2.5}>
            <TextField
              fullWidth
              variant="outlined"
              size="small"
              type={showCurrentPassword ? "text" : "password"}
              label="Current Password"
              name="current_password"
              value={passwordForm.current_password}
              onChange={handlePasswordChange}
              disabled={saving}
              sx={{
                ...authFieldSx(brand),
                mb: 1.75,
              }}
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <KeyIcon sx={{ color: "text.secondary", fontSize: 20 }} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        size="small"
                        onClick={() =>
                          setShowCurrentPassword((previous) => !previous)
                        }
                        edge="end"
                        disabled={saving}
                      >
                        {showCurrentPassword ? (
                          <VisibilityOff
                            sx={{ color: "text.secondary", fontSize: 20 }}
                          />
                        ) : (
                          <Visibility
                            sx={{ color: "text.secondary", fontSize: 20 }}
                          />
                        )}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
            />

            <TextField
              fullWidth
              variant="outlined"
              size="small"
              type={showPassword ? "text" : "password"}
              label="New Password"
              name="new_password"
              value={passwordForm.new_password}
              onChange={handlePasswordChange}
              disabled={saving}
              helperText="Password must contain at least 8 characters."
              sx={{
                ...authFieldSx(brand),
                mb: 1.75,
                "& .MuiInput-input": { padding: "8px 4px" },
              }}
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <KeyIcon sx={{ color: "text.secondary", fontSize: 20 }} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        onClick={() => setShowPassword((previous) => !previous)}
                        edge="end"
                        disabled={saving}
                        size="small"
                      >
                        {showPassword ? (
                          <VisibilityOff
                            sx={{ fontSize: 20, color: "text.secondary" }}
                          />
                        ) : (
                          <Visibility
                            sx={{ fontSize: 20, color: "text.secondary" }}
                          />
                        )}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
            />

            <TextField
              fullWidth
              variant="outlined"
              size="small"
              type={showConfirmPassword ? "text" : "password"}
              label="Confirm New Password"
              name="confirm_password"
              value={passwordForm.confirm_password}
              onChange={handlePasswordChange}
              disabled={saving}
              sx={{
                ...authFieldSx(brand),
                mb: 1.75,
              }}
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <KeyIcon sx={{ color: "text.secondary", fontSize: 20 }} />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        size="small"
                        onClick={() =>
                          setShowConfirmPassword((previous) => !previous)
                        }
                        edge="end"
                        disabled={saving}
                      >
                        {showConfirmPassword ? (
                          <VisibilityOff
                            sx={{ color: "text.secondary", fontSize: 20 }}
                          />
                        ) : (
                          <Visibility
                            sx={{ color: "text.secondary", fontSize: 20 }}
                          />
                        )}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
            />

            <Box sx={{ display: "flex", justifyContent: "flex-end", pt: 1 }}>
              <Button
                type="submit"
                variant="contained"
                disableElevation
                startIcon={<LockIcon />}
                disabled={saving}
                sx={{
                  borderRadius: "10px",
                  px: 3,
                  py: 1,
                  fontWeight: 600,
                  textTransform: "none",
                  fontSize: "0.9rem",
                  color: brand.ctaText,
                  backgroundColor: brand.ctaBg,
                  border: brand.accent,
                  "&:hover": {
                    backgroundColor: brand.ctaBgHover,
                  },
                }}
              >
                {saving ? "Changing..." : "Change Password"}
              </Button>
            </Box>
          </Stack>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SecurityForm;
