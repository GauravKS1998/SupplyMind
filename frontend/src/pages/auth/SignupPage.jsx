import { useState } from "react";

import { useTheme } from "@mui/material/styles";

import { Select, MenuItem } from "@mui/material";
import * as countryCodesList from "country-codes-list";

import {
  Alert,
  Box,
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import {
  ArrowBack,
  BusinessOutlined,
  EmailOutlined,
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";

import SmartphoneIcon from "@mui/icons-material/Smartphone";

import PersonIcon from "@mui/icons-material/Person";

import KeyIcon from "@mui/icons-material/Key";

import { Link as MuiLink } from "@mui/material";

import { Link, useNavigate } from "react-router-dom";

import { signup } from "../../api/services/authService";

import signupImage from "../../assets/login/supplymind-login.jpg";

import { GoogleIcon } from "./LoginPage";

const IMAGE_SRC = signupImage;
const VIDEO_SRC = "";

// Helper: convert "IN" -> 🇮🇳
const isoToFlag = (iso) =>
  iso
    .toUpperCase()
    .replace(/./g, (char) => String.fromCodePoint(127397 + char.charCodeAt(0)));

const rawList = countryCodesList.customList(
  "countryCode",
  "{countryNameEn}|+{countryCallingCode}",
);

const SignupPage = () => {
  const navigate = useNavigate();

  const theme = useTheme();

  const countryList = Object.entries(rawList)
    .map(([iso, entry]) => {
      const [label, code] = entry.split("|");
      return { iso, code, label, flag: isoToFlag(iso) };
    })
    .filter((c) => c.code !== "+") // drop countries with no calling code (e.g. Antarctica)
    .sort((a, b) => {
      if (a.iso === "IN") return -1;
      if (b.iso === "IN") return 1;
      return a.label.localeCompare(b.label);
    });

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
    countryCode: "+91",
    company_name: "",
    account_type: "",
    password: "",
    confirm_password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [termsAccepted, setTermsAccepted] = useState(false);

  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleAccountTypeChange = (type) => {
    setFormData((previous) => ({
      ...previous,
      account_type: type,
    }));
  };

  const validateForm = () => {
    if (!formData.full_name.trim()) {
      return "Full name is required.";
    }

    if (!formData.email.trim()) {
      return "Email is required.";
    }

    if (!formData.phone.trim()) {
      return "Phone number is required.";
    }

    if (!formData.company_name.trim()) {
      return "Company name is required.";
    }

    if (!formData.account_type) {
      return "Please select an account type.";
    }

    if (!formData.password) {
      return "Password is required.";
    }

    if (formData.password.length < 8) {
      return "Password must contain at least 8 characters.";
    }

    if (formData.password !== formData.confirm_password) {
      return "Passwords do not match.";
    }

    if (!termsAccepted) {
      return "Please accept the terms and conditions.";
    }

    return "";
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    const validationError = validateForm();

    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      setLoading(true);

      await signup({
        full_name: formData.full_name.trim(),
        email: formData.email.trim(),
        phone: `${formData.countryCode}${formData.phone.trim()}`,
        company_name: formData.company_name.trim(),
        account_type: formData.account_type,
        password: formData.password,
      });

      /*
       * V1 registration flow:
       *
       * Signup
       *   ↓
       * Account created
       *   ↓
       * Pending approval
       *   ↓
       * User logs in after approval
       *
       * We intentionally do NOT dispatch loginSuccess()
       * and do NOT create an authenticated session here.
       */

      navigate("/login", {
        replace: true,
        state: {
          signupSuccess: true,
          message: "Account created successfully. Pending approval.",
        },
      });
    } catch (err) {
      console.error("Signup failed", err);

      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Unable to create your account.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    setError("");

    /*
     * Google signup will eventually follow:
     *
     * Google authentication
     *        ↓
     * Receive Google identity
     *        ↓
     * Complete account information
     *        ↓
     * Select Supplier / Customer
     *        ↓
     * Pending approval
     *
     * The actual OAuth implementation will be connected
     * once the backend Google authentication endpoint
     * is established.
     */

    try {
      setGoogleLoading(true);

      // TODO:
      // Start Google OAuth flow.

      console.info("Google signup flow is not connected yet.");
    } finally {
      setGoogleLoading(false);
    }
  };

  const renderMediaPanel = () => {
    if (VIDEO_SRC) {
      return (
        <Box
          component="video"
          src={VIDEO_SRC}
          autoPlay
          muted
          loop
          playsInline
          sx={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      );
    }

    return (
      <Box
        component="img"
        src={IMAGE_SRC}
        alt="SupplyMind"
        sx={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
    );
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",

        "&::before": {
          content: '""',
          position: "absolute",
          inset: 0,
          backgroundImage: `url(${IMAGE_SRC})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(18px)",
          transform: "scale(1.08)",
          opacity: 0.75,
          zIndex: 0,
        },

        "&::after": {
          content: '""',
          position: "absolute",
          inset: 0,
          backgroundColor: "rgba(0, 0, 0, 0.22)",
          zIndex: 0,
        },
      }}
    >
      <Paper
        elevation={12}
        sx={{
          position: "relative",
          zIndex: 1,

          width: {
            xs: "92%",
            sm: "88%",
            md: "880px",
            lg: "940px",
          },

          height: {
            xs: "auto",
            sm: "720px",
            md: "760px",
          },

          maxHeight: "92vh",

          display: "flex",
          overflow: "hidden",

          borderRadius: {
            xs: 3,
            md: 4,
          },

          backgroundColor: "background.paper",
        }}
      >
        {/* =========================================================
            LEFT PANEL — SIGNUP FORM
        ========================================================= */}

        <Box
          sx={{
            width: { xs: "100%", md: "50%" },
            display: "flex",
            flexDirection: "column",
            p: { xs: 3, sm: 4, md: 5 },
            overflowY: "auto",

            scrollbarWidth: "thin",
            scrollbarColor: `${theme.palette.action.hover} transparent`,

            "&::-webkit-scrollbar": {
              width: "6px",
            },
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
          }}
        >
          {/* Back */}
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              mb: 2,
            }}
          >
            <IconButton
              component={Link}
              to="/"
              disabled={loading || googleLoading}
              size="small"
            >
              <ArrowBack fontSize="small" />
            </IconButton>

            <Typography
              component={Link}
              to="/"
              sx={{
                ml: 0.5,
                textDecoration: "none",
                color: "text.secondary",
                fontSize: "0.85rem",
                fontWeight: 500,
              }}
            >
              Back to SupplyMind
            </Typography>
          </Box>

          {/* Header */}
          <Box
            sx={{
              mb: 2.5,
            }}
          >
            <Typography
              variant="h4"
              fontWeight={700}
              sx={{
                mb: 0.5,
              }}
            >
              Create Account
            </Typography>

            <Typography variant="body2" color="text.secondary">
              Join SupplyMind and manage your supply chain smarter.
            </Typography>
          </Box>

          {/* Error */}
          {error && (
            <Alert
              severity="error"
              sx={{
                mb: 2,
              }}
            >
              {error}
            </Alert>
          )}

          {/* Form */}
          <Box component="form" onSubmit={handleSubmit} noValidate>
            {/* Full Name */}
            <TextField
              fullWidth
              variant="standard"
              size="small"
              label="Full Name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              autoComplete="name"
              disabled={loading || googleLoading}
              margin="dense"
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <PersonIcon
                        sx={{ color: "text.secondary", fontSize: 20 }}
                      />
                    </InputAdornment>
                  ),
                },
              }}
            />

            {/* Email */}
            <TextField
              fullWidth
              variant="standard"
              size="small"
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
              disabled={loading || googleLoading}
              margin="dense"
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <EmailOutlined
                        sx={{ color: "text.secondary", fontSize: 20 }}
                      />
                    </InputAdornment>
                  ),
                },
              }}
            />

            {/* Phone */}
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: "block", mt: 1, mb: 0.5 }}
            >
              Phone Number
            </Typography>

            <Box sx={{ display: "flex", gap: 1.5 }}>
              <Select
                variant="standard"
                name="countryCode"
                value={formData.countryCode}
                onChange={handleChange}
                disabled={loading || googleLoading}
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
                value={formData.phone}
                onChange={handleChange}
                autoComplete="tel-national"
                disabled={loading || googleLoading}
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

            {/* Company */}
            <TextField
              fullWidth
              variant="standard"
              size="small"
              label="Company Name"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              autoComplete="organization"
              disabled={loading || googleLoading}
              margin="dense"
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <BusinessOutlined
                        sx={{ color: "text.secondary", fontSize: 20 }}
                      />
                    </InputAdornment>
                  ),
                },
              }}
            />

            {/* Account Type */}
            <Typography
              variant="body2"
              fontWeight={600}
              sx={{
                mt: 2,
                mb: 1,
              }}
            >
              Account Type
            </Typography>

            <Box
              sx={{
                display: "flex",
                gap: 1,
              }}
            >
              <Button
                type="button"
                fullWidth
                variant={
                  formData.account_type === "SUPPLIER"
                    ? "contained"
                    : "outlined"
                }
                disabled={loading || googleLoading}
                onClick={() => handleAccountTypeChange("SUPPLIER")}
                sx={{
                  py: 1,
                  textTransform: "none",
                  fontWeight: 600,
                }}
              >
                Supplier
              </Button>

              <Button
                type="button"
                fullWidth
                variant={
                  formData.account_type === "CUSTOMER"
                    ? "contained"
                    : "outlined"
                }
                disabled={loading || googleLoading}
                onClick={() => handleAccountTypeChange("CUSTOMER")}
                sx={{
                  py: 1,
                  textTransform: "none",
                  fontWeight: 600,
                }}
              >
                Customer
              </Button>
            </Box>

            {/* Password */}
            <TextField
              fullWidth
              variant="standard"
              size="small"
              label="Password"
              name="password"
              type={showPassword ? "text" : "password"}
              value={formData.password}
              onChange={handleChange}
              autoComplete="new-password"
              disabled={loading || googleLoading}
              margin="dense"
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
                        onClick={() => setShowPassword((previous) => !previous)}
                        edge="end"
                      >
                        {showPassword ? (
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

            {/* Confirm Password */}
            <TextField
              fullWidth
              variant="standard"
              size="small"
              label="Confirm Password"
              name="confirm_password"
              type={showConfirmPassword ? "text" : "password"}
              value={formData.confirm_password}
              onChange={handleChange}
              autoComplete="new-password"
              disabled={loading || googleLoading}
              margin="dense"
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

            {/* Terms */}
            <FormControlLabel
              sx={{
                my: 1.5,
                alignItems: "flex-start",
              }}
              control={
                <Checkbox
                  size="small"
                  checked={termsAccepted}
                  onChange={(event) => setTermsAccepted(event.target.checked)}
                  disabled={loading || googleLoading}
                  sx={{
                    py: 0.5,
                    mt: "-5px",
                  }}
                />
              }
              label={
                <Typography variant="caption" color="text.secondary">
                  I agree to the SupplyMind{" "}
                  <MuiLink
                    component={Link}
                    to="/terms"
                    underline="hover"
                    onClick={(event) => event.stopPropagation()}
                    sx={{ fontWeight: 600 }}
                  >
                    Terms and Conditions
                  </MuiLink>
                  .
                </Typography>
              }
            />

            {/* Signup */}
            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              disabled={loading || googleLoading || !termsAccepted}
              sx={{
                mt: 1,
                py: 1.25,
                fontWeight: 600,
                textTransform: "none",
              }}
            >
              {loading ? (
                <CircularProgress size={23} color="inherit" />
              ) : (
                "Sign Up"
              )}
            </Button>

            {/* Divider */}
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1.5,
                my: 2,
              }}
            >
              <Box
                sx={{
                  flex: 1,
                  height: "1px",
                  bgcolor: "divider",
                }}
              />

              <Typography variant="caption" color="text.secondary">
                OR
              </Typography>

              <Box
                sx={{
                  flex: 1,
                  height: "1px",
                  bgcolor: "divider",
                }}
              />
            </Box>

            {/* Google */}
            <Button
              fullWidth
              variant="outlined"
              size="large"
              onClick={handleGoogleSignup}
              disabled={loading || googleLoading || !termsAccepted}
              sx={{
                height: 44,
                borderRadius: "6px",
                textTransform: "none",
                fontWeight: 500,
                color: "text.primary",
                borderColor: "divider",
                "&:hover": {
                  borderColor: "text.secondary",
                  backgroundColor: "action.hover",
                },
              }}
              startIcon={
                googleLoading ? <CircularProgress size={18} /> : <GoogleIcon />
              }
            >
              {googleLoading ? "Connecting..." : "Sign up with Google"}
            </Button>
          </Box>

          {/* Login */}
          <Box
            sx={{
              textAlign: "center",
              mt: 2,
            }}
          >
            <Typography variant="body2" color="text.secondary">
              Already have an account?{" "}
              <Box
                component={Link}
                to="/login"
                sx={{
                  textDecoration: "none",
                  fontWeight: 600,
                  color: "primary.main",
                }}
              >
                Log In
              </Box>
            </Typography>
          </Box>
        </Box>

        {/* =========================================================
            RIGHT PANEL — MEDIA
        ========================================================= */}

        <Box
          sx={{
            display: {
              xs: "none",
              md: "block",
            },

            width: "50%",
            position: "relative",
            overflow: "hidden",
          }}
        >
          {renderMediaPanel()}

          {/* Media overlay */}
          <Box
            sx={{
              position: "absolute",
              inset: 0,

              background:
                "linear-gradient(180deg, rgba(0,0,0,0.08) 0%, rgba(0,0,0,0.62) 100%)",

              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-end",

              p: 5,

              color: "#fff",
            }}
          >
            <Typography
              variant="h4"
              fontWeight={700}
              sx={{
                mb: 1,
              }}
            >
              Welcome to SupplyMind
            </Typography>

            <Typography
              variant="body1"
              sx={{
                maxWidth: 360,
                opacity: 0.9,
                lineHeight: 1.6,
              }}
            >
              Connect your business to smarter inventory, procurement and supply
              chain operations.
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default SignupPage;
