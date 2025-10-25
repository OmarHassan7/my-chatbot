import React, { useState, useRef, useEffect } from "react";
import { BotIcon, SendIcon } from "./Icons";
import Message from "./Message";
import LoadingMessage from "./LoadingMessage";
import { sendMessage } from "@/utils/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const ChatbotInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hello! How can I help you today?" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiEndpoint, setApiEndpoint] = useState("/api/chat");

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input;
    setInput("");
    setLoading(true);

    try {
      const response = await sendMessage(currentInput, apiEndpoint);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.response,
        },
      ]);
    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${
            err instanceof Error ? err.message : "Unknown error"
          }. Make sure your backend is running at ${apiEndpoint}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="bg-black bg-opacity-30 backdrop-blur-lg border-b border-purple-500 border-opacity-30">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-purple-600 p-2 rounded-lg">
                <BotIcon />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">AI Chatbot</h1>
                <p className="text-sm text-purple-300">
                  Powered by Next.jsss & FastAPI
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={apiEndpoint}
                onChange={(e) => setApiEndpoint(e.target.value)}
                placeholder="API Endpoint"
                className="px-3 py-1 text-sm bg-white bg-opacity-10 backdrop-blur-lg border border-purple-500 border-opacity-30 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((msg, idx) => (
            <Message key={idx} message={msg} index={idx} />
          ))}
          {loading && <LoadingMessage />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-black bg-opacity-30 backdrop-blur-lg border-t border-purple-500 border-opacity-30 px-4 py-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={loading}
              className="flex-1 px-4 py-3 bg-white bg-opacity-10 backdrop-blur-lg border border-purple-500 border-opacity-30 rounded-xl text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50"
            />
            <button
              onClick={handleSubmit}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-xl font-medium transition-colors flex items-center gap-2"
            >
              <SendIcon />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotInterface;
