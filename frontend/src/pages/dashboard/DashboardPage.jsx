import {
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
} from "@mui/material";

import { useEffect, useState } from "react";

import { getDashboardSummary } from "../../api/services/dashboardService";

const DashboardPage = () => {
  const [summary, setSummary] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const data = await getDashboardSummary();

        setSummary(data);
      } catch (error) {
        console.error("Dashboard fetch failed", error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  const cards = summary
    ? [
        {
          title: "Products",
          value: summary.total_products,
        },
        {
          title: "Suppliers",
          value: summary.total_suppliers,
        },
        {
          title: "Warehouses",
          value: summary.total_warehouses,
        },
        {
          title: "Purchase Orders",
          value: summary.total_purchase_orders,
        },
        {
          title: "Sales Orders",
          value: summary.total_sales_orders,
        },
      ]
    : [];

  if (loading) return <CircularProgress />;

  return (
    <Grid container spacing={3}>
      {cards.map((card) => (
        <Grid item xs={12} sm={6} md={3} key={card.title}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6">{card.title}</Typography>

              <Typography variant="h4">{card.value}</Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default DashboardPage;
