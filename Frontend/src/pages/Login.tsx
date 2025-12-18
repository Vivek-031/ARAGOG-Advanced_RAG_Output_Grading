import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, Sparkles } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import "@/customStyles.css";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({ email: false, password: false });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({ email: false, password: false });

    // Validate fields
    const errors = { email: false, password: false };
    if (!email.trim()) errors.email = true;
    if (!password.trim()) errors.password = true;

    if (errors.email || errors.password) {
      setFieldErrors(errors);
      setError("Please fill all required fields.");
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setFieldErrors({ ...errors, email: true });
      setError("Please enter a valid email address.");
      return;
    }

    try {
      const res = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        // Store user and token in AuthContext
        const userData = {
          id: data.user?.id || 1,
          name: data.user?.name || email.split('@')[0],
          email: email,
          avatar: data.user?.avatar,
        };
        login(userData, data.token || 'mock-token');
        navigate("/main");
      } else {
        setError(data.message || "Login failed. Please check your credentials.");
      }
    } catch (err) {
      console.error(err);
      setError("Unable to connect to the server. Please try again later.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-bl from-bg to-shade-2 relative flex items-center justify-center px-4 py-8 overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 bg-shade-3/10 rounded-full blur-3xl"
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
          className="absolute bottom-20 right-10 w-[500px] h-[500px] bg-shade-2/15 rounded-full blur-3xl"
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

      <motion.div
        initial={{ opacity: 0, y: 30, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="w-full max-w-md relative z-10"
      >
        <motion.div 
          className="bg-card/80 backdrop-blur-md rounded-2xl p-10 shadow-lg border border-border"
          animate={error ? { x: [0, -8, 8, -8, 8, 0] } : {}}
          transition={{ duration: 0.4, ease: "easeInOut" }}
        >
          {/* Logo/Icon */}
          <motion.div
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, type: "spring", bounce: 0.4 }}
            className="flex justify-center mb-6"
          >
            <div className="relative">
              <motion.div
                className="absolute inset-0 bg-primary rounded-2xl blur-xl opacity-30"
                animate={{
                  scale: [1, 1.1, 1],
                  opacity: [0.3, 0.5, 0.3],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              />
              <div className="relative w-16 h-16 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="text-center mb-8"
          >
            <h1 className="text-4xl font-bold text-foreground mb-2">
              Welcome Back
            </h1>
            <p className="text-muted-foreground text-base">
              Sign in to continue to <span className="font-semibold text-primary">Medical RAG</span>
            </p>
          </motion.div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="mb-6 p-4 rounded-2xl bg-red-50 border border-red-200"
            >
              <p className="text-red-600 text-sm flex items-center gap-2 font-medium">
                <span>⚠️</span>
                <span>{error}</span>
              </p>
            </motion.div>
          )}

            {/* Uiverse style form */}
            <form onSubmit={handleSubmit} className="form space-y-6">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3, duration: 0.5 }}
              >
                <Label htmlFor="email" className="text-foreground font-semibold text-sm mb-2 block">
                  Email Address
                </Label>
                <motion.div 
                  className="relative"
                  animate={fieldErrors.email ? { x: [0, -4, 4, -4, 4, 0] } : {}}
                  transition={{ duration: 0.3 }}
                >
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-primary" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => { setEmail(e.target.value); setFieldErrors(prev => ({ ...prev, email: false })); setError(""); }}
                    className={`pl-12 h-14 bg-white/60 backdrop-blur-sm rounded-xl border-2 transition-all font-medium ${
                      fieldErrors.email 
                        ? "border-red-400 shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:border-red-500 focus:ring-4 focus:ring-red-500/20" 
                        : "border-border hover:border-primary focus:border-primary focus:ring-1 focus:ring-primary"
                    }`}
                    required
                  />
                </motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4, duration: 0.5 }}
              >
                <Label htmlFor="password" className="text-foreground font-semibold text-sm mb-2 block">
                  Password
                </Label>
                <motion.div 
                  className="relative"
                  animate={fieldErrors.password ? { x: [0, -4, 4, -4, 4, 0] } : {}}
                  transition={{ duration: 0.3 }}
                >
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-primary" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); setFieldErrors(prev => ({ ...prev, password: false })); setError(""); }}
                    className={`pl-12 h-14 bg-white/60 backdrop-blur-sm rounded-xl border-2 transition-all font-medium ${
                      fieldErrors.password 
                        ? "border-red-400 shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:border-red-500 focus:ring-4 focus:ring-red-500/20" 
                        : "border-border hover:border-primary focus:border-primary focus:ring-1 focus:ring-primary"
                    }`}
                    required
                  />
                </motion.div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5, duration: 0.5 }}
                className="flex items-center justify-end text-sm"
              >
                <a
                  href="#"
                  className="text-primary hover:text-primary-hover font-semibold transition-colors duration-200"
                >
                  Forgot Password?
                </a>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.5 }}
              >
                <motion.button 
                  type="submit" 
                  className="button-submit w-full h-14 text-base font-semibold"
                  whileHover={{ 
                    scale: 1.05
                  }}
                  whileTap={{ scale: 0.98 }}
                  transition={{ duration: 0.2, ease: "easeInOut" }}
                >
                  Sign In
                </motion.button>
              </motion.div>
            </form>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7, duration: 0.5 }}
            className="mt-8 text-center text-sm text-muted-foreground"
          >
            Don't have an account?{" "}
            <span
              onClick={() => navigate("/signup")}
              className="text-primary hover:text-primary-hover font-semibold transition-colors duration-200 cursor-pointer"
            >
              Sign Up
            </span>
          </motion.div>
          </motion.div>
        </motion.div>
    </div>
  );
};

export default Login;
