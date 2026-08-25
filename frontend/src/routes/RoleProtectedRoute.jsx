import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

const RoleProtectedRoute = ({ allowedRoles }) => {
  const user = useSelector((state) => state.auth.user);

  const hasAccess = allowedRoles.includes(user?.role);

  if (!hasAccess) {
    return <Navigate to="/app/dashboard" replace />;
  }

  return <Outlet />;
};

export default RoleProtectedRoute;
