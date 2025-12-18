import { motion } from 'framer-motion';

interface MedicalRAGLogoProps {
  size?: number;
  className?: string;
  showText?: boolean;
}

const MedicalRAGLogo = ({ size = 40, className = '', showText = true }: MedicalRAGLogoProps) => {
  return (
    <motion.div
      className={`flex items-center gap-3 ${className}`}
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.3 }}
    >
      {/* Logo SVG - Medical Cross + Neural Network */}
      <motion.div
        whileHover={{ 
          filter: 'drop-shadow(0 0 12px rgba(59, 130, 246, 0.6))',
        }}
        transition={{ duration: 0.3 }}
      >
        <svg
          width={size}
          height={size}
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Gradient for medical cross */}
            <linearGradient id="crossGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
            
            {/* Gradient for neural nodes */}
            <radialGradient id="nodeGradient">
              <stop offset="0%" stopColor="#60a5fa" stopOpacity="1" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.8" />
            </radialGradient>

            {/* Glow filter */}
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          {/* Outer circle */}
          <motion.circle
            cx="50"
            cy="50"
            r="48"
            stroke="url(#crossGradient)"
            strokeWidth="2"
            fill="none"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 1.5, ease: "easeInOut" }}
          />

          {/* Medical Cross */}
          <motion.g
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Vertical bar */}
            <rect
              x="42"
              y="25"
              width="16"
              height="50"
              rx="3"
              fill="url(#crossGradient)"
              filter="url(#glow)"
            />
            {/* Horizontal bar */}
            <rect
              x="25"
              y="42"
              width="50"
              height="16"
              rx="3"
              fill="url(#crossGradient)"
              filter="url(#glow)"
            />
          </motion.g>

          {/* Neural Network Nodes */}
          {[
            { cx: 20, cy: 20, delay: 0.5 },
            { cx: 80, cy: 20, delay: 0.6 },
            { cx: 20, cy: 80, delay: 0.7 },
            { cx: 80, cy: 80, delay: 0.8 },
            { cx: 50, cy: 15, delay: 0.65 },
            { cx: 50, cy: 85, delay: 0.75 },
          ].map((node, i) => (
            <motion.circle
              key={i}
              cx={node.cx}
              cy={node.cy}
              r="4"
              fill="url(#nodeGradient)"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ 
                scale: [1, 1.3, 1], 
                opacity: [0.7, 1, 0.7] 
              }}
              transition={{
                scale: {
                  duration: 2,
                  repeat: Infinity,
                  delay: node.delay,
                },
                opacity: {
                  duration: 2,
                  repeat: Infinity,
                  delay: node.delay,
                }
              }}
            />
          ))}

          {/* Neural Network Connections */}
          <motion.g
            stroke="#3b82f6"
            strokeWidth="1"
            opacity="0.4"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 2, delay: 0.5 }}
          >
            <line x1="20" y1="20" x2="50" y2="50" />
            <line x1="80" y1="20" x2="50" y2="50" />
            <line x1="20" y1="80" x2="50" y2="50" />
            <line x1="80" y1="80" x2="50" y2="50" />
            <line x1="50" y1="15" x2="50" y2="50" />
            <line x1="50" y1="85" x2="50" y2="50" />
          </motion.g>

          {/* Central pulse */}
          <motion.circle
            cx="50"
            cy="50"
            r="6"
            fill="#3b82f6"
            initial={{ scale: 0 }}
            animate={{ 
              scale: [1, 1.5, 1],
              opacity: [0.8, 0.3, 0.8]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: 1,
            }}
          />
        </svg>
      </motion.div>

      {/* Logo Text */}
      {showText && (
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <h1 className="text-xl font-bold">
            <span className="bg-gradient-to-r from-primary via-blue-600 to-cyan-600 bg-clip-text text-transparent">
              MediRAG
            </span>
          </h1>
        </motion.div>
      )}
    </motion.div>
  );
};

export default MedicalRAGLogo;
