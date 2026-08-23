import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";

export const useFlashMessage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  
  // Ref tracking ensures the toast fires strictly once per navigation payload
  const hasFired = useRef(false);

  useEffect(() => {
    const flashState = location.state;

    if (flashState?.signupSuccess || flashState?.flashMessage) {
      if (hasFired.current) return;
      hasFired.current = true;

      const message =
        flashState.flashMessage ||
        flashState.message ||
        "Action completed successfully.";
      const variant = flashState.variant || "success";

      // 1. Trigger toast
      enqueueSnackbar(message, { variant });

      // 2. Instantly scrub browser history state
      window.history.replaceState({}, document.title);

      // 3. Clear React Router location state
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [location, navigate, enqueueSnackbar]);
};