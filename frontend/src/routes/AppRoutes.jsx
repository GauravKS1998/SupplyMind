import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "../components/layout/Layout";

import LoginPage from "../pages/auth/LoginPage";
import SignupPage from "../pages/auth/SignupPage";
import LandingPage from "../pages/landing/LandingPage";
import UsersPage from "../pages/users/UsersPage";
import ProfilePlaceholder from "../pages/profile/ProfilePlaceholder";

import DashboardPage from "../pages/dashboard/DashboardPage";

import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import RoleProtectedRoute from "./RoleProtectedRoute";

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* -----------------------------------------------------------
            Public Routes
        ----------------------------------------------------------- */}

        <Route path="/" element={<LandingPage />} />

        <Route element={<PublicRoute />}>
          <Route path="/login" element={<LoginPage />} />

          <Route path="/signup" element={<SignupPage />} />
        </Route>

        {/* -----------------------------------------------------------
            Protected Application
        ----------------------------------------------------------- */}

        <Route element={<ProtectedRoute />}>
          <Route path="/app" element={<Layout />}>
            {/* /app -> /app/dashboard */}
            <Route index element={<Navigate to="/app/dashboard" replace />} />

            {/* Dashboard */}
            <Route path="dashboard" element={<DashboardPage />} />

            <Route
              element={
                <RoleProtectedRoute allowedRoles={["SUPER_ADMIN", "ADMIN"]} />
              }
            >
              <Route path="users" element={<UsersPage />} />
            </Route>

            <Route path="profile" element={<ProfilePlaceholder />} />

            {/* -------------------------------------------------------
                Master Data
            ------------------------------------------------------- */}

            {/* Future:
            <Route
              path="master-data/products"
              element={<ProductsPage />}
            />

            <Route
              path="master-data/categories"
              element={<CategoriesPage />}
            />

            <Route
              path="master-data/subcategories"
              element={<SubcategoriesPage />}
            />

            <Route
              path="master-data/product-types"
              element={<ProductTypesPage />}
            />

            <Route
              path="master-data/brands"
              element={<BrandsPage />}
            />

            <Route
              path="master-data/units-of-measure"
              element={<UnitsOfMeasurePage />}
            />

            <Route
              path="master-data/suppliers"
              element={<SuppliersPage />}
            />

            <Route
              path="master-data/warehouses"
              element={<WarehousesPage />}
            />
            */}

            {/* -------------------------------------------------------
                Inventory
            ------------------------------------------------------- */}

            {/* Future:
            <Route
              path="inventory"
              element={<InventoryPage />}
            />

            <Route
              path="inventory/stock-transfers"
              element={<StockTransfersPage />}
            />

            <Route
              path="inventory/transactions"
              element={<InventoryTransactionsPage />}
            />
            */}

            {/* -------------------------------------------------------
                Procurement
            ------------------------------------------------------- */}

            {/* Future:
            <Route
              path="procurement/purchase-orders"
              element={<PurchaseOrdersPage />}
            />

            <Route
              path="procurement/goods-receipts"
              element={<GoodsReceiptsPage />}
            />
            */}

            {/* -------------------------------------------------------
                Sales
            ------------------------------------------------------- */}

            {/* Future:
            <Route
              path="sales/sales-orders"
              element={<SalesOrdersPage />}
            />
            */}

            {/* -------------------------------------------------------
                Analytics
            ------------------------------------------------------- */}

            {/* Future:
            <Route
              path="analytics/forecasting"
              element={<ForecastingPage />}
            />

            <Route
              path="analytics"
              element={<AnalyticsPage />}
            />
            */}
          </Route>
        </Route>

        {/* -----------------------------------------------------------
            Fallback
        ----------------------------------------------------------- */}

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
