import React from "react";
import { BotIcon, UserIcon } from "./Icons";

interface MessageProps {
  message: {
    role: "user" | "assistant";
    content: string;
  };
  index: number;
}

const Message: React.FC<MessageProps> = ({ message, index }) => {
  return (
    <div
      className={`flex gap-3 message-enter ${
        message.role === "user" ? "justify-end" : "justify-start"
      }`}
    >
      {message.role === "assistant" && (
        <div className="flex-shrink-0 w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
          <BotIcon />
        </div>
      )}
      <div
        className={`max-w-2xl px-4 py-3 rounded-2xl ${
          message.role === "user"
            ? "bg-purple-600 text-white"
            : "bg-white bg-opacity-10 backdrop-blur-lg text-white border border-purple-500 border-opacity-30"
        }`}
      >
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
      {message.role === "user" && (
        <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
          <UserIcon />
        </div>
      )}
    </div>
  );
};

export default Message;
