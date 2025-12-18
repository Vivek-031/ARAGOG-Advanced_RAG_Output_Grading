import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { motion } from "framer-motion";
import { Home, AlertCircle } from "lucide-react";
import "../customStyles.css";

const NotFound = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 bg-[#FDB87D]/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.15, 0.3, 0.15],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-[500px] h-[500px] bg-[#F6EFBD]/15 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.15, 0.3, 0.15],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Glass card */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="relative z-10 text-center bg-white/80 backdrop-blur-md p-12 rounded-2xl shadow-lg border border-[#d3e0e2] max-w-md"
      >
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5, type: "spring", bounce: 0.4 }}
          className="flex justify-center mb-6"
        >
          <div className="w-20 h-20 bg-gradient-to-br from-[#FDB87D] to-[#fca65a] rounded-2xl flex items-center justify-center shadow-lg">
            <AlertCircle className="w-10 h-10 text-white" />
          </div>
        </motion.div>

        <motion.h1
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-8xl font-bold text-[#3B3B3B]"
        >
          404
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-6 text-xl text-[#666666] font-medium"
        >
          Oops! The page you're looking for doesn't exist.
        </motion.p>

        <motion.button
          onClick={() => navigate("/")}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="button-submit mt-8 inline-flex items-center gap-2 px-8 py-4 text-lg"
          whileHover={{ 
            scale: 1.05,
            boxShadow: "0 12px 32px rgba(253, 184, 125, 0.35)"
          }}
          whileTap={{ scale: 0.95 }}
        >
          <Home className="w-5 h-5" />
          Go Home
        </motion.button>
      </motion.div>
    </div>
  );
};

export default NotFound;
