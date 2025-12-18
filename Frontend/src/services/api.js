const API_URL = "http://localhost:5000/api"; // backend URL

// Fetch full chat history
export const getChatHistory = async (userId) => {
  const res = await fetch(`${API_URL}/chat/${userId}`);
  return res.json();
};

// Save chat messages
export const saveChatMessage = async (data) => {
  await fetch(`${API_URL}/chat/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
};

// Send message to backend RAG endpoint
export const sendToRAG = async (query) => {
  const res = await fetch(`${API_URL}/rag/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: query }),
  });
  return res.json();
};
