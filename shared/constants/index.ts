export const APP_NAME = "ProcureFlow AI";
export const APP_VERSION = "1.0.0";

export const PAGINATION = {
  DEFAULT_PAGE: 1,
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
};

export const ROLES = [
  "Admin",
  "Operations Manager",
  "Warehouse Manager",
  "Procurement Manager",
  "Finance Manager",
  "Viewer",
] as const;

export const PERMISSION_GROUPS = [
  "Users",
  "Inventory",
  "Products",
  "Categories",
  "Brands",
  "Warehouses",
  "Suppliers",
  "Procurement",
  "Finance",
  "Dashboard",
  "Analytics",
  "Reports",
  "AI",
  "Automation",
  "Audit",
  "Settings",
  "Simulation",
] as const;
