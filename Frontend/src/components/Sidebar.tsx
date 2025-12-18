import { motion } from "framer-motion";
import { Home, History, MessageSquare, Settings, Menu, Plus, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import axios from "axios";

interface ChatSession {
  session_id: string;
  title: string;
  created_at: string;
  message_count?: number;
}

interface SidebarProps {
  onSectionChange?: (section: string) => void;
  activeSection?: string;
  userId?: number;
  currentSessionId?: string;
  onSessionChange?: (sessionId: string) => void;
  onNewChat?: () => void;
}

const Sidebar = ({ 
  onSectionChange, 
  activeSection = "chat",
  userId = 1,
  currentSessionId,
  onSessionChange,
  onNewChat
}: SidebarProps) => {
  const [isCollapsed, setIsCollapsed] = useState(true);
  const [isHovered, setIsHovered] = useState(false);
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);

  const menuItems = [
    { id: "home", label: "Home", icon: Home },
    { id: "chat", label: "Chat", icon: MessageSquare },
    { id: "history", label: "History", icon: History },
    { id: "settings", label: "Settings", icon: Settings },
  ];

  // Fetch chat sessions when in chat mode
  useEffect(() => {
    if (activeSection === "chat" && userId) {
      fetchSessions();
    }
  }, [activeSection, userId, currentSessionId]);

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
      if (currentSessionId === sessionId && onNewChat) {
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
        className="fixed top-20 left-4 z-40 lg:hidden bg-card rounded-lg p-2 shadow-md border border-border"
        whileHover={{ 
          scale: 1.1, 
          filter: "brightness(1.15)",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)"
        }}
        whileTap={{ scale: 0.95 }}
        transition={{ duration: 0.2, ease: "easeInOut" }}
      >
        <Menu className="w-5 h-5 text-foreground" />
      </motion.button>

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`
          fixed left-0 top-16 h-[calc(100vh-4rem)] 
          bg-card/80 backdrop-blur-lg border-r border-border 
          transition-all duration-300 ease-in-out z-40
          ${isCollapsed && !isHovered ? 'w-0 lg:w-16' : 'w-64'}
          overflow-hidden
        `}
      >
        <div className="flex flex-col h-full">
          {/* Main Navigation */}
          <div className="flex flex-col gap-1 p-4 pt-6">
            {menuItems.map((item, index) => {
              const Icon = item.icon;
              const isActive = activeSection === item.id;
              
              return (
                <motion.div
                  key={item.id}
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: index * 0.05, duration: 0.3 }}
                >
                  <Button
                    variant="ghost"
                    className={`
                      w-full justify-start gap-3 h-11 px-4
                      transition-all duration-200
                      ${isActive 
                        ? 'bg-primary text-white hover:shadow-md shadow-sm' 
                        : 'hover:bg-muted text-muted-foreground hover:text-foreground'
                      }
                      ${(isCollapsed && !isHovered) ? 'lg:justify-center lg:px-0' : ''}
                      rounded-lg
                    `}
                    onClick={() => onSectionChange?.(item.id)}
                  >
                    <Icon className={`h-5 w-5 flex-shrink-0 ${isActive ? 'text-white' : ''}`} />
                    {(!isCollapsed || isHovered) && (
                      <span className="font-medium text-sm">{item.label}</span>
                    )}
                  </Button>
                </motion.div>
              );
            })}
          </div>

          {/* Chat History Section (only show in chat mode) */}
          {activeSection === "chat" && (!isCollapsed || isHovered) && (
            <div className="flex-1 flex flex-col overflow-hidden px-4 pb-4">
              <div className="border-t border-border/50 pt-4 mb-3">
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 px-2">
                  Chat History
                </h3>
                {/* New Chat Button */}
                <motion.button
                  onClick={onNewChat}
                  className="w-full flex items-center justify-center gap-2 bg-gradient-to-br from-shade-3 to-shade-5 text-primary-foreground px-3 py-2.5 rounded-lg hover:shadow-hover transition-all shadow-md font-semibold text-sm mb-3"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Plus className="w-4 h-4" />
                  <span>New Chat</span>
                </motion.button>
              </div>

              {/* Sessions List */}
              <div className="flex-1 overflow-y-auto space-y-1.5 scrollbar-thin">
                {loading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                  </div>
                ) : sessions.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground text-xs">
                    <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>No chats yet</p>
                  </div>
                ) : (
                  sessions.map((session) => (
                    <motion.div
                      key={session.session_id}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      onClick={() => onSessionChange?.(session.session_id)}
                      className={`group relative flex items-center gap-2 p-2.5 rounded-lg cursor-pointer transition-all ${
                        currentSessionId === session.session_id
                          ? "bg-gradient-to-br from-shade-3 to-shade-5 text-primary-foreground shadow-sm"
                          : "hover:bg-shade-1 text-foreground"
                      }`}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <MessageSquare className="w-3.5 h-3.5 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium truncate">
                          {truncateTitle(session.title)}
                        </p>
                        <p className={`text-[10px] mt-0.5 ${
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
                        className={`opacity-0 group-hover:opacity-100 p-1 rounded transition-opacity ${
                          currentSessionId === session.session_id
                            ? "hover:bg-primary-foreground/20"
                            : "hover:bg-destructive/20"
                        }`}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        <Trash2 className="w-3 h-3" />
                      </motion.button>
                    </motion.div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Collapse Toggle for Desktop */}
        <div className="hidden lg:block absolute bottom-4 left-0 right-0 px-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full hover:bg-muted rounded-xl"
          >
            <Menu className="h-4 w-4" />
          </Button>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;
