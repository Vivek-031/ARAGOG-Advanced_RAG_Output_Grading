import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";           // Tailwind styles
import "./customStyles.css";    // 👈 Add this line (your Uiverse styles)

createRoot(document.getElementById("root")!).render(<App />);
