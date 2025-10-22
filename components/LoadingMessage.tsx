import React from "react";
import { BotIcon, LoaderIcon } from "./Icons";

interface LoadingMessageProps {}

const LoadingMessage: React.FC<LoadingMessageProps> = () => {
  return (
    <div className="flex gap-3 justify-start message-enter">
      <div className="flex-shrink-0 w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
        <BotIcon />
      </div>
      <div className="max-w-2xl px-4 py-3 rounded-2xl bg-white bg-opacity-10 backdrop-blur-lg border border-purple-500 border-opacity-30">
        <LoaderIcon />
      </div>
    </div>
  );
};

export default LoadingMessage;
