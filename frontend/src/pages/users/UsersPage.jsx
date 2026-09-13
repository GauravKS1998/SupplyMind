import { useCallback, useEffect, useState } from "react";

import {
  Alert,
  Avatar,
  Box,
  Button,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  FormControl,
  InputLabel,
  Menu,
  MenuItem,
  Paper,
  Select,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  Tooltip,
  TextField,
  Typography,
} from "@mui/material";

import MoreVertIcon from "@mui/icons-material/MoreVert";
import AddIcon from "@mui/icons-material/Add";
import SearchIcon from "@mui/icons-material/Search";
import RefreshIcon from "@mui/icons-material/Refresh";

import { useSnackbar } from "notistack";
import { useSelector } from "react-redux";

import {
  approveUser,
  rejectUser,
  activateUser,
  deactivateUser,
  changeUserRole,
  createInternalUser,
  searchUsers,
} from "../../api/services/userService";

import {
  ROLES,
  INTERNAL_ROLES,
  CREATE_EMPLOYEE_ROLES,
  APPROVAL_STATUS,
  APPROVAL_STATUS_COLORS,
  ROLE_LABELS,
} from "../../constants/userConstants";

import SupplyMindLoader from "../../components/common/Loader";
import {
  useAuthTokens,
  authScrollbarSx,
  authFieldSx,
  authSelectSx,
  authMenuPaperSx,
} from "../../components/auth/authStyles";

/* ==================================================
   Helpers
================================================== */

const getRoleLabel = (role) => ROLE_LABELS[role] || role;

const getInitials = (name) => {
  if (!name) return "?";
  return name
    .split(" ")
    .filter(Boolean)
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
};

const getApprovalColor = (status) =>
  APPROVAL_STATUS_COLORS[status] || "default";

const hasAvailableActions = (user) => {
  if (!user) return false;
  // REJECTED users have no available actions
  return (
    user.approval_status === APPROVAL_STATUS.PENDING ||
    user.approval_status === APPROVAL_STATUS.APPROVED
  );
};

const canChangeRole = (user) => {
  if (!user) return false;

  return (
    INTERNAL_ROLES.includes(user.role) &&
    user.approval_status === APPROVAL_STATUS.APPROVED
  );
};

/* ==================================================
   Component
================================================== */

