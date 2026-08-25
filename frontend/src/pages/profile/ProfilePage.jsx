import { Box, CircularProgress, Grid, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useSnackbar } from "notistack";

import {
  getMyProfile,
  updateMyProfile,
  changePassword,
} from "../../api/services/userService";

import { loginSuccess } from "../../store/slices/authSlice";
import { countryList, splitPhone } from "../../utils/countryCodes";

import ProfileSummaryCard from "../../components/profile/ProfileSummaryCard";
import PersonalInfoForm from "../../components/profile/PersonalInfoForm";
import SecurityForm from "../../components/profile/SecurityForm";

const ProfilePage = () => {
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();
  const currentUser = useSelector((state) => state.auth.user);

  const [profile, setProfile] = useState(null);
  const [profileForm, setProfileForm] = useState({
    full_name: "",
    countryCode: "+91",
    phone: "",
  });
  const [profileLoading, setProfileLoading] = useState(true);
  const [profileSaving, setProfileSaving] = useState(false);

  const [passwordForm, setPasswordForm] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [passwordSaving, setPasswordSaving] = useState(false);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        setProfileLoading(true);
        const data = await getMyProfile();
        const { countryCode, number } = splitPhone(data.phone);

        setProfile(data);
        setProfileForm({
          full_name: data.full_name || "",
          countryCode,
          phone: number,
        });
      } catch (error) {
        enqueueSnackbar(
          error.response?.data?.detail || "Failed to load your profile.",
          { variant: "error" },
        );
      } finally {
        setProfileLoading(false);
      }
    };

    loadProfile();
  }, [enqueueSnackbar]);

  const handleProfileSubmit = async (event) => {
    event.preventDefault();

    if (!profileForm.full_name.trim()) {
      enqueueSnackbar("Full name is required.", { variant: "warning" });
      return;
    }

    try {
      setProfileSaving(true);

      const combinedPhone = profileForm.phone.trim()
        ? `${profileForm.countryCode}${profileForm.phone.trim()}`
        : null;

      const updatedProfile = await updateMyProfile({
        full_name: profileForm.full_name.trim(),
        phone: combinedPhone,
      });

      const { countryCode, number } = splitPhone(updatedProfile.phone);

      setProfile(updatedProfile);
      setProfileForm({
        full_name: updatedProfile.full_name || "",
        countryCode,
        phone: number,
      });

      if (currentUser) {
        dispatch(
          loginSuccess({
            token:
              localStorage.getItem("accessToken") ||
              sessionStorage.getItem("accessToken"),
            user: {
              ...currentUser,
              full_name: updatedProfile.full_name,
              email: updatedProfile.email,
              role: updatedProfile.role,
            },
            rememberMe: !!localStorage.getItem("accessToken"),
          }),
        );
      }

      enqueueSnackbar("Profile updated successfully.", { variant: "success" });
    } catch (error) {
      enqueueSnackbar(
        error.response?.data?.detail || "Failed to update your profile.",
        { variant: "error" },
      );
    } finally {
      setProfileSaving(false);
    }
  };

  const handlePasswordChange = (event) => {
    const { name, value } = event.target;
    setPasswordForm((prev) => ({ ...prev, [name]: value }));
  };

  const handlePasswordSubmit = async (event) => {
    event.preventDefault();

    if (
      !passwordForm.current_password ||
      !passwordForm.new_password ||
      !passwordForm.confirm_password
    ) {
      enqueueSnackbar("Please complete all password fields.", {
        variant: "warning",
      });
      return;
    }

    if (passwordForm.new_password.length < 8) {
      enqueueSnackbar("New password must contain at least 8 characters.", {
        variant: "warning",
      });
      return;
    }

    if (passwordForm.new_password !== passwordForm.confirm_password) {
      enqueueSnackbar("New password and confirmation do not match.", {
        variant: "warning",
      });
      return;
    }

    try {
      setPasswordSaving(true);
      await changePassword({
        current_password: passwordForm.current_password,
        new_password: passwordForm.new_password,
      });

      setPasswordForm({
        current_password: "",
        new_password: "",
        confirm_password: "",
      });

      enqueueSnackbar("Password changed successfully.", { variant: "success" });
    } catch (error) {
      enqueueSnackbar(
        error.response?.data?.detail || "Failed to change password.",
        { variant: "error" },
      );
    } finally {
      setPasswordSaving(false);
    }
  };

  if (profileLoading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
        <CircularProgress size={32} />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
          }}
        >
          Profile
        </Typography>
        <Typography color="text.secondary" sx={{ mt: 0.5 }}>
          Manage your account information and security settings.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, md: 4 }}>
          <ProfileSummaryCard profile={profile} currentUser={currentUser} />
        </Grid>

        <Grid size={{ xs: 12, md: 8 }}>
          <PersonalInfoForm
            profileForm={profileForm}
            setProfileForm={setProfileForm}
            profileEmail={profile?.email || currentUser?.email}
            countryList={countryList}
            saving={profileSaving}
            onSubmit={handleProfileSubmit}
          />

          <SecurityForm
            passwordForm={passwordForm}
            handlePasswordChange={handlePasswordChange}
            saving={passwordSaving}
            onSubmit={handlePasswordSubmit}
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProfilePage;
