import {
  Box,
  Collapse,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Tooltip,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import MenuIcon from "@mui/icons-material/Menu";

import { useTheme } from "@mui/material/styles";

import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { menuItems } from "../../navigation/menuItems";

const EXPANDED_WIDTH = 250;
const COLLAPSED_WIDTH = 80;

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const theme = useTheme();

  const [open, setOpen] = useState(true);

  const getInitialSection = () => {
    const section = menuItems.find((item) =>
      item.children?.some((child) => child.path === location.pathname),
    );

    return section?.text ?? null;
  };

  const [expandedSection, setExpandedSection] = useState(getInitialSection);

  const toggleSection = (sectionName) => {
    setExpandedSection((current) =>
      current === sectionName ? null : sectionName,
    );
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const hasActiveChild = (children) => {
    return children?.some((child) => location.pathname === child.path);
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: open ? EXPANDED_WIDTH : COLLAPSED_WIDTH,

        flexShrink: 0,

        "& .MuiDrawer-paper": {
          width: open ? EXPANDED_WIDTH : COLLAPSED_WIDTH,

          overflowX: "hidden",
          overflowY: "auto",

          transition: "width 0.3s ease",

          top: "64px",
          height: "calc(100vh - 64px)",

          borderRight: "1px solid",
          borderColor: "divider",

          backgroundImage: "none",

          scrollbarWidth: "thin",

          scrollbarColor: `
            ${theme.palette.action.hover}
            transparent
          `,

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
        },
      }}
    >
      {/* -----------------------------------------------------------
          Sidebar Toggle
      ----------------------------------------------------------- */}

      <Box
        sx={{
          display: "flex",
          justifyContent: open ? "flex-end" : "center",

          p: 1,
        }}
      >
        <IconButton
          onClick={() => {
            setOpen((current) => !current);

            if (open) {
              setExpandedSection(null);
            }
          }}
        >
          <MenuIcon />
        </IconButton>
      </Box>

      {/* -----------------------------------------------------------
          Navigation
      ----------------------------------------------------------- */}

      <List
        sx={{
          px: 1,
        }}
      >
        {menuItems.map((item) => {
          const hasChildren = Boolean(item.children);

          const activeParent = hasChildren
            ? hasActiveChild(item.children)
            : isActive(item.path);

          const isExpanded = expandedSection === item.text;

          {
            /* -------------------------------------------------------
              Direct Navigation Item
          ------------------------------------------------------- */
          }

          if (!hasChildren) {
            const Icon = item.icon;

            const button = (
              <ListItemButton
                selected={isActive(item.path)}
                onClick={() => navigate(item.path)}
                sx={{
                  minHeight: 48,

                  justifyContent: open ? "initial" : "center",

                  px: 2,

                  borderRadius: 2,

                  mb: 0.5,

                  transition: "all 0.2s ease",

                  "&.Mui-selected": {
                    backgroundColor: "action.selected",
                  },

                  "&.Mui-selected:hover": {
                    backgroundColor: "action.selected",
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    minWidth: 0,

                    mr: open ? 2 : 0,

                    justifyContent: "center",
                  }}
                >
                  <Icon />
                </ListItemIcon>

                {open && (
                  <ListItemText
                    primary={item.text}
                    primaryTypographyProps={{
                      fontSize: "0.95rem",
                      fontWeight: 500,
                    }}
                  />
                )}
              </ListItemButton>
            );

            return open ? (
              <Box key={item.text}>{button}</Box>
            ) : (
              <Tooltip key={item.text} title={item.text} placement="right">
                {button}
              </Tooltip>
            );
          }

          {
            /* -------------------------------------------------------
              Parent Navigation Item
          ------------------------------------------------------- */
          }

          const ParentIcon = item.icon;

          const parentButton = (
            <ListItemButton
              onClick={() => {
                if (!open) {
                  setOpen(true);
                  setExpandedSection(item.text);

                  return;
                }

                toggleSection(item.text);
              }}
              sx={{
                minHeight: 48,

                justifyContent: open ? "initial" : "center",

                px: 2,

                borderRadius: 2,

                mb: 0.5,

                backgroundColor: activeParent
                  ? "action.selected"
                  : "transparent",

                "&:hover": {
                  backgroundColor: "action.hover",
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,

                  mr: open ? 2 : 0,

                  justifyContent: "center",
                }}
              >
                <ParentIcon />
              </ListItemIcon>

              {open && (
                <>
                  <ListItemText
                    primary={item.text}
                    primaryTypographyProps={{
                      fontSize: "0.95rem",

                      fontWeight: activeParent ? 600 : 500,
                    }}
                  />

                  {isExpanded ? (
                    <ExpandMoreIcon
                      sx={{
                        fontSize: 20,
                      }}
                    />
                  ) : (
                    <ChevronRightIcon
                      sx={{
                        fontSize: 20,
                      }}
                    />
                  )}
                </>
              )}
            </ListItemButton>
          );

          return (
            <Box key={item.text}>
              {open ? (
                parentButton
              ) : (
                <Tooltip title={item.text} placement="right">
                  {parentButton}
                </Tooltip>
              )}

              {/* -------------------------------------------------
                  Sub Navigation
              ------------------------------------------------- */}

              <Collapse in={open && isExpanded} timeout="auto" unmountOnExit>
                <List
                  component="div"
                  disablePadding
                  sx={{
                    mb: 1,
                  }}
                >
                  {item.children.map((child) => {
                    const ChildIcon = child.icon;

                    return (
                      <ListItemButton
                        key={child.text}
                        selected={isActive(child.path)}
                        onClick={() => navigate(child.path)}
                        sx={{
                          minHeight: 42,

                          pl: 6,

                          pr: 1.5,

                          borderRadius: 2,

                          mb: 0.25,

                          "&.Mui-selected": {
                            backgroundColor: "action.selected",
                          },

                          "&.Mui-selected:hover": {
                            backgroundColor: "action.selected",
                          },
                        }}
                      >
                        <ListItemIcon
                          sx={{
                            minWidth: 32,
                          }}
                        >
                          <ChildIcon />
                        </ListItemIcon>

                        <ListItemText
                          primary={child.text}
                          primaryTypographyProps={{
                            fontSize: "0.88rem",

                            fontWeight: isActive(child.path) ? 600 : 400,
                          }}
                        />
                      </ListItemButton>
                    );
                  })}
                </List>
              </Collapse>
            </Box>
          );
        })}
      </List>
    </Drawer>
  );
};

export default Sidebar;
