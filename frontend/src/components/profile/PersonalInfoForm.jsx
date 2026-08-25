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
  useTheme,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import SaveIcon from "@mui/icons-material/Save";
import SmartphoneIcon from "@mui/icons-material/Smartphone";

const PersonalInfoForm = ({
  profileForm,
  setProfileForm,
  profileEmail,
  countryList = [],
  saving,
  onSubmit,
}) => {
  const theme = useTheme();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <Card
      elevation={0}
      sx={{ border: 1, borderColor: "divider", borderRadius: 2, mb: 3 }}
    >
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={1} sx={{ mb: 3, alignItems: "center" }}>
          <PersonIcon color="primary" />
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            Personal Information
          </Typography>
        </Stack>

        <Box component="form" onSubmit={onSubmit}>
          <Stack spacing={2.5}>
            <TextField
              fullWidth
              variant="standard"
              label="Full Name"
              name="full_name"
              value={profileForm.full_name}
              onChange={handleChange}
              disabled={saving}
              slotProps={{ input: { maxLength: 150 } }}
            />

            <TextField
              fullWidth
              variant="standard"
              label="Email"
              value={profileEmail || ""}
              disabled
              helperText="Email cannot be changed from your profile."
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
                  variant="standard"
                  name="countryCode"
                  value={profileForm.countryCode}
                  onChange={handleChange}
                  disabled={saving}
                  sx={{ width: 100 }}
                  MenuProps={{
                    slotProps: {
                      paper: {
                        sx: {
                          maxHeight: 5 * 44,
                          scrollbarWidth: "thin",
                          scrollbarColor: `${theme.palette.action.hover} transparent`,
                          "&::-webkit-scrollbar": { width: "6px" },
                          "&::-webkit-scrollbar-track": {
                            background: "transparent",
                          },
                          "&::-webkit-scrollbar-thumb": {
                            backgroundColor: theme.palette.action.hover,
                            borderRadius: "10px",
                          },
                          "&::-webkit-scrollbar-thumb:hover": {
                            backgroundColor: theme.palette.action.selected,
                          },
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
                  variant="standard"
                  name="phone"
                  type="tel"
                  placeholder="Phone number"
                  value={profileForm.phone}
                  onChange={handleChange}
                  autoComplete="tel-national"
                  disabled={saving}
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
                  borderRadius: 2,
                  px: 3,
                  fontWeight: 600,
                  textTransform: "none",
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
