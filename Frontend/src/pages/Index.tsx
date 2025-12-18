import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { ArrowRight, Brain, Shield, Zap, Sparkles } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Grading",
      description: "Evaluates medical responses for accuracy and structure.",
      gradient: "from-shade-3 to-shade-5",
    },
    {
      icon: Shield,
      title: "Trusted Knowledge",
      description: "Combines clinical reliability with retrieval-augmented reasoning.",
      gradient: "from-shade-2 to-shade-4",
    },
    {
      icon: Zap,
      title: "Next-Gen AI",
      description: "Delivering precision healthcare insights that you can trust.",
      gradient: "from-shade-3 to-shade-4",
    },
  ];

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-72 h-72 bg-shade-3/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-96 h-96 bg-shade-2/15 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center text-center px-6 py-16">
        {/* Floating Icon */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5, y: -50 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.8, type: "spring", bounce: 0.4 }}
          className="mb-8"
        >
          <div className="relative">
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-shade-3 to-shade-5 rounded-3xl blur-xl opacity-50"
              animate={{
                scale: [1, 1.1, 1],
                opacity: [0.5, 0.7, 0.5],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
            <div className="relative w-20 h-20 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
          </div>
        </motion.div>

        {/* Hero Title */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-shade-3 via-primary to-shade-4"
        >
          Medical RAG
        </motion.h1>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.7 }}
          className="mb-4"
        >
          <span className="inline-block px-6 py-2 bg-gradient-to-r from-shade-3/10 to-shade-4/10 border border-primary/20 rounded-full text-primary font-semibold text-sm backdrop-blur-sm">
            AI-Powered Medical Insights
          </span>
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.7 }}
          className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-12 leading-relaxed"
        >
          Revolutionizing medical AI with accurate, structured, and trusted answers —
          powered by RAG and precision grading intelligence.
        </motion.p>

        {/* CTA Button */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          <motion.button
            className="button-submit flex items-center justify-center gap-2 text-lg"
            onClick={() => navigate("/about")}
            whileHover={{ 
              scale: 1.05,
              boxShadow: "0 20px 40px rgba(161, 98, 247, 0.3)"
            }}
            whileTap={{ scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
          >
            Explore Now <ArrowRight className="w-5 h-5" />
          </motion.button>
        </motion.div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.7 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 max-w-6xl w-full"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 + index * 0.1, duration: 0.5 }}
                whileHover={{ 
                  y: -8,
                  transition: { duration: 0.3 }
                }}
                className="relative group"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-shade-3/20 to-shade-4/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                <div className="relative bg-card/80 backdrop-blur-xl rounded-2xl p-8 border border-border shadow-lg hover:shadow-2xl transition-all duration-300">
                  <div className={`w-14 h-14 bg-gradient-to-br ${feature.gradient} rounded-xl flex items-center justify-center mb-5 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </motion.div>
      </div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.6 }}
        className="absolute bottom-0 left-0 right-0 py-8 text-center"
      >
        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          <span>© 2025 Medical RAG</span>
          <span className="text-primary">•</span>
          <span>Powered by AI</span>
        </div>
      </motion.footer>
    </div>
  );
};

export default Index;
