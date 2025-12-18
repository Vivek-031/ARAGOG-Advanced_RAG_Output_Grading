import { motion, AnimatePresence } from "framer-motion";
import { X, CheckCircle } from "lucide-react";

interface SuccessToastProps {
  message: string;
  isVisible: boolean;
  onClose: () => void;
}

const SuccessToast = ({ message, isVisible, onClose }: SuccessToastProps) => {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -50, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -50, scale: 0.95 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
          className="fixed top-20 left-1/2 -translate-x-1/2 z-[100] max-w-md w-full mx-4"
        >
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="bg-white/90 backdrop-blur-lg rounded-2xl shadow-lg border border-primary/30 p-4"
          >
            <div className="flex items-start gap-3">
              {/* Icon */}
              <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-primary" />
              </div>

              {/* Message */}
              <div className="flex-1 pt-1">
                <h3 className="font-semibold text-foreground text-sm mb-1">Success</h3>
                <p className="text-primary text-sm leading-relaxed">{message}</p>
              </div>

              {/* Close Button */}
              <motion.button
                onClick={onClose}
                whileHover={{ scale: 1.1, rotate: 90 }}
                whileTap={{ scale: 0.9 }}
                className="flex-shrink-0 w-8 h-8 rounded-lg hover:bg-primary/10 flex items-center justify-center transition-colors"
              >
                <X className="w-4 h-4 text-muted-foreground" />
              </motion.button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default SuccessToast;
