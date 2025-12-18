import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, MessageSquare, X, Menu, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import axios from "axios";

interface ChatSession {
  session_id: string;
  title: string;
  created_at: string;
  message_count?: number;
}

interface ChatHistorySidebarProps {
  userId: number;
  currentSessionId: string;
  onSessionChange: (sessionId: string) => void;
  onNewChat: () => void;
  className?: string;
}

const ChatHistorySidebar = ({
  userId,
  currentSessionId,
  onSessionChange,
  onNewChat,
  className = "",
}: ChatHistorySidebarProps) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [loading, setLoading] = useState(false);

  // Fetch all chat sessions for the user
  useEffect(() => {
    fetchSessions();
  }, [userId]);

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/chat/sessions/${userId}`);
      setSessions(response.data);
    } catch (error) {
      console.error("❌ Error fetching sessions:", error);
    } finally {
      setLoading(false);
    }
  };

  const deleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await axios.delete(`http://127.0.0.1:5000/api/chat/sessions/${sessionId}`);
      setSessions(sessions.filter(s => s.session_id !== sessionId));
      if (currentSessionId === sessionId) {
        onNewChat();
      }
    } catch (error) {
      console.error("❌ Error deleting session:", error);
    }
  };

  const truncateTitle = (title: string, maxLength: number = 25) => {
    return title.length > maxLength ? title.substring(0, maxLength) + "..." : title;
  };

  return (
    <>
      {/* Mobile Toggle Button */}
      <motion.button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="fixed top-20 left-4 z-50 lg:hidden bg-white rounded-lg p-2 shadow-md border border-border"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
      >
        <Menu className="w-5 h-5 text-foreground" />
      </motion.button>

      {/* Overlay for mobile */}
      <AnimatePresence>
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsCollapsed(true)}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: isCollapsed ? -300 : 0 }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className={`fixed left-0 top-16 h-[calc(100vh-4rem)] w-72 bg-white/90 backdrop-blur-lg border-r border-border/50 shadow-lg z-50 lg:z-40 flex flex-col ${className}`}
      >
        {/* Header - New Chat Button */}
        <div className="p-4 border-b border-border/50">
          <motion.button
            onClick={() => {
              onNewChat();
              setIsCollapsed(true);
            }}
            className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground px-4 py-3 rounded-xl hover:bg-primary/90 transition-all shadow-md font-medium"
            whileHover={{ scale: 1.02, boxShadow: "0 6px 16px rgba(0, 0, 0, 0.2)" }}
            whileTap={{ scale: 0.98 }}
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </motion.button>
        </div>

        {/* Chat Sessions List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground text-sm">
              <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-50" />
              <p>No chat history yet</p>
              <p className="text-xs mt-1">Start a new conversation</p>
            </div>
          ) : (
            <AnimatePresence>
              {sessions.map((session, index) => (
                <motion.div
                  key={session.session_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => {
                    onSessionChange(session.session_id);
                    setIsCollapsed(true);
                  }}
                  className={`group relative flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
                    currentSessionId === session.session_id
                      ? "bg-primary text-primary-foreground shadow-md"
                      : "hover:bg-muted text-foreground"
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <MessageSquare className="w-4 h-4 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{truncateTitle(session.title)}</p>
                    <p className={`text-xs mt-0.5 ${
                      currentSessionId === session.session_id 
                        ? "text-primary-foreground/70" 
                        : "text-muted-foreground"
                    }`}>
                      {new Date(session.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  {/* Delete Button */}
                  <motion.button
                    onClick={(e) => deleteSession(session.session_id, e)}
                    className={`opacity-0 group-hover:opacity-100 p-1.5 rounded-lg transition-opacity ${
                      currentSessionId === session.session_id
                        ? "hover:bg-primary-foreground/20"
                        : "hover:bg-destructive/20"
                    }`}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </motion.button>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </div>

        {/* Footer - Collapse Toggle */}
        <div className="p-3 border-t border-border/50 hidden lg:block">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full hover:bg-muted rounded-xl"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </motion.aside>
    </>
  );
};

export default ChatHistorySidebar;
