import { useState, useEffect } from "react";

import {
  Alert,
  Box,
  Button,
  Checkbox,
  // CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Link as MuiLink,
  TextField,
  Typography,
} from "@mui/material";

import { EmailOutlined, Visibility, VisibilityOff } from "@mui/icons-material";
import KeyIcon from "@mui/icons-material/Key";

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import { login } from "../../api/services/authService";
import { loginSuccess } from "../../store/slices/authSlice";

import loginImage from "../../assets/login/supplymind-login.jpg";

import { useSnackbar } from "notistack";

import AuthShell from "../../components/auth/Authshell";
import { useAuthTokens, authFieldSx } from "../../components/auth/authStyles";

import SupplyMindLoader from "../../components/common/Loader"; // Adjust relative path as needed

// -------------------------------------------------------------
// Google Icon
// -------------------------------------------------------------

export const GoogleIcon = () => {
  return (
    <Box
      component="svg"
      viewBox="0 0 24 24"
      sx={{ width: 21, height: 21, display: "block" }}
    >
      <path
        fill="#4285F4"
        d="M21.35 12.23c0-.71-.06-1.4-.18-2.05H12v3.88h5.23a4.47 4.47 0 0 1-1.94 2.93v2.43h3.14c1.84-1.69 2.92-4.18 2.92-7.19Z"
      />
      <path
        fill="#34A853"
        d="M12 21.73c2.63 0 4.84-.87 6.45-2.34l-3.14-2.43c-.87.58-1.98.93-3.31.93-2.54 0-4.69-1.72-5.46-4.03H3.3v2.5A9.74 9.74 0 0 0 12 21.73Z"
      />
      <path
        fill="#FBBC05"
        d="M6.54 13.86A5.85 5.85 0 0 1 6.23 12c0-.64.11-1.26.31-1.86v-2.5H3.3A9.73 9.73 0 0 0 2.27 12c0 1.57.38 3.05 1.03 4.36l3.24-2.5Z"
      />
      <path
        fill="#EA4335"
        d="M12 6.11c1.43 0 2.71.49 3.72 1.45l2.79-2.79C16.84 3.2 14.63 2.27 12 2.27a9.74 9.74 0 0 0-8.7 5.37l3.24 2.5C7.31 7.83 9.46 6.11 12 6.11Z"
      />
    </Box>
  );
};

// -------------------------------------------------------------
// Login Page
// -------------------------------------------------------------

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const authTokens = useAuthTokens();

  const { enqueueSnackbar } = useSnackbar();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // -----------------------------------------------------------
  // Signup success message
  // -----------------------------------------------------------

  useEffect(() => {
    if (location.state?.signupSuccess) {
      enqueueSnackbar(
        location.state.message ||
          "Account created successfully. Your account is pending approval.",
        { variant: "success" },
      );

      // Clear state in browser history immediately to prevent re-triggering
      window.history.replaceState({}, document.title);

      const timer = setTimeout(() => {
        navigate(location.pathname, {
          replace: true,
          state: {},
        });
      }, 0);

      return () => clearTimeout(timer);
    }
  }, [
    location.state?.signupSuccess,
    location.pathname,
    navigate,
    enqueueSnackbar,
    location.state?.message,
  ]);

  // -----------------------------------------------------------
  // Form change
  // -----------------------------------------------------------

  const handleChange = (event) => {
    const { name, value } = event.target;

    setError("");

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  // -----------------------------------------------------------
  // Login
  // -----------------------------------------------------------

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");

    if (!formData.email.trim()) {
      setError("Email is required.");
      return;
    }

    if (!formData.password) {
      setError("Password is required.");
      return;
    }

    try {
      setLoading(true);

      const response = await login(formData);

      dispatch(
        loginSuccess({
          token: response.access_token,
          user: response.user,
          rememberMe,
        }),
      );

      enqueueSnackbar("Login successful.", {
        variant: "success",
      });

      // Default destination after successful login.
      navigate("/app/dashboard", {
        replace: true,
      });
    } catch (err) {
      console.error("Login failed", err);

      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        "Invalid email or password.";

      enqueueSnackbar(message, {
        variant: "error",
      });

      // setError(message);
    } finally {
      setLoading(false);
    }
  };

  // -----------------------------------------------------------
  // Google login
  // -----------------------------------------------------------

  const handleGoogleLogin = () => {
    // OAuth integration will be implemented later.
    console.log("Google login selected");
  };

  const iconSx = { color: authTokens.textMuted, fontSize: 20 };

  return (
    <AuthShell
      headline="Welcome back"
      subtext="Log in to your SupplyMind account."
      imageSrc={loginImage}
      imageTitle="Welcome back"
      imageSubtitle="Pick up where you left off — inventory, procurement and supply chain, all in one place."
      cardMaxWidth={420}
      footer={
        <Typography
          sx={{ fontSize: "0.875rem", color: authTokens.textSecondary }}
        >
          Don&apos;t have an account?{" "}
          <MuiLink
            component={Link}
            to="/signup"
            underline="hover"
            sx={{ fontWeight: 600, color: authTokens.accent }}
          >
            Sign up
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
        onClick={handleGoogleLogin}
        disabled={loading}
        startIcon={<GoogleIcon />}
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
      >
        Sign in with Google
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
        {/* Email */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Email"
          name="email"
          type="email"
          placeholder="Email address"
          value={formData.email}
          onChange={handleChange}
          autoComplete="email"
          disabled={loading}
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

        {/* Password */}
        <TextField
          fullWidth
          variant="outlined"
          size="small"
          label="Password"
          name="password"
          type={showPassword ? "text" : "password"}
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          autoComplete="current-password"
          disabled={loading}
          sx={authFieldSx(authTokens)}
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
                    onClick={() => setShowPassword((previous) => !previous)}
                    edge="end"
                    disabled={loading}
                    size="small"
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

        {/* Remember + Forgot */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            mt: 1,
            mb: 2.5,
          }}
        >
          <FormControlLabel
            sx={{
              ml: -0.8,
              mr: 0,
              "& .MuiFormControlLabel-label": {
                fontSize: "0.82rem",
                color: authTokens.textSecondary,
              },
            }}
            control={
              <Checkbox
                size="small"
                checked={rememberMe}
                onChange={(event) => setRememberMe(event.target.checked)}
                disabled={loading}
                sx={{
                  color: "rgba(255,255,255,0.28)",
                  "&.Mui-checked": { color: authTokens.accent },
                }}
              />
            }
            label="Remember me"
          />

          <MuiLink
            component={Link}
            to="/forgot-password"
            underline="hover"
            sx={{
              fontSize: "0.82rem",
              fontWeight: 500,
              color: authTokens.accent,
            }}
          >
            Forgot password?
          </MuiLink>
        </Box>

        {/* Login Button */}
        <Button
          fullWidth
          type="submit"
          size="large"
          disabled={loading}
          sx={{
            height: 46,
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
            // <CircularProgress size={22} sx={{ color: authTokens.ctaText }} />
            <SupplyMindLoader size={20} color={authTokens.ctaText} />
          ) : (
            "Log in"
          )}
        </Button>
      </Box>
    </AuthShell>
  );
};

export default LoginPage;
