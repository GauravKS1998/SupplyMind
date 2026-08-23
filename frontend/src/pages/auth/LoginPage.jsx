import { useState, useEffect } from "react";

import {
  Alert,
  Box,
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Link as MuiLink,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import {
  ArrowBack,
  EmailOutlined,
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";

import KeyIcon from "@mui/icons-material/Key";

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import { login } from "../../api/services/authService";
import { loginSuccess } from "../../store/slices/authSlice";

import loginImage from "../../assets/login/supplymind-login.jpg";

import { useSnackbar } from "notistack";

// -------------------------------------------------------------
// Login media
// -------------------------------------------------------------

const IMAGE_SRC = loginImage;
const VIDEO_SRC = "";

// -------------------------------------------------------------
// Google Icon
// -------------------------------------------------------------

export const GoogleIcon = () => {
  return (
    <Box
      component="svg"
      viewBox="0 0 24 24"
      sx={{
        width: 21,
        height: 21,
        display: "block",
      }}
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

  return (
    <Box
      sx={{
        width: "100%",
        height: "100vh",
        minHeight: "100vh",
        overflow: "hidden",

        display: "flex",
        alignItems: "center",
        justifyContent: "center",

        position: "relative",

        backgroundImage: `url(${IMAGE_SRC})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      {/* -------------------------------------------------------
          Blurred background layer
      ------------------------------------------------------- */}

      <Box
        sx={{
          position: "absolute",
          inset: 0,

          backgroundImage: `url(${IMAGE_SRC})`,
          backgroundSize: "cover",
          backgroundPosition: "center",

          filter: "blur(18px)",
          transform: "scale(1.08)",

          "&::after": {
            content: '""',
            position: "absolute",
            inset: 0,
            backgroundColor: "rgba(0, 0, 0, 0.22)",
          },
        }}
      />

      {/* -------------------------------------------------------
          Main Login Card
      ------------------------------------------------------- */}

      <Paper
        elevation={18}
        sx={{
          position: "relative",
          zIndex: 1,

          width: {
            xs: "92%",
            sm: "760px",
            md: "850px",
          },

          height: {
            xs: "auto",
            sm: "520px",
            md: "560px",
          },

          maxHeight: "70vh",
          minHeight: {
            xs: "620px",
            sm: "520px",
          },

          display: "flex",

          overflow: "hidden",

          borderRadius: "18px",

          border: "0px solid rgba(255,255,255,0.45)",

          backgroundColor: "background.paper",
        }}
      >
        {/* =====================================================
            LEFT PANEL
        ===================================================== */}

        <Box
          sx={{
            width: "50%",

            position: "relative",

            display: {
              xs: "none",
              sm: "flex",
            },

            alignItems: "center",
            justifyContent: "center",

            overflow: "hidden",

            color: "#fff",

            backgroundColor: "#17212b",
          }}
        >
          {/* ---------------------------------------------------
              Video
              
              VIDEO_SRC can replace the image later without
              changing the panel structure.
          --------------------------------------------------- */}

          {VIDEO_SRC ? (
            <Box
              component="video"
              src={VIDEO_SRC}
              autoPlay
              muted
              loop
              playsInline
              sx={{
                position: "absolute",
                inset: 0,

                width: "100%",
                height: "100%",

                objectFit: "cover",
              }}
            />
          ) : (
            <Box
              component="img"
              src={IMAGE_SRC}
              alt="SupplyMind"
              sx={{
                position: "absolute",
                inset: 0,

                width: "100%",
                height: "100%",

                objectFit: "cover",
              }}
            />
          )}

          {/* ---------------------------------------------------
              Dark overlay
          --------------------------------------------------- */}

          <Box
            sx={{
              position: "absolute",
              inset: 0,

              background:
                "linear-gradient(90deg, rgba(0,0,0,0.48), rgba(0,0,0,0.18))",
            }}
          />

          {/* ---------------------------------------------------
              Welcome Content
          --------------------------------------------------- */}

          <Box
            sx={{
              position: "relative",
              zIndex: 2,

              width: "100%",

              px: {
                sm: 4,
                md: 5,
              },

              textAlign: "center",
            }}
          >
            <Typography
              sx={{
                fontSize: {
                  sm: "2.2rem",
                  md: "2.5rem",
                },

                fontWeight: 700,

                lineHeight: 1.1,

                mb: 1,
              }}
            >
              Welcome Back
            </Typography>

            <Typography
              sx={{
                fontSize: {
                  sm: "1rem",
                  md: "1.1rem",
                },

                fontWeight: 400,

                opacity: 0.95,
              }}
            >
              Log in to your SupplyMind account
            </Typography>
          </Box>
        </Box>

        {/* =====================================================
            RIGHT PANEL
        ===================================================== */}

        <Box
          sx={{
            width: {
              xs: "100%",
              sm: "50%",
            },

            height: "100%",

            display: "flex",
            flexDirection: "column",

            justifyContent: "center",

            px: {
              xs: 3,
              sm: 4,
              md: 5,
            },

            py: 3,

            overflow: "hidden",
          }}
        >
          {/* ---------------------------------------------------
              Error
          --------------------------------------------------- */}

          {error && (
            <Alert
              severity="error"
              sx={{
                mb: 1.5,
                fontSize: "0.8rem",
              }}
            >
              {error}
            </Alert>
          )}

          {/* ---------------------------------------------------
              Login Form
          --------------------------------------------------- */}

          <Box component="form" onSubmit={handleSubmit} noValidate>
            {/* Email */}

            <Typography
              variant="body2"
              sx={{
                fontWeight: 600,
                mb: 0.5,
              }}
            >
              Email
            </Typography>

            <TextField
              fullWidth
              variant="standard"
              name="email"
              type="email"
              placeholder="Email Id"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
              disabled={loading}
              size="small"
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
              sx={{
                mb: 2,
                "& .MuiInput-input": { padding: "8px 4px" },
              }}
            />

            {/* Password */}

            <Typography
              variant="body2"
              sx={{
                fontWeight: 600,
                mb: 0.5,
              }}
            >
              Password
            </Typography>

            <TextField
              fullWidth
              variant="standard"
              name="password"
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="current-password"
              disabled={loading}
              size="small"
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
                        disabled={loading}
                        size="small"
                      >
                        {showPassword ? (
                          <Visibility
                            sx={{ fontSize: 20, color: "text.secondary" }}
                          />
                        ) : (
                          <VisibilityOff
                            sx={{ fontSize: 20, color: "text.secondary" }}
                          />
                        )}
                      </IconButton>
                    </InputAdornment>
                  ),
                },
              }}
              sx={{
                "& .MuiInput-input": { padding: "8px 4px" },
              }}
            />

            {/* Remember + Forgot */}

            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",

                mt: 1.2,
                mb: 2,
              }}
            >
              <FormControlLabel
                sx={{
                  ml: -0.8,
                  mr: 0,

                  "& .MuiFormControlLabel-label": {
                    fontSize: "0.85rem",
                  },
                }}
                control={
                  <Checkbox
                    size="small"
                    checked={rememberMe}
                    onChange={(event) => setRememberMe(event.target.checked)}
                    disabled={loading}
                  />
                }
                label="Remember me"
              />

              <MuiLink
                component={Link}
                to="/forgot-password"
                underline="hover"
                sx={{
                  fontSize: "0.85rem",
                  fontWeight: 500,
                }}
              >
                Forgot password?
              </MuiLink>
            </Box>

            {/* Login Button */}

            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="medium"
              disabled={loading}
              sx={{
                height: 46,

                borderRadius: "6px",

                fontWeight: 600,

                textTransform: "none",

                boxShadow: "none",

                "&:hover": {
                  boxShadow: "none",
                },
              }}
            >
              {loading ? (
                <CircularProgress size={22} color="inherit" />
              ) : (
                "Log In"
              )}
            </Button>
          </Box>

          {/* ---------------------------------------------------
              OR Divider
          --------------------------------------------------- */}

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
                backgroundColor: "divider",
              }}
            />

            <Typography
              variant="caption"
              sx={{
                fontWeight: 600,
              }}
            >
              OR
            </Typography>

            <Box
              sx={{
                flex: 1,
                height: "1px",
                backgroundColor: "divider",
              }}
            />
          </Box>

          {/* ---------------------------------------------------
              Google Login
          --------------------------------------------------- */}

          <Button
            fullWidth
            variant="outlined"
            onClick={handleGoogleLogin}
            startIcon={<GoogleIcon />}
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
          >
            Sign in with Google
          </Button>

          {/* ---------------------------------------------------
              Sign Up
          --------------------------------------------------- */}

          <Typography
            variant="body2"
            sx={{
              textAlign: "center",
              mt: 2,

              fontSize: "0.85rem",
            }}
          >
            Don't have an account?{" "}
            <MuiLink
              component={Link}
              to="/signup"
              underline="hover"
              sx={{
                fontWeight: 600,
              }}
            >
              Sign Up
            </MuiLink>
          </Typography>

          {/* ---------------------------------------------------
              Back to SupplyMind
          --------------------------------------------------- */}

          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              mt: 1.5,
            }}
          >
            <MuiLink
              component={Link}
              to="/"
              underline="hover"
              sx={{
                display: "inline-flex",
                alignItems: "center",
                gap: 0.7,
                fontSize: "0.85rem",
                fontWeight: 500,
              }}
            >
              <ArrowBack fontSize="small" />
              Back to SupplyMind
            </MuiLink>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default LoginPage;