const UsersPage = () => {
  const { enqueueSnackbar } = useSnackbar();
  const brand = useAuthTokens();
  const currentUser = useSelector((state) => state.auth.user);

  // Shared dropdown paper style (matches the country-code select
  // used in PersonalInfoForm) — reused by every Select on this page.
  const selectMenuProps = {
    slotProps: {
      paper: {
        sx: {
          maxHeight: 5 * 44,
          ...authMenuPaperSx(brand),
          ...authScrollbarSx(brand),
        },
      },
    },
  };

  /* --------------------------------------------------
     Users
  -------------------------------------------------- */

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* --------------------------------------------------
     Pagination
  -------------------------------------------------- */

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalItems, setTotalItems] = useState(0);

  /* --------------------------------------------------
     Search / Filters
  -------------------------------------------------- */

  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("");
  const [approvalFilter, setApprovalFilter] = useState("");
  const [activeFilter, setActiveFilter] = useState("");
  const [sortBy, setSortBy] = useState("created_at");
  const [sortDirection, setSortDirection] = useState("desc");

  /* --------------------------------------------------
     Action Menu
  -------------------------------------------------- */

  const [actionAnchor, setActionAnchor] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);

  /* --------------------------------------------------
     Reject Dialog
  -------------------------------------------------- */

  const [rejectDialogOpen, setRejectDialogOpen] = useState(false);
  const [rejectReason, setRejectReason] = useState("");

  /* --------------------------------------------------
     Role Dialog
  -------------------------------------------------- */

  const [roleDialogOpen, setRoleDialogOpen] = useState(false);
  const [newRole, setNewRole] = useState("");

  /* --------------------------------------------------
     Create Employee Dialog
  -------------------------------------------------- */

  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [employeeForm, setEmployeeForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
    role: ROLES.ADMIN,
  });

  /* ==================================================
     Load Users
  ================================================== */

  const loadUsers = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await searchUsers({
        page: page + 1,
        size: rowsPerPage,
        search: search.trim() || null,
        role: roleFilter || null,
        approval_status: approvalFilter || null,
        is_active: activeFilter === "" ? null : activeFilter === "true",
        sort_by: sortBy,
        direction: sortDirection,
      });

      setUsers(response.items || []);
      setTotalItems(response.pagination?.total_items || 0);
    } catch (err) {
      const message = err.response?.data?.detail || "Failed to load users.";

      setError(message);

      enqueueSnackbar(message, {
        variant: "error",
      });
    } finally {
      setLoading(false);
    }
  }, [
    page,
    rowsPerPage,
    search,
    roleFilter,
    approvalFilter,
    activeFilter,
    sortBy,
    sortDirection,
    enqueueSnackbar,
  ]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- legitimate data fetch, not a derived-state anti-pattern
    loadUsers();
  }, [loadUsers]);

  /* ==================================================
     Action Menu
  ================================================== */

  const handleActionMenuOpen = (event, user) => {
    setActionAnchor(event.currentTarget);
    setSelectedUser(user);
  };

  const handleActionMenuClose = () => {
    setActionAnchor(null);
  };

  /* ==================================================
     Approve
  ================================================== */

  const handleApprove = async () => {
    if (!selectedUser) {
      return;
    }
    try {
      await approveUser(selectedUser.id);
      enqueueSnackbar("User approved successfully.", {
        variant: "success",
      });
      handleActionMenuClose();

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(err.response?.data?.detail || "Failed to approve user.", {
        variant: "error",
      });
    }
  };

  /* ==================================================
     Reject
  ================================================== */

  const handleRejectOpen = () => {
    setRejectReason("");
    handleActionMenuClose();
    setRejectDialogOpen(true);
  };

  const handleReject = async () => {
    if (!selectedUser) {
      return;
    }
    if (rejectReason.trim().length < 3) {
      enqueueSnackbar("Rejection reason must contain at least 3 characters.", {
        variant: "warning",
      });
      return;
    }
    try {
      await rejectUser(selectedUser.id, {
        reason: rejectReason.trim(),
      });
      enqueueSnackbar("User rejected successfully.", {
        variant: "success",
      });
      setRejectDialogOpen(false);
      setRejectReason("");
      setSelectedUser(null);

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(err.response?.data?.detail || "Failed to reject user.", {
        variant: "error",
      });
    }
  };

  /* ==================================================
     Activate
  ================================================== */

  const handleActivate = async () => {
    if (!selectedUser) {
      return;
    }
    try {
      await activateUser(selectedUser.id);
      enqueueSnackbar("User activated successfully.", {
        variant: "success",
      });
      handleActionMenuClose();

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(
        err.response?.data?.detail || "Failed to activate user.",
        {
          variant: "error",
        },
      );
    }
  };

  /* ==================================================
     Deactivate
  ================================================== */

  const handleDeactivate = async () => {
    if (!selectedUser) {
      return;
    }
    try {
      await deactivateUser(selectedUser.id);
      enqueueSnackbar("User deactivated successfully.", {
        variant: "success",
      });
      handleActionMenuClose();

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(
        err.response?.data?.detail || "Failed to deactivate user.",
        {
          variant: "error",
        },
      );
    }
  };

  /* ==================================================
     Change Role
  ================================================== */

  const handleChangeRoleOpen = () => {
    if (!selectedUser) {
      return;
    }
    setNewRole(selectedUser.role);
    handleActionMenuClose();
    setRoleDialogOpen(true);
  };

  const handleChangeRole = async () => {
    if (!selectedUser || !newRole) {
      return;
    }
    if (newRole === selectedUser.role) {
      enqueueSnackbar("User already has this role.", {
        variant: "info",
      });
      return;
    }
    try {
      await changeUserRole(selectedUser.id, {
        role: newRole,
      });
      enqueueSnackbar("User role updated successfully.", {
        variant: "success",
      });
      setRoleDialogOpen(false);
      setNewRole("");
      setSelectedUser(null);

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(
        err.response?.data?.detail || "Failed to change user role.",
        {
          variant: "error",
        },
      );
    }
  };

  /* ==================================================
     Create Employee
  ================================================== */

  const handleCreateEmployeeOpen = () => {
    setEmployeeForm({
      full_name: "",
      email: "",
      phone: "",
      password: "",
      role: ROLES.ADMIN,
    });
    setCreateDialogOpen(true);
  };

  const handleCreateEmployee = async () => {
    if (!employeeForm.full_name.trim()) {
      enqueueSnackbar("Full name is required.", {
        variant: "warning",
      });
      return;
    }

    if (!employeeForm.email.trim()) {
      enqueueSnackbar("Email is required.", {
        variant: "warning",
      });
      return;
    }

    if (!employeeForm.password) {
      enqueueSnackbar("Password is required.", {
        variant: "warning",
      });
      return;
    }

    if (employeeForm.password.length < 8) {
      enqueueSnackbar("Password must contain at least 8 characters.", {
        variant: "warning",
      });
      return;
    }

    try {
      await createInternalUser({
        full_name: employeeForm.full_name.trim(),
        email: employeeForm.email.trim(),
        phone: employeeForm.phone.trim() || null,
        password: employeeForm.password,
        role: employeeForm.role,
      });

      enqueueSnackbar("Employee created successfully.", {
        variant: "success",
      });
      setCreateDialogOpen(false);

      await loadUsers();
    } catch (err) {
      enqueueSnackbar(
        err.response?.data?.detail || "Failed to create employee.",
        {
          variant: "error",
        },
      );
    }
  };

  /* ==================================================
     Pagination
  ================================================== */

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  /* ==================================================
     Search
  ================================================== */

  const handleSearchChange = (event) => {
    setSearch(event.target.value);
    setPage(0);
  };

  /* ==================================================
     Role options for change dialog
  ================================================== */

  const roleOptions = CREATE_EMPLOYEE_ROLES;

  /* ==================================================
     Render
  ================================================== */

  return (
    <Box
      sx={{
        p: 3,
      }}
    >
      {/* ==================================================
          Header
      ================================================== */}

      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          mb: 3,
        }}
      >
        <Box>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 700,
              fontFamily: brand.fontDisplay,
            }}
          >
            User Management
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mt: 0.5,
              fontFamily: brand.fontBody,
            }}
          >
            Manage employees, customers, suppliers, approvals and account
            access.
          </Typography>
        </Box>

        {currentUser?.role === ROLES.SUPER_ADMIN && (
          <Button
            variant="contained"
            disableElevation
            startIcon={<AddIcon />}
            onClick={handleCreateEmployeeOpen}
            sx={{
              borderRadius: "10px",
              px: 2.5,
              py: 1,
              fontWeight: 600,
              textTransform: "none",
              fontFamily: brand.fontBody,
              color: brand.ctaText,
              backgroundColor: brand.ctaBg,
              "&:hover": {
                backgroundColor: brand.ctaBgHover,
              },
            }}
          >
            Add Employee
          </Button>
        )}
      </Box>

      {/* ==================================================
          Filters & Controls Section
      ================================================== */}

      <Paper
        elevation={0}
        variant="outlined"
        sx={{
          p: 2,
          mb: 3,
          borderRadius: 5,
          borderColor: "divider",
          backgroundColor: brand.pageBg,
          transition: "background-color 0.2s ease, color 0.2s ease",
        }}
      >
        <Box
          sx={{
            display: "flex",
            gap: 2,
            flexWrap: "wrap",
            alignItems: "center",
          }}
        >
          <TextField
            size="small"
            label="Search users"
            name="user-table-search"
            placeholder="Search by name, email..."
            autoComplete="off"
            value={search}
            onChange={handleSearchChange}
            sx={{ ...authFieldSx(brand), minWidth: 240, flexGrow: 1 }}
            slotProps={{
              input: {
                startAdornment: (
                  <SearchIcon
                    fontSize="small"
                    sx={{
                      mr: 1,
                      color: "text.secondary",
                    }}
                  />
                ),
              },
            }}
          />

          {/* Role Filter */}
          <FormControl
            size="small"
            sx={{ ...authSelectSx(brand), minWidth: 160 }}
          >
            <InputLabel id="role-filter-label">Role</InputLabel>
            <Select
              labelId="role-filter-label"
              label="Role"
              value={roleFilter}
              onChange={(e) => {
                setRoleFilter(e.target.value);
                setPage(0);
              }}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              <MenuItem value="">All Roles</MenuItem>
              {Object.values(ROLES).map((roleKey) => (
                <MenuItem key={roleKey} value={roleKey}>
                  {getRoleLabel(roleKey)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Approval Filter */}
          <FormControl
            size="small"
            sx={{ ...authSelectSx(brand), minWidth: 160 }}
          >
            <InputLabel id="approval-filter-label">Approval Status</InputLabel>
            <Select
              labelId="approval-filter-label"
              label="Approval Status"
              value={approvalFilter}
              onChange={(e) => {
                setApprovalFilter(e.target.value);
                setPage(0);
              }}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              <MenuItem value="">All Statuses</MenuItem>
              {Object.values(APPROVAL_STATUS).map((status) => (
                <MenuItem key={status} value={status}>
                  {status}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Account Filter */}
          <FormControl
            size="small"
            sx={{ ...authSelectSx(brand), minWidth: 140 }}
          >
            <InputLabel id="account-filter-label">Account</InputLabel>
            <Select
              labelId="account-filter-label"
              label="Account"
              value={activeFilter}
              onChange={(e) => {
                setActiveFilter(e.target.value);
                setPage(0);
              }}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              <MenuItem value="">All Accounts</MenuItem>
              <MenuItem value="true">Active</MenuItem>
              <MenuItem value="false">Inactive</MenuItem>
            </Select>
          </FormControl>

          {/* Sort Field */}
          <FormControl
            size="small"
            sx={{ ...authSelectSx(brand), minWidth: 140 }}
          >
            <InputLabel id="sort-by-label">Sort By</InputLabel>
            <Select
              labelId="sort-by-label"
              label="Sort By"
              value={sortBy}
              onChange={(e) => {
                setSortBy(e.target.value);
                setPage(0);
              }}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              <MenuItem value="created_at">Date Created</MenuItem>
              <MenuItem value="full_name">Name</MenuItem>
              <MenuItem value="email">Email</MenuItem>
            </Select>
          </FormControl>

          {/* Sort Direction */}
          <FormControl
            size="small"
            sx={{ ...authSelectSx(brand), minWidth: 110 }}
          >
            <InputLabel id="sort-order-label">Order</InputLabel>
            <Select
              labelId="sort-order-label"
              label="Order"
              value={sortDirection}
              onChange={(e) => {
                setSortDirection(e.target.value);
                setPage(0);
              }}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              <MenuItem value="desc">Newest</MenuItem>
              <MenuItem value="asc">Oldest</MenuItem>
            </Select>
          </FormControl>

          {/* Refresh Action */}
          <Tooltip title="Refresh Table">
            <span style={{ display: "inline-flex" }}>
              <IconButton
                onClick={loadUsers}
                disabled={loading}
                sx={{ border: 1, borderColor: "divider", borderRadius: 1.5 }}
              >
                <RefreshIcon fontSize="small" />
              </IconButton>
            </span>
          </Tooltip>
        </Box>
      </Paper>

      {/* ==================================================
          Error
      ================================================== */}

      {error && (
        <Alert
          severity="error"
          sx={{
            mb: 2,
            borderRadius: 2,
          }}
        >
          {error}
        </Alert>
      )}

      {/* ==================================================
          Table
      ================================================== */}

      <Paper
        elevation={0}
        variant="outlined"
        sx={{
          borderRadius: 5,
          overflow: "hidden",
          borderColor: "divider",
          backgroundColor: brand.pageBg,
          transition: "background-color 0.2s ease, color 0.2s ease",
        }}
      >
        <TableContainer
          sx={{
            // scrolls horizontally on small screens
            ...authScrollbarSx(brand),
          }}
        >
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 600, fontFamily: brand.fontBody }}>
                  User
                </TableCell>
                <TableCell sx={{ fontWeight: 600, fontFamily: brand.fontBody }}>
                  Role
                </TableCell>
                <TableCell sx={{ fontWeight: 600, fontFamily: brand.fontBody }}>
                  Approval
                </TableCell>
                <TableCell sx={{ fontWeight: 600, fontFamily: brand.fontBody }}>
                  Account
                </TableCell>
                <TableCell sx={{ fontWeight: 600, fontFamily: brand.fontBody }}>
                  Created
                </TableCell>
                <TableCell
                  align="right"
                  sx={{ fontWeight: 600, fontFamily: brand.fontBody }}
                >
                  Actions
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    align="center"
                    sx={{
                      py: 6,
                    }}
                  >
                    <Box sx={{ display: "flex", justifyContent: "center" }}>
                      <SupplyMindLoader size={30} color={brand.accent} />
                    </Box>
                  </TableCell>
                </TableRow>
              ) : users.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    align="center"
                    sx={{
                      py: 6,
                    }}
                  >
                    <Typography
                      color="text.secondary"
                      sx={{ fontFamily: brand.fontBody }}
                    >
                      No users found.
                    </Typography>
                  </TableCell>
                </TableRow>
              ) : (
                users.map((user) => (
                  <TableRow key={user.id} hover>
                    {/* User */}

                    <TableCell>
                      <Box
                        sx={{
                          display: "flex",
                          alignItems: "center",
                          gap: 1.5,
                        }}
                      >
                        <Avatar
                          sx={{
                            width: 36,
                            height: 36,
                            fontSize: 14,
                            fontWeight: 600,
                            fontFamily: brand.fontDisplay,
                            bgcolor: brand.accent,
                            color: brand.ctaText,
                          }}
                        >
                          {getInitials(user.full_name)}
                        </Avatar>

                        <Box>
                          <Typography
                            sx={{
                              fontWeight: 600,
                              fontSize: "0.875rem",
                              fontFamily: brand.fontBody,
                            }}
                          >
                            {user.full_name}
                          </Typography>

                          <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{
                              fontSize: "0.775rem",
                              fontFamily: brand.fontBody,
                            }}
                          >
                            {user.email}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>

                    {/* Role */}

                    <TableCell>
                      <Chip
                        size="small"
                        label={getRoleLabel(user.role)}
                        variant="outlined"
                        sx={{
                          borderRadius: 1.5,
                          borderColor: brand.accent,
                          color: brand.accent,
                          fontFamily: brand.fontBody,
                        }}
                      />
                    </TableCell>

                    {/* Approval */}

                    <TableCell>
                      <Chip
                        size="small"
                        label={user.approval_status}
                        color={getApprovalColor(user.approval_status)}
                        sx={{ fontWeight: 600 }}
                      />
                    </TableCell>

                    {/* Account */}

                    <TableCell>
                      <Chip
                        size="small"
                        label={user.is_active ? "Active" : "Inactive"}
                        color={user.is_active ? "success" : "default"}
                        variant={user.is_active ? "filled" : "outlined"}
                      />
                    </TableCell>

                    {/* Created */}

                    <TableCell>
                      {user.created_at
                        ? new Date(user.created_at).toLocaleDateString()
                        : "—"}
                    </TableCell>

                    {/* Actions Column: Hides button if user is REJECTED */}
                    <TableCell align="right">
                      {hasAvailableActions(user) ? (
                        <IconButton
                          onClick={(event) => handleActionMenuOpen(event, user)}
                        >
                          <MoreVertIcon fontSize="small" />
                        </IconButton>
                      ) : (
                        <Typography
                          variant="body2"
                          color="text.disabled"
                          sx={{ px: 1 }}
                        ></Typography>
                      )}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          component="div"
          count={totalItems}
          page={page}
          onPageChange={handlePageChange}
          rowsPerPage={rowsPerPage}
          onRowsPerPageChange={handleRowsPerPageChange}
          rowsPerPageOptions={[5, 10, 20, 50]}
        />
      </Paper>

      {/* ==================================================
          User Action Menu
      ================================================== */}

      <Menu
        anchorEl={actionAnchor}
        open={Boolean(actionAnchor)}
        onClose={handleActionMenuClose}
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
              minWidth: 140,
              borderRadius: 2,
              border: 1,
              borderColor: "divider",
              backgroundColor: brand.pageBg,
              backgroundImage: "none",
            },
          },
        }}
      >
        {selectedUser?.approval_status === APPROVAL_STATUS.PENDING && [
          <MenuItem key="approve" onClick={handleApprove}>
            Approve
          </MenuItem>,
          <MenuItem key="reject" onClick={handleRejectOpen}>
            Reject
          </MenuItem>,
        ]}

        {selectedUser?.approval_status === APPROVAL_STATUS.APPROVED &&
          !selectedUser?.is_active && (
            <MenuItem onClick={handleActivate}>Activate</MenuItem>
          )}

        {selectedUser?.approval_status === APPROVAL_STATUS.APPROVED &&
          selectedUser?.is_active && (
            <MenuItem onClick={handleDeactivate}>Deactivate</MenuItem>
          )}

        {canChangeRole(selectedUser) && (
          <MenuItem onClick={handleChangeRoleOpen}>Change Role</MenuItem>
        )}
      </Menu>

      {/* ==================================================
          Reject Dialog
      ================================================== */}

      <Dialog
        open={rejectDialogOpen}
        onClose={() => setRejectDialogOpen(false)}
        fullWidth
        maxWidth="sm"
        slotProps={{
          paper: {
            sx: {
              borderRadius: 3,
              p: 1,
              backgroundColor: brand.pageBg,
              backgroundImage: "none",
            },
          },
        }}
      >
        <DialogTitle sx={{ pb: 1, pt: 2.5, px: 3 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              letterSpacing: "-0.5px",
              fontFamily: brand.fontDisplay,
            }}
          >
            Reject User
          </Typography>
        </DialogTitle>

        <DialogContent sx={{ px: 3, py: 2 }}>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mb: 2,
              fontFamily: brand.fontBody,
            }}
          >
            You are rejecting <strong>{selectedUser?.full_name}</strong>.
          </Typography>

          <TextField
            fullWidth
            variant="outlined"
            multiline
            minRows={4}
            label="Rejection Reason"
            value={rejectReason}
            onChange={(event) => setRejectReason(event.target.value)}
            inputProps={{
              maxLength: 500,
            }}
            helperText={`${rejectReason.length}/500`}
            sx={authFieldSx(brand)}
          />
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 2.5, pt: 1.5 }}>
          <Button
            onClick={() => setRejectDialogOpen(false)}
            sx={{ textTransform: "none", color: "text.secondary" }}
          >
            Cancel
          </Button>

          <Button
            color="error"
            variant="contained"
            disableElevation
            onClick={handleReject}
            sx={{
              borderRadius: "10px",
              px: 3,
              fontWeight: 600,
              textTransform: "none",
            }}
          >
            Reject User
          </Button>
        </DialogActions>
      </Dialog>

      {/* ==================================================
          Change Role Dialog
      ================================================== */}

      <Dialog
        open={roleDialogOpen}
        onClose={() => setRoleDialogOpen(false)}
        fullWidth
        maxWidth="xs"
        slotProps={{
          paper: {
            sx: {
              borderRadius: 3,
              p: 1,
              backgroundColor: brand.pageBg,
              backgroundImage: "none",
            },
          },
        }}
      >
        <DialogTitle sx={{ pb: 1, pt: 2.5, px: 3 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              letterSpacing: "-0.5px",
              fontFamily: brand.fontDisplay,
            }}
          >
            Change User Role
          </Typography>
        </DialogTitle>

        <DialogContent sx={{ px: 3, py: 2 }}>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mb: 2,
              fontFamily: brand.fontBody,
            }}
          >
            Change the role for <strong>{selectedUser?.full_name}</strong>.
          </Typography>

          <FormControl fullWidth variant="outlined" sx={authSelectSx(brand)}>
            <InputLabel id="change-role-label">Role *</InputLabel>
            <Select
              labelId="change-role-label"
              label="Role *"
              value={newRole}
              onChange={(event) => setNewRole(event.target.value)}
              sx={authSelectSx(brand)}
              MenuProps={selectMenuProps}
            >
              {roleOptions.map((role) => (
                <MenuItem key={role} value={role}>
                  {getRoleLabel(role)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 2.5, pt: 1.5 }}>
          <Button
            onClick={() => setRoleDialogOpen(false)}
            sx={{ textTransform: "none", color: "text.secondary" }}
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            disableElevation
            onClick={handleChangeRole}
            sx={{
              borderRadius: "10px",
              px: 3,
              fontWeight: 600,
              textTransform: "none",
              color: brand.ctaText,
              backgroundColor: brand.ctaBg,
              "&:hover": {
                backgroundColor: brand.ctaBgHover,
              },
            }}
          >
            Change Role
          </Button>
        </DialogActions>
      </Dialog>

      {/* ==================================================
          Create Employee Dialog
      ================================================== */}

      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        fullWidth
        maxWidth="sm"
        slotProps={{
          paper: {
            sx: {
              borderRadius: 3,
              p: 1,
              backgroundColor: brand.pageBg,
              backgroundImage: "none",
            },
          },
        }}
      >
        <DialogTitle sx={{ pb: 1, pt: 2.5, px: 3 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              letterSpacing: "-0.5px",
              fontFamily: brand.fontDisplay,
            }}
          >
            Create Employee
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ mt: 0.5, fontFamily: brand.fontBody }}
          >
            Internal employees are created as approved and active accounts.
          </Typography>
        </DialogTitle>

        <DialogContent sx={{ px: 3, py: 2 }}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: 2,
              mt: 1,
            }}
          >
            <TextField
              variant="outlined"
              label="Full Name"
              required
              fullWidth
              name="full_name"
              autoComplete="off"
              value={employeeForm.full_name}
              onChange={(event) =>
                setEmployeeForm((previous) => ({
                  ...previous,
                  full_name: event.target.value,
                }))
              }
              sx={authFieldSx(brand)}
            />

            <TextField
              variant="outlined"
              label="Email"
              type="email"
              required
              fullWidth
              name="email"
              autoComplete="off"
              value={employeeForm.email}
              onChange={(event) =>
                setEmployeeForm((previous) => ({
                  ...previous,
                  email: event.target.value,
                }))
              }
              sx={authFieldSx(brand)}
            />

            <TextField
              variant="outlined"
              label="Phone"
              fullWidth
              name="phone"
              autoComplete="off"
              value={employeeForm.phone}
              onChange={(event) =>
                setEmployeeForm((previous) => ({
                  ...previous,
                  phone: event.target.value,
                }))
              }
              sx={authFieldSx(brand)}
            />

            <TextField
              variant="outlined"
              label="Temporary Password"
              type="password"
              required
              fullWidth
              name="password"
              autoComplete="new-password"
              value={employeeForm.password}
              onChange={(event) =>
                setEmployeeForm((previous) => ({
                  ...previous,
                  password: event.target.value,
                }))
              }
              helperText="Minimum 8 characters"
              sx={authFieldSx(brand)}
            />

            <FormControl fullWidth variant="outlined" sx={authSelectSx(brand)}>
              <InputLabel id="employee-role-label">Role *</InputLabel>
              <Select
                labelId="employee-role-label"
                label="Role *"
                value={employeeForm.role}
                onChange={(e) =>
                  setEmployeeForm((prev) => ({ ...prev, role: e.target.value }))
                }
                sx={authSelectSx(brand)}
                MenuProps={selectMenuProps}
              >
                {CREATE_EMPLOYEE_ROLES.map((role) => (
                  <MenuItem key={role} value={role}>
                    {getRoleLabel(role)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 2.5, pt: 1.5 }}>
          <Button
            onClick={() => setCreateDialogOpen(false)}
            sx={{ textTransform: "none", color: "text.secondary" }}
          >
            Cancel
          </Button>

          <Button
            variant="contained"
            disableElevation
            onClick={handleCreateEmployee}
            sx={{
              borderRadius: "10px",
              px: 3,
              fontWeight: 600,
              textTransform: "none",
              color: brand.ctaText,
              backgroundColor: brand.ctaBg,
              "&:hover": {
                backgroundColor: brand.ctaBgHover,
              },
            }}
          >
            Create Employee
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UsersPage;
