import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Sparkles, Mic, MicOff } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatBubble from "../components/ChatBubble";
import TypingIndicator from "../components/TypingIndicator";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

interface Message {
  text: string;
  isUser: boolean;
  timestamp?: string;
}

const Main: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [activeSection, setActiveSection] = useState("chat");
  const [isListening, setIsListening] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string>(
    `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  );
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const recognitionRef = useRef<any>(null);
  const { toast } = useToast();

  const userId = user?.id || 1;

  // Redirect if not logged in
  useEffect(() => {
    if (!isAuthenticated) navigate("/login");
  }, [isAuthenticated, navigate]);

  // Load chat session messages
  const loadSessionMessages = async (sessionId: string) => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/api/chat/sessions/${sessionId}/messages`);
      const formatted = res.data.map((msg: any) => ({
        text: msg.message,
        isUser: msg.role === "user",
        timestamp: msg.created_at,
      }));
      setMessages(formatted);
    } catch (err) {
      console.error("❌ Error loading session messages:", err);
      setMessages([]);
    }
  };

  // Create new session
  const createNewSessionId = async (): Promise<string | null> => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/chat/new", {
        user_id: userId,
      });
      return response.data.session_id;
    } catch (error) {
      console.error("❌ Error creating new session:", error);
      return null;
    }
  };

  // Load or create session on mount
  useEffect(() => {
    const initializeChat = async () => {
      try {
        const lastSessionId = localStorage.getItem(`lastActiveSession_${userId}`);
        if (lastSessionId) {
          setCurrentSessionId(lastSessionId);
          await loadSessionMessages(lastSessionId);
        } else {
          const newSession = await createNewSessionId();
          if (newSession) setCurrentSessionId(newSession);
        }
      } catch (error) {
        console.error("❌ Error initializing chat:", error);
      }
    };
    initializeChat();
  }, []);

  useEffect(() => {
    if (currentSessionId) {
      localStorage.setItem(`lastActiveSession_${userId}`, currentSessionId);
    }
  }, [currentSessionId, userId]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // ✅ FIXED HANDLE SEND
  const handleSend = async () => {
    if (!input.trim()) return;
    const messageText = input;

    const userMessage: Message = {
      text: messageText,
      isUser: true,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      await axios.post("http://127.0.0.1:5000/api/chat/save", {
        user_id: userId,
        session_id: currentSessionId,
        role: "user",
        message: messageText,
      });

      const response = await axios.post("http://127.0.0.1:5000/api/rag/query", {
        query: messageText,
        user_id: userId,
        session_id: currentSessionId,
      });

      console.log("🧠 RAG Backend Response:", response.data); // 👈 Optional debug

      // ✅ FIXED: use `answer`, not `response`
      const aiResponse =
        response.data.answer ||
        "AI could not process your query. Please try again.";

      await axios.post("http://127.0.0.1:5000/api/chat/save", {
        user_id: userId,
        session_id: currentSessionId,
        role: "assistant",
        message: aiResponse,
      });

      setMessages((prev) => [
        ...prev,
        { text: aiResponse, isUser: false, timestamp: new Date().toISOString() },
      ]);
    } catch (error) {
      console.error("❌ Error communicating with backend:", error);
      setMessages((prev) => [
        ...prev,
        {
          text: "⚠️ Server error! Please check if backend is running.",
          isUser: false,
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  // New Chat
  const handleNewChat = async () => {
    const newSessionId = await createNewSessionId();
    if (newSessionId) {
      setCurrentSessionId(newSessionId);
      setMessages([]);
      setInput("");
      toast({
        title: "New chat started",
        description: "You can now start a fresh conversation.",
      });
    }
  };

  const handleSessionChange = (sessionId: string) => {
    setCurrentSessionId(sessionId);
    setInput("");
  };

  const clearChat = () => {
    setMessages([]);
    toast({
      title: "Chat cleared",
      description: "All messages have been removed from view.",
    });
  };

  // Voice input
  useEffect(() => {
    if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
      const SpeechRecognition =
        (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = "en-US";

      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsListening(false);
        toast({ title: "Voice input captured", description: transcript });
      };

      recognitionRef.current.onerror = (event: any) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
        toast({
          title: "Voice input failed",
          description: "Please try again or check microphone permissions.",
          variant: "destructive",
        });
      };

      recognitionRef.current.onend = () => setIsListening(false);
    }
  }, [toast]);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      toast({
        title: "Voice input not supported",
        description: "Your browser doesn't support speech recognition.",
        variant: "destructive",
      });
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
      toast({
        title: "Listening...",
        description: "Speak your medical query now.",
      });
    }
  };

  const handleSectionChange = (section: string) => {
    setActiveSection(section);
    toast({
      title: `Switched to ${section.charAt(0).toUpperCase() + section.slice(1)}`,
      description:
        section === "chat"
          ? "Continue your conversation"
          : `${section.charAt(0).toUpperCase() + section.slice(1)} section opened.`,
    });
  };

  return (
    <div className="flex flex-col min-h-screen relative bg-gradient-to-bl from-bg to-white">
      {/* Background Animation */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-96 h-96 bg-shade-3/10 rounded-full blur-3xl"
          animate={{ scale: [1, 1.2, 1], opacity: [0.15, 0.3, 0.15] }}
          transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-[500px] h-[500px] bg-shade-2/15 rounded-full blur-3xl"
          animate={{ scale: [1.2, 1, 1.2], opacity: [0.15, 0.3, 0.15] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      <Navbar />

      <div className="flex flex-1 pt-16 overflow-hidden">
        <Sidebar
          onSectionChange={handleSectionChange}
          activeSection={activeSection}
          userId={userId}
          currentSessionId={currentSessionId}
          onSessionChange={handleSessionChange}
          onNewChat={handleNewChat}
        />

        <main className="flex-1 flex flex-col lg:ml-64 transition-all duration-300">
          {activeSection === "chat" && (
            <div className="flex-1 overflow-hidden flex flex-col">
              {/* Chat UI */}
              <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto py-8">
                  {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
                      <div className="w-16 h-16 mb-6 rounded-2xl bg-primary flex items-center justify-center shadow-lg">
                        <Sparkles className="w-8 h-8 text-white" />
                      </div>
                      <h2 className="text-3xl font-bold text-foreground mb-3">
                        Welcome to MediRAG
                      </h2>
                      <p className="text-muted-foreground text-lg max-w-md">
                        Ask any medical question and get reliable, AI-powered answers.
                      </p>
                    </div>
                  ) : (
                    <div>
                      {messages.map((msg, index) => (
                        <ChatBubble
                          key={index}
                          text={msg.text}
                          isUser={msg.isUser}
                          timestamp={msg.timestamp}
                        />
                      ))}
                      {isTyping && <TypingIndicator />}
                      <div ref={chatEndRef} />
                    </div>
                  )}
                </div>
              </div>

              {/* Input Area */}
              <div className="border-t border-border bg-card/80 backdrop-blur-md">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                  <div className="relative flex items-end gap-2 bg-card rounded-2xl shadow-lg border border-border p-2 focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                    <motion.button
                      onClick={toggleVoiceInput}
                      className={`p-3 rounded-xl ${
                        isListening
                          ? "bg-destructive text-destructive-foreground"
                          : "bg-shade-1 text-foreground"
                      }`}
                      title={isListening ? "Stop recording" : "Voice input"}
                    >
                      {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                    </motion.button>

                    <input
                      type="text"
                      className="flex-1 px-4 py-3 bg-transparent focus:outline-none text-foreground placeholder:text-muted-foreground text-[15px]"
                      placeholder="Ask your medical query..."
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault();
                          handleSend();
                        }
                      }}
                    />

                    <motion.button
                      onClick={handleSend}
                      disabled={!input.trim() || isTyping}
                      className="flex items-center justify-center gap-2 bg-primary text-white px-5 py-3 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <Send className="w-4 h-4" />
                      <span className="hidden sm:inline font-medium">Send</span>
                    </motion.button>
                  </div>
                  <p className="text-xs text-muted-foreground text-center mt-3">
                    ⚕️ MediRAG can make mistakes. Consider checking important information.
                  </p>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Main;
