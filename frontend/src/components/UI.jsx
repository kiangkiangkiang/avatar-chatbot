import { useRef, useState, useEffect } from "react";
import { useChat } from "../hooks/useChat";



export const UI = ({ hidden, ...props }) => {
  const input = useRef();
  const chatEndRef = useRef(null); // 用於滾動到底部
  const { chat, loading, cameraZoomed, setCameraZoomed } = useChat();
  const [chatHistory, setChatHistory] = useState([]);

  const sendMessage = async () => {
    const text = input.current.value;
    if (!loading && text.trim()) {
      setChatHistory((prev) => [...prev, { sender: "user", text }]);

      try {
        const response = await chat(text);
        const response_msg = response.messages
        const response_image = response.image_data // TODO: if exist

        if (response_msg && Array.isArray(response_msg)) {
          response_msg.forEach((msg) => {
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

        if (response_image) {
          setChatHistory((prev) => [
            ...prev,
            { sender: "bot", image: response_image },
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
    <div className="fixed top-0 left-0 right-0 bottom-0 z-10 flex justify-between p-4 flex-col pointer-events-none">

      <div className="self-start backdrop-blur-md bg-white bg-opacity-50 p-4 rounded-lg">
        <h1 className="font-black text-xl">Avatar Chatbot</h1>
      </div>
      <div className="w-full flex flex-col items-end justify-center gap-4">
        <button
          onClick={() => setCameraZoomed(!cameraZoomed)}
          className="pointer-events-auto bg-pink-500 hover:bg-pink-600 text-white p-4 rounded-md"
        >
          {cameraZoomed ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607zM13.5 10.5h-6"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607zM10.5 7.5v6m3-3h-6"
              />
            </svg>
          )}
        </button>
        <button
          onClick={() => {
            const body = document.querySelector("body");
            if (body.classList.contains("greenScreen")) {
              body.classList.remove("greenScreen");
            } else {
              body.classList.add("greenScreen");
            }
          }}
          className="pointer-events-auto bg-pink-500 hover:bg-pink-600 text-white p-4 rounded-md"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z"
            />
          </svg>
        </button>
      </div>
      <div className="flex flex-col items-start justify-center gap-4 w-full max-w-screen-md mx-auto pointer-events-auto">
        <div
          className="flex-1 w-full overflow-y-auto bg-gray-100 p-4 rounded-md bg-opacity-30 backdrop-blur-md"
          style={{ maxHeight: "250px" }}
          onWheel={(e) => e.stopPropagation()}
        >
          {chatHistory.map((entry, index) => (
            <div
              key={index}
              className={`mb-2 p-2 rounded-md max-w-[75%] ${entry.sender === "user"
                ? "bg-blue-100 bg-opacity-50 self-start"
                : "bg-green-100 bg-opacity-50 self-end"
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
                {entry.image && <img src={`data:image/png;base64,${entry.image}`} />}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

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
