import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Chip,
  Divider,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import { useTheme } from "@mui/material/styles";

import HubIcon from "@mui/icons-material/Hub";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import PersonIcon from "@mui/icons-material/Person";
import LogoutIcon from "@mui/icons-material/Logout";

import { useContext, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { ColorModeContext } from "../../theme/ColorModeContext";
import { logout } from "../../store/slices/authSlice";
import { ROLE_LABELS } from "../../constants/userConstants";

const Navbar = () => {
  const { mode, toggleTheme } = useContext(ColorModeContext);
  const theme = useTheme();

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const user = useSelector((state) => state.auth.user);

  const [accountAnchor, setAccountAnchor] = useState(null);

  const accountOpen = Boolean(accountAnchor);

  const handleAccountClick = (event) => {
    setAccountAnchor(event.currentTarget);
  };

  const handleAccountClose = () => {
    setAccountAnchor(null);
  };

  const handleProfile = () => {
    handleAccountClose();
    navigate("/app/profile");
  };

  const handleLogout = () => {
    handleAccountClose();
    dispatch(logout());
    navigate("/login", { replace: true });
  };

  const getInitials = (name) => {
    if (!name) return "?";
    return name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
      .toUpperCase();
  };

  return (
    <AppBar position="fixed" elevation={0}>
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          borderBottom: 1,
          borderColor: "divider",
        }}
      >
        {/* Branding */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1.2,
          }}
        >
          <HubIcon sx={{ fontSize: 30 }} />

          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              letterSpacing: 1,
            }}
          >
            SupplyMind
          </Typography>
        </Box>

        {/* Right Side Controls */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 1,
          }}
        >
          {/* Theme Toggle */}
          <IconButton
            color="inherit"
            onClick={toggleTheme}
            aria-label="Toggle theme"
            sx={{
              border: 1,
              borderColor: "rgba(255, 255, 255, 0.3)",
              borderRadius: 1.5,
            }}
          >
            {mode === "dark" ? (
              <LightModeIcon fontSize="small" />
            ) : (
              <DarkModeIcon fontSize="small" />
            )}
          </IconButton>

          {/* Account */}
          <IconButton
            onClick={handleAccountClick}
            aria-label="Account"
            aria-controls={accountOpen ? "account-menu" : undefined}
            aria-haspopup="true"
            aria-expanded={accountOpen ? "true" : undefined}
            sx={{ p: 0.5 }}
          >
            <Avatar
              sx={{
                width: 36,
                height: 36,
                fontSize: "0.85rem",
                fontWeight: 600,
              }}
            >
              {getInitials(user?.full_name)}
            </Avatar>
          </IconButton>
        </Box>

        {/* Account Menu */}
        <Menu
          id="account-menu"
          anchorEl={accountAnchor}
          open={accountOpen}
          onClose={handleAccountClose}
          anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
          transformOrigin={{ vertical: "top", horizontal: "right" }}
          slotProps={{
            paper: {
              elevation: 3,
              sx: {
                mt: 1.5,
                minWidth: 280,
                borderRadius: 2,
                border: 1,
                borderColor: "divider",
                overflow: "hidden",

                scrollbarWidth: "thin",
                scrollbarColor: `${theme.palette.action.hover} transparent`,
                "&::-webkit-scrollbar": { width: "6px" },
                "&::-webkit-scrollbar-track": { background: "transparent" },
                "&::-webkit-scrollbar-thumb": {
                  backgroundColor: theme.palette.action.hover,
                  borderRadius: "10px",
                },
                "&::-webkit-scrollbar-thumb:hover": {
                  backgroundColor: theme.palette.action.selected,
                },
              },
            },
          }}
        >
          {/* User Information */}
          <Box sx={{ px: 2.5, py: 2 }}>
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1.5,
              }}
            >
              <Avatar
                sx={{
                  width: 44,
                  height: 44,
                  fontWeight: 600,
                }}
              >
                {getInitials(user?.full_name)}
              </Avatar>

              <Box sx={{ minWidth: 0 }}>
                <Typography
                  variant="subtitle1"
                  sx={{
                    fontWeight: 700,
                    lineHeight: 1.3,
                  }}
                >
                  {user?.full_name || "User"}
                </Typography>

                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    wordBreak: "break-word",
                    fontSize: "0.8rem",
                  }}
                >
                  {user?.email || ""}
                </Typography>
              </Box>
            </Box>

            {/* Role */}
            {user?.role && (
              <Chip
                size="small"
                variant="outlined"
                label={ROLE_LABELS[user.role] || user.role}
                sx={{
                  mt: 1.5,
                  borderRadius: 1.5,
                  fontWeight: 600,
                  fontSize: "0.7rem",
                }}
              />
            )}
          </Box>

          <Divider />

          {/* Profile */}
          <MenuItem
            onClick={handleProfile}
            sx={{
              mx: 1,
              my: 0.5,
              borderRadius: 1.5,
            }}
          >
            <ListItemIcon>
              <PersonIcon fontSize="small" sx={{ color: "text.secondary" }} />
            </ListItemIcon>
            <ListItemText primary="Profile" />
          </MenuItem>

          {/* Logout */}
          <MenuItem
            onClick={handleLogout}
            sx={{
              mx: 1,
              mb: 0.5,
              borderRadius: 1.5,
            }}
          >
            <ListItemIcon>
              <LogoutIcon fontSize="small" sx={{ color: "text.secondary" }} />
            </ListItemIcon>
            <ListItemText primary="Log Out" />
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
