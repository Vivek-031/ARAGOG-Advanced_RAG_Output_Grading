import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { User, Mail, Lock, Sparkles } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import SuccessToast from "@/components/SuccessToast";

const Signup = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({ name: false, email: false, password: false });
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setFieldErrors({ name: false, email: false, password: false });

    // Validate fields
    const errors = { name: false, email: false, password: false };
    if (!name.trim()) errors.name = true;
    if (!email.trim()) errors.email = true;
    if (!password.trim()) errors.password = true;

    if (errors.name || errors.email || errors.password) {
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

    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        setShowSuccess(true);
        // Auto-login after successful signup
        const userData = {
          id: data.user?.id || 1,
          name: name,
          email: email,
          avatar: data.user?.avatar,
        };
        login(userData, data.token || 'mock-token');
        setTimeout(() => {
          navigate("/main");
        }, 1500);
      } else {
        setError(data.message || "Signup failed. Please try again.");
      }
    } catch (err) {
      console.error("Signup Error:", err);
      setError("Unable to connect to the server. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-bl from-[#ffe4e6] to-[#ccfbf1] relative flex items-center justify-center px-4 py-8 overflow-hidden">
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

      <SuccessToast 
        message="Account created successfully! Redirecting to login..."
        isVisible={showSuccess}
        onClose={() => setShowSuccess(false)}
      />

      <motion.div
        initial={{ opacity: 0, y: 30, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="w-full max-w-md relative z-10"
      >
        <motion.div 
          className="bg-white/80 backdrop-blur-md rounded-2xl p-10 shadow-lg border border-[#d3e0e2]"
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
                className="absolute inset-0 bg-gradient-to-br from-[#FDB87D] to-[#fca65a] rounded-2xl blur-xl opacity-30"
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
              <div className="relative w-16 h-16 bg-gradient-to-br from-[#FDB87D] to-[#fca65a] rounded-2xl flex items-center justify-center shadow-lg">
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
            <h1 className="text-4xl font-bold text-[#3B3B3B] mb-2">
              Create Account
            </h1>
            <p className="text-[#666666] text-base">Join <span className="font-semibold text-[#FDB87D]">Medical RAG</span> today</p>
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

            {/* Form Section */}
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Name Field */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
              >
                <Label htmlFor="name" className="text-foreground font-semibold text-sm mb-2 block">
                  Name
                </Label>
                <motion.div 
                  className="relative"
                  animate={fieldErrors.name ? { x: [0, -4, 4, -4, 4, 0] } : {}}
                  transition={{ duration: 0.3 }}
                >
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-[#FDB87D]" />
                  <Input
                    id="name"
                    type="text"
                    placeholder="Your full name"
                    value={name}
                    onChange={(e) => { setName(e.target.value); setFieldErrors(prev => ({ ...prev, name: false })); setError(""); }}
                    className={`pl-12 h-14 bg-white/60 backdrop-blur-sm rounded-xl border-2 transition-all font-medium ${
                      fieldErrors.name 
                        ? "border-red-400 shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:border-red-500 focus:ring-4 focus:ring-red-500/20" 
                        : "border-[#d3e0e2] hover:border-[#FDB87D] focus:border-[#FDB87D] focus:ring-4 focus:ring-[#FDB87D]/20"
                    }`}
                    required
                  />
                </motion.div>
              </motion.div>

              {/* Email Field */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
              >
                <Label htmlFor="email" className="text-foreground font-semibold text-sm mb-2 block">
                  Email Address
                </Label>
                <motion.div 
                  className="relative"
                  animate={fieldErrors.email ? { x: [0, -4, 4, -4, 4, 0] } : {}}
                  transition={{ duration: 0.3 }}
                >
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-[#FDB87D]" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => { setEmail(e.target.value); setFieldErrors(prev => ({ ...prev, email: false })); setError(""); }}
                    className={`pl-12 h-14 bg-white/60 backdrop-blur-sm rounded-xl border-2 transition-all font-medium ${
                      fieldErrors.email 
                        ? "border-red-400 shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:border-red-500 focus:ring-4 focus:ring-red-500/20" 
                        : "border-[#d3e0e2] hover:border-[#FDB87D] focus:border-[#FDB87D] focus:ring-4 focus:ring-[#FDB87D]/20"
                    }`}
                    required
                  />
                </motion.div>
              </motion.div>

              {/* Password Field */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Label htmlFor="password" className="text-foreground font-semibold text-sm mb-2 block">
                  Password
                </Label>
                <motion.div 
                  className="relative"
                  animate={fieldErrors.password ? { x: [0, -4, 4, -4, 4, 0] } : {}}
                  transition={{ duration: 0.3 }}
                >
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-[#FDB87D]" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); setFieldErrors(prev => ({ ...prev, password: false })); setError(""); }}
                    className={`pl-12 h-14 bg-white/60 backdrop-blur-sm rounded-xl border-2 transition-all font-medium ${
                      fieldErrors.password 
                        ? "border-red-400 shadow-[0_0_12px_rgba(239,68,68,0.3)] focus:border-red-500 focus:ring-4 focus:ring-red-500/20" 
                        : "border-[#d3e0e2] hover:border-[#FDB87D] focus:border-[#FDB87D] focus:ring-4 focus:ring-[#FDB87D]/20"
                    }`}
                    required
                  />
                </motion.div>
              </motion.div>

              {/* Submit Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <motion.button
                  type="submit"
                  disabled={loading}
                  className="button-submit w-full h-14 text-base font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                  whileHover={!loading ? { 
                    scale: 1.02,
                    boxShadow: "0 12px 32px rgba(253, 184, 125, 0.35)"
                  } : {}}
                  whileTap={!loading ? { scale: 0.98 } : {}}
                  transition={{ duration: 0.2, ease: "easeInOut" }}
                >
                  {loading ? "Creating Account..." : "Create Account"}
                </motion.button>
              </motion.div>
            </form>

          {/* Login Redirect */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
            className="mt-8 text-center text-sm text-[#666666]"
          >
            Already have an account?{" "}
            <span
              onClick={() => navigate("/login")}
              className="text-[#FDB87D] hover:text-[#fca65a] font-semibold transition-colors cursor-pointer"
            >
              Login
            </span>
          </motion.div>
          </motion.div>
        </motion.div>
    </div>
  );
};

export default Signup;
