import { motion } from "framer-motion";
import { User, Bot } from "lucide-react";
import { useState } from "react";

interface ChatBubbleProps {
  text: string;
  isUser: boolean;
  imageUrl?: string;
  timestamp?: string;
}

const ChatBubble = ({ text, isUser, imageUrl, timestamp }: ChatBubbleProps) => {
  const [showTimestamp, setShowTimestamp] = useState(false);

  const formatTimestamp = (ts?: string) => {
    if (!ts) return "";
    const date = new Date(ts);
    return date.toLocaleString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex gap-4 mb-6 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.2, delay: 0.1 }}
        className={`
          flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center
          ${isUser 
            ? "bg-gradient-to-br from-primary to-secondary shadow-md" 
            : "bg-muted border border-border"
          }
        `}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-muted-foreground" />
        )}
      </motion.div>

      {/* Message Bubble */}
      <motion.div
        initial={{ opacity: 0, x: isUser ? 20 : -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
        onMouseEnter={() => setShowTimestamp(true)}
        onMouseLeave={() => setShowTimestamp(false)}
        className={`
          relative max-w-[75%] sm:max-w-[70%] px-4 py-3 rounded-2xl
          ${isUser
            ? "bg-primary text-primary-foreground shadow-md"
            : "bg-muted text-foreground border border-border"
          }
        `}
      >
        {/* Image */}
        {imageUrl && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
            className="mb-2"
          >
            <img
              src={imageUrl}
              alt="Uploaded content"
              className="rounded-lg max-w-full h-auto max-h-64 object-cover border-2 border-white/20"
            />
          </motion.div>
        )}
        
        {/* Text */}
        {text && (
          <p className="text-[15px] leading-relaxed whitespace-pre-wrap break-words">
            {text}
          </p>
        )}
        
        {/* Timestamp (appears on hover) */}
        {timestamp && showTimestamp && (
          <motion.div
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 5 }}
            className={`absolute -bottom-6 text-xs ${
              isUser ? "right-0" : "left-0"
            } ${isUser ? "text-muted-foreground" : "text-muted-foreground"}`}
          >
            {formatTimestamp(timestamp)}
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  );
};

export default ChatBubble;
