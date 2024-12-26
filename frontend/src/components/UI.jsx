import { useRef, useState, useEffect } from "react";
import { useChat } from "../hooks/useChat";

export const UI = ({ hidden, ...props }) => {
  const input = useRef();
  const chatEndRef = useRef(null); // 用於滾動到底部
  const { chat, loading } = useChat();
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    const text = input.current.value;
    if (!loading && text.trim()) {
      setChatHistory((prev) => [...prev, { sender: "user", text }]);

      try {
        const response = await chat(text);

        if (response && Array.isArray(response)) {
          response.forEach((msg) => {
            setChatHistory((prev) => [
              ...prev,
              { sender: "bot", text: msg?.text || "Error: Missing text." },
            ]);
          });
        } else {
          setChatHistory((prev) => [
            ...prev,
            { sender: "bot", text: "Error: Invalid response format." },
          ]);
        }
      } catch (error) {
        setChatHistory((prev) => [
          ...prev,
          { sender: "bot", text: "Error: Unable to fetch response." },
        ]);
      }

      input.current.value = "";
    }
  };

  // 滾輪自動滾到底部
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatHistory]);

  if (hidden) {
    return null;
  }

  return (
    <div className="fixed top-0 left-0 right-0 bottom-0 z-10 flex justify-between p-4 flex-col">
      <div className="self-start backdrop-blur-md bg-white bg-opacity-50 p-4 rounded-lg">
        <h1 className="font-black text-xl">My AI Agent</h1>
      </div>
      <div className="flex flex-col items-start justify-center gap-4 w-full max-w-screen-md mx-auto">
        <div
          className="flex-1 w-full overflow-y-auto bg-gray-100 p-4 rounded-md bg-opacity-50 backdrop-blur-md"
          style={{ maxHeight: "250px" }}
          onWheel={(e) => e.stopPropagation()} // 阻止滾動事件傳播到背景
        >
          {chatHistory.map((entry, index) => (
            <div
              key={index}
              className={`mb-2 p-2 rounded-md max-w-[75%] ${entry.sender === "user"
                ? "bg-blue-100 self-start"
                : "bg-green-100 self-end"
                }`}
              style={{
                alignSelf: entry.sender === "user" ? "flex-start" : "flex-end",
                marginLeft: entry.sender === "user" ? "0" : "auto",
                marginRight: entry.sender === "user" ? "auto" : "0",
              }}
            >
              <div className="inline-block text-black">
                <strong>{entry.sender === "user" ? "You: " : "Bot: "}</strong>
                {entry.text}
              </div>
            </div>
          ))}
          {/* 滾輪自動滾動到這裡 */}
          <div ref={chatEndRef} />
        </div>

        {/* 输入框和发送按钮 */}
        <div className="flex items-center gap-2 pointer-events-auto w-full">
          <input
            className="w-full placeholder:text-gray-800 placeholder:italic p-4 rounded-md bg-opacity-50 bg-white backdrop-blur-md"
            placeholder="Type a message..."
            ref={input}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />
          <button
            disabled={loading}
            onClick={sendMessage}
            className={`bg-pink-500 hover:bg-pink-600 text-white p-4 px-10 font-semibold uppercase rounded-md ${loading ? "cursor-not-allowed opacity-30" : ""
              }`}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};
