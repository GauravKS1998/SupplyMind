import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

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

const Navbar = () => {
  const { mode, toggleTheme } = useContext(ColorModeContext);

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

    navigate("/login", {
      replace: true,
    });
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
    <AppBar position="fixed" elevation={2}>
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
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
          <HubIcon
            sx={{
              fontSize: 30,
            }}
          />

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
            gap: 0.5,
          }}
        >
          {/* Theme Toggle */}
          <IconButton
            color="inherit"
            onClick={toggleTheme}
            aria-label="Toggle theme"
          >
            {mode === "dark" ? <LightModeIcon /> : <DarkModeIcon />}
          </IconButton>

          {/* Account */}
          <IconButton
            color="inherit"
            onClick={handleAccountClick}
            aria-label="Account"
            aria-controls={accountOpen ? "account-menu" : undefined}
            aria-haspopup="true"
            aria-expanded={accountOpen ? "true" : undefined}
          >
            <Avatar
              sx={{
                width: 36,
                height: 36,
                fontSize: "0.9rem",
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
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "right",
          }}
          transformOrigin={{
            vertical: "top",
            horizontal: "right",
          }}
          slotProps={{
            paper: {
              sx: {
                mt: 1,
                minWidth: 260,
              },
            },
          }}
        >
          {/* User Information */}
          <Box
            sx={{
              px: 2,
              py: 1.5,
            }}
          >
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
                    fontWeight: 600,
                  }}
                >
                  {user?.full_name || "User"}
                </Typography>

                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    wordBreak: "break-word",
                  }}
                >
                  {user?.email || ""}
                </Typography>
              </Box>
            </Box>

            {/* Role */}
            {user?.role && (
              <Typography
                variant="caption"
                color="text.secondary"
                sx={{
                  display: "block",
                  mt: 1,
                }}
              >
                Role: {user.role}
              </Typography>
            )}
          </Box>

          <Divider />

          {/* Profile */}
          <MenuItem onClick={handleProfile}>
            <ListItemIcon>
              <PersonIcon fontSize="small" />
            </ListItemIcon>

            <ListItemText primary="Profile" />
          </MenuItem>

          {/* Logout */}
          <MenuItem onClick={handleLogout}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" />
            </ListItemIcon>

            <ListItemText primary="Log Out" />
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
