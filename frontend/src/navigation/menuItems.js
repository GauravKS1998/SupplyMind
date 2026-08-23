import DashboardIcon from "@mui/icons-material/Dashboard";
import InventoryIcon from "@mui/icons-material/Inventory";
import WarehouseIcon from "@mui/icons-material/Warehouse";
import SwapHorizIcon from "@mui/icons-material/SwapHoriz";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import LocalShippingIcon from "@mui/icons-material/LocalShipping";
import AssessmentIcon from "@mui/icons-material/Assessment";
import CategoryIcon from "@mui/icons-material/Category";
import BusinessIcon from "@mui/icons-material/Business";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing";
import StraightenIcon from "@mui/icons-material/Straighten";
import StyleIcon from "@mui/icons-material/Style";

export const menuItems = [
  // -------------------------------------------------------------------
  // Dashboard
  // -------------------------------------------------------------------

  {
    type: "item",
    text: "Dashboard",
    icon: DashboardIcon,
    path: "/app/dashboard",
  },

  // -------------------------------------------------------------------
  // Master Data
  // -------------------------------------------------------------------

  {
    type: "section",
    text: "Master Data",
    icon: CategoryIcon,

    children: [
      {
        text: "Products",
        icon: InventoryIcon,
        path: "/app/master-data/products",
      },
      {
        text: "Categories",
        icon: CategoryIcon,
        path: "/app/master-data/categories",
      },
      {
        text: "Subcategories",
        icon: CategoryIcon,
        path: "/app/master-data/subcategories",
      },
      {
        text: "Product Types",
        icon: PrecisionManufacturingIcon,
        path: "/app/master-data/product-types",
      },
      {
        text: "Brands",
        icon: StyleIcon,
        path: "/app/master-data/brands",
      },
      {
        text: "Units of Measure",
        icon: StraightenIcon,
        path: "/app/master-data/units-of-measure",
      },
      {
        text: "Suppliers",
        icon: BusinessIcon,
        path: "/app/master-data/suppliers",
      },
      {
        text: "Warehouses",
        icon: WarehouseIcon,
        path: "/app/master-data/warehouses",
      },
    ],
  },

  // -------------------------------------------------------------------
  // Inventory
  // -------------------------------------------------------------------

  {
    type: "section",
    text: "Inventory",
    icon: InventoryIcon,

    children: [
      {
        text: "Inventory",
        icon: InventoryIcon,
        path: "/app/inventory",
      },
      {
        text: "Stock Transfers",
        icon: SwapHorizIcon,
        path: "/app/inventory/stock-transfers",
      },
      {
        text: "Transactions",
        icon: ReceiptLongIcon,
        path: "/app/inventory/transactions",
      },
    ],
  },

  // -------------------------------------------------------------------
  // Procurement
  // -------------------------------------------------------------------

  {
    type: "section",
    text: "Procurement",
    icon: ShoppingCartIcon,

    children: [
      {
        text: "Purchase Orders",
        icon: ShoppingCartIcon,
        path: "/app/procurement/purchase-orders",
      },
      {
        text: "Goods Receipts",
        icon: ReceiptLongIcon,
        path: "/app/procurement/goods-receipts",
      },
    ],
  },

  // -------------------------------------------------------------------
  // Sales
  // -------------------------------------------------------------------

  {
    type: "section",
    text: "Sales",
    icon: LocalShippingIcon,

    children: [
      {
        text: "Sales Orders",
        icon: LocalShippingIcon,
        path: "/app/sales/sales-orders",
      },
    ],
  },

  // -------------------------------------------------------------------
  // Analytics
  // -------------------------------------------------------------------

  {
    type: "section",
    text: "Analytics",
    icon: AssessmentIcon,

    children: [
      {
        text: "Forecasting",
        icon: AssessmentIcon,
        path: "/app/analytics/forecasting",
      },
      {
        text: "Analytics",
        icon: AssessmentIcon,
        path: "/app/analytics",
      },
    ],
  },
];