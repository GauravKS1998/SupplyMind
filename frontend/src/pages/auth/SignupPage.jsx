import { useState } from "react";

import { Select, MenuItem } from "@mui/material";
import * as countryCodesList from "country-codes-list";

import {
  Alert,
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material";

import {
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

import AuthShell from "../../components/auth/Authshell";
import {
  useAuthTokens,
  authFieldSx,
  authSelectSx,
  authMenuPaperSx,
  authScrollbarSx,
} from "../../components/auth/authStyles";

import SupplyMindLoader from "../../components/common/Loader"; // Adjust relative path as needed

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
  const authTokens = useAuthTokens();

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

  const disabled = loading || googleLoading;

  const iconSx = { color: authTokens.textMuted, fontSize: 20 };

  return (
    <AuthShell
      headline="Create your account"
      subtext="Join SupplyMind and manage your supply chain smarter."
      imageSrc={signupImage}
      imageTitle="Welcome to SupplyMind"
      imageSubtitle="Connect your business to smarter inventory, procurement and supply chain operations."
      cardMaxWidth={480}
      footer={
        <Typography
          sx={{ fontSize: "0.875rem", color: authTokens.textSecondary }}
        >
          Already have an account?{" "}
          <MuiLink
            component={Link}
            to="/login"
            underline="hover"
            sx={{ fontWeight: 600, color: authTokens.accent }}
          >
            Log in
          </MuiLink>
        </Typography>
      }
    >
      {error && (
        <Alert
          severity="error"
          sx={{
            mb: 2.5,
            backgroundColor: authTokens.errorBg,
            color: authTokens.errorText,
            border: "1px solid rgba(214, 90, 70, 0.28)",
            "& .MuiAlert-icon": { color: authTokens.errorText },
          }}
        >
          {error}
        </Alert>
      )}

      {/* Google */}
      <Button
        fullWidth
        variant="outlined"
        size="large"
        onClick={handleGoogleSignup}
        disabled={disabled || !termsAccepted}
        sx={{
          height: 46,
          borderRadius: "10px",
          textTransform: "none",
          fontWeight: 500,
          fontSize: "0.95rem",
          color: authTokens.textPrimary,
          borderColor: "rgba(255,255,255,0.14)",
          backgroundColor: authTokens.fieldFill,
          mb: 2.5,
          "&:hover": {
            borderColor: "rgba(255,255,255,0.24)",
            backgroundColor: authTokens.fieldFillHover,
          },
        }}
        startIcon={
          googleLoading ? (
            <SupplyMindLoader size={18} color={authTokens.textPrimary} />
          ) : (
            <GoogleIcon />
          )
        }
      >
        {googleLoading ? "Connecting..." : "Sign up with Google"}
      </Button>

      {/* Divider */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 2.5 }}>
        <Box
          sx={{ flex: 1, height: "1px", backgroundColor: authTokens.divider }}
        />
        <Typography
          sx={{
            fontSize: "0.72rem",
            color: authTokens.textMuted,
            letterSpacing: 0.4,
          }}
        >
          OR
        </Typography>
        <Box
          sx={{ flex: 1, height: "1px", backgroundColor: authTokens.divider }}
        />
      </Box>

      {/* Form */}
      <Box component="form" onSubmit={handleSubmit} noValidate>
        {/* Full Name */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Full name"
          name="full_name"
          value={formData.full_name}
          onChange={handleChange}
          autoComplete="name"
          disabled={disabled}
          sx={{ ...authFieldSx(authTokens), mb: 1.75 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <PersonIcon sx={iconSx} />
                </InputAdornment>
              ),
            },
          }}
        />

        {/* Email */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          autoComplete="email"
          disabled={disabled}
          sx={{ ...authFieldSx(authTokens), mb: 1.75 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <EmailOutlined sx={iconSx} />
                </InputAdornment>
              ),
            },
          }}
        />

        {/* Phone */}
        <Box sx={{ display: "flex", gap: 1.25, mb: 1.75 }}>
          <Select
            variant="outlined"
            name="countryCode"
            value={formData.countryCode}
            onChange={handleChange}
            disabled={disabled}
            sx={{ ...authSelectSx(authTokens), width: 108 }}
            MenuProps={{
              slotProps: {
                paper: {
                  sx: {
                    ...authMenuPaperSx(authTokens),
                    ...authScrollbarSx(authTokens),
                    maxHeight: 5 * 44,
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
            value={formData.phone}
            onChange={handleChange}
            autoComplete="tel-national"
            disabled={disabled}
            sx={authFieldSx(authTokens)}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SmartphoneIcon sx={iconSx} />
                  </InputAdornment>
                ),
              },
            }}
          />
        </Box>

        {/* Company */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Company name"
          name="company_name"
          value={formData.company_name}
          onChange={handleChange}
          autoComplete="organization"
          disabled={disabled}
          sx={{ ...authFieldSx(authTokens), mb: 2 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <BusinessOutlined sx={iconSx} />
                </InputAdornment>
              ),
            },
          }}
        />

        {/* Account Type */}
        <Typography
          sx={{
            fontSize: "0.8rem",
            fontWeight: 600,
            color: authTokens.textSecondary,
            mb: 1,
          }}
        >
          Account type
        </Typography>

        <Box sx={{ display: "flex", gap: 1, mb: 2.5 }}>
          {["SUPPLIER", "CUSTOMER"].map((type) => {
            const active = formData.account_type === type;
            return (
              <Button
                key={type}
                type="button"
                fullWidth
                disabled={disabled}
                onClick={() => handleAccountTypeChange(type)}
                sx={{
                  py: 1,
                  borderRadius: "10px",
                  textTransform: "none",
                  fontWeight: 600,
                  fontSize: "0.9rem",
                  color: active ? authTokens.ctaText : authTokens.textPrimary,
                  backgroundColor: active
                    ? authTokens.accent
                    : authTokens.fieldFill,
                  border: `1px solid ${active ? authTokens.accent : "rgba(255,255,255,0.12)"}`,
                  "&:hover": {
                    backgroundColor: active
                      ? authTokens.accent
                      : authTokens.fieldFillHover,
                  },
                }}
              >
                {type === "SUPPLIER" ? "Supplier" : "Customer"}
              </Button>
            );
          })}
        </Box>

        {/* Password */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Password"
          name="password"
          type={showPassword ? "text" : "password"}
          value={formData.password}
          onChange={handleChange}
          autoComplete="new-password"
          disabled={disabled}
          sx={{ ...authFieldSx(authTokens), mb: 1.75 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <KeyIcon sx={iconSx} />
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
                      <VisibilityOff sx={iconSx} />
                    ) : (
                      <Visibility sx={iconSx} />
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
          variant="outlined"
          size="small"
          label="Confirm password"
          name="confirm_password"
          type={showConfirmPassword ? "text" : "password"}
          value={formData.confirm_password}
          onChange={handleChange}
          autoComplete="new-password"
          disabled={disabled}
          sx={{ ...authFieldSx(authTokens), mb: 1 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <KeyIcon sx={iconSx} />
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
                      <VisibilityOff sx={iconSx} />
                    ) : (
                      <Visibility sx={iconSx} />
                    )}
                  </IconButton>
                </InputAdornment>
              ),
            },
          }}
        />

        {/* Terms */}
        <FormControlLabel
          sx={{ my: 1.25, alignItems: "flex-start", mx: 0 }}
          control={
            <Checkbox
              size="small"
              checked={termsAccepted}
              onChange={(event) => setTermsAccepted(event.target.checked)}
              disabled={disabled}
              sx={{
                py: 0.5,
                mt: "-5px",
                ml: -1,
                color: authTokens.checkboxUnchecked,
                "&.Mui-checked": { color: authTokens.accent },
                "&.Mui-disabled": { color: authTokens.disabledText },
              }}
            />
          }
          label={
            <Typography
              sx={{ fontSize: "0.78rem", color: authTokens.textSecondary }}
            >
              I agree to the SupplyMind{" "}
              <MuiLink
                component={Link}
                to="/terms"
                underline="hover"
                onClick={(event) => event.stopPropagation()}
                sx={{ fontWeight: 600, color: authTokens.accent }}
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
          size="large"
          disabled={disabled || !termsAccepted}
          sx={{
            mt: 0.5,
            py: 1.2,
            borderRadius: "10px",
            fontWeight: 600,
            fontSize: "0.95rem",
            textTransform: "none",
            color: authTokens.ctaText,
            backgroundColor: authTokens.ctaBg,
            "&:hover": { backgroundColor: authTokens.ctaBgHover },
            "&.Mui-disabled": {
              backgroundColor: authTokens.disabledBg,
              color: authTokens.disabledText,
            },
          }}
        >
          {loading ? (
            <SupplyMindLoader size={22} sx={{ color: authTokens.ctaText }} />
          ) : (
            "Sign up"
          )}
        </Button>
      </Box>
    </AuthShell>
  );
};

export default SignupPage;
