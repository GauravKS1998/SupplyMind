import { Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import { motion } from "framer-motion";

import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

const NAVBAR_HEIGHT = 64;

const Layout = () => {
  return (
    <Box
      sx={{
        height: "100vh",
        overflow: "hidden",
      }}
    >
      <Navbar />

      <Box
        sx={{
          display: "flex",
          height: "100vh",
          pt: `${NAVBAR_HEIGHT}px`,
        }}
      >
        <Sidebar />

        <Box
          sx={{
            flexGrow: 1,
            overflowY: "auto",
            height: `calc(100vh - ${NAVBAR_HEIGHT}px)`,
            p: 3,
          }}
        >
          <motion.div
            initial={{
              opacity: 0,
              y: 20,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              duration: 0.4,
            }}
          >
            <Outlet />
          </motion.div>
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;
