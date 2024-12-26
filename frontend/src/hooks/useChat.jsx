import { createContext, useContext, useEffect, useState } from "react";

const backendUrl = import.meta.env.VITE_API_URL || "http://localhost:3000";

const ChatContext = createContext();

function generatePageId() {
  return Date.now().toString() + Math.random().toString(36).substring(2);
}

sessionStorage.setItem('pageId', generatePageId());
const pageId = sessionStorage.getItem('pageId');

window.onload = function () {
  fetch(`${backendUrl}/on_page_create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pageId: pageId })
  });
};

window.addEventListener('beforeunload', (event) => {
  fetch(`${backendUrl}/on_page_remove`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ pageId: pageId }),
    keepalive: true, // 確保瀏覽器允許在 unload 時執行請求
  });
});

export const ChatProvider = ({ children }) => {
  const chat = async (message) => {
    setLoading(true);
    const data = await fetch(`${backendUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message, pageId: pageId }),
    });
    const resp = (await data.json());
    console.log("resp == ", resp.image_data);
    setMessages((messages) => [...messages, ...resp.messages]);
    setLoading(false);
    return (resp);
  };
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState();
  const [loading, setLoading] = useState(false);
  const [cameraZoomed, setCameraZoomed] = useState(true);
  const onMessagePlayed = () => {
    setMessages((messages) => messages.slice(1));
  };

  useEffect(() => {
    if (messages.length > 0) {
      setMessage(messages[0]);
    } else {
      setMessage(null);
    }
  }, [messages]);

  return (
    <ChatContext.Provider
      value={{
        chat,
        message,
        onMessagePlayed,
        loading,
        cameraZoomed,
        setCameraZoomed,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};
