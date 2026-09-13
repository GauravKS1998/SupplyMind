import {
  Box,
  Button,
  Card,
  CardContent,
  InputAdornment,
  MenuItem,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import SaveIcon from "@mui/icons-material/Save";
import SmartphoneIcon from "@mui/icons-material/Smartphone";

import {
  useAuthTokens,
  authScrollbarSx,
  authSelectSx,
  authFieldSx,
  authMenuPaperSx,
} from "../../components/auth/authStyles";

const PersonalInfoForm = ({
  profileForm,
  setProfileForm,
  profileEmail,
  countryList = [],
  saving,
  onSubmit,
}) => {
  const brand = useAuthTokens();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

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
          <PersonIcon
            sx={{
              color: brand.accent,
            }}
          />
          <Typography
            variant="h6"
            sx={{ fontWeight: 700, fontFamily: brand.fontDisplay }}
          >
            Personal Information
          </Typography>
        </Stack>

        <Box component="form" onSubmit={onSubmit}>
          <Stack spacing={2.5}>
            <TextField
              fullWidth
              variant="outlined"
              size="small"
              label="Full Name"
              name="full_name"
              value={profileForm.full_name}
              onChange={handleChange}
              disabled={saving}
              slotProps={{ input: { maxLength: 150 } }}
              sx={{
                ...authFieldSx(brand),
                mb: 1.75,
              }}
            />

            <TextField
              fullWidth
              variant="outlined"
              size="small"
              label="Email"
              value={profileEmail || ""}
              disabled
              helperText="Email cannot be changed from your profile."
              sx={{
                ...authFieldSx(brand),
                mb: 1.75,
              }}
            />

            <Box>
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{ display: "block", mb: 0.5 }}
              >
                Phone Number
              </Typography>

              <Box sx={{ display: "flex", gap: 1.5 }}>
                <Select
                  variant="outlined"
                  name="countryCode"
                  value={profileForm.countryCode}
                  onChange={handleChange}
                  disabled={saving}
                  sx={{ ...authSelectSx(brand), width: 100 }}
                  MenuProps={{
                    slotProps: {
                      paper: {
                        sx: {
                          maxHeight: 5 * 44,
                          ...authMenuPaperSx(brand),
                          ...authScrollbarSx(brand),
                        },
                      },
                    },
                  }}
                >
                  {countryList.map((c) => (
                    <MenuItem key={c.iso} value={c.code}>
                      {c.flag} {c.code}
                    </MenuItem>
                  ))}
                </Select>

                <TextField
                  fullWidth
                  variant="outlined"
                  size="small"
                  name="phone"
                  type="tel"
                  placeholder="Phone number"
                  value={profileForm.phone}
                  onChange={handleChange}
                  autoComplete="tel-national"
                  disabled={saving}
                  sx={authFieldSx(brand)}
                  slotProps={{
                    input: {
                      startAdornment: (
                        <InputAdornment position="start">
                          <SmartphoneIcon
                            sx={{ color: "text.secondary", fontSize: 20 }}
                          />
                        </InputAdornment>
                      ),
                    },
                  }}
                />
              </Box>
            </Box>

            <Box sx={{ display: "flex", justifyContent: "flex-end", pt: 1 }}>
              <Button
                type="submit"
                variant="contained"
                disableElevation
                startIcon={<SaveIcon />}
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
                {saving ? "Saving..." : "Save Changes"}
              </Button>
            </Box>
          </Stack>
        </Box>
      </CardContent>
    </Card>
  );
};

export default PersonalInfoForm;
