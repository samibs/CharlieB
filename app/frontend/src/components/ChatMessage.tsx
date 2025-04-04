// frontend/src/components/ChatMessage.tsx
import React from "react";
import ReactMarkdown from "react-markdown";
import BotAvatar from "./BotAvatar";

interface ChatMessageProps {
    sender: "user" | "bot";
    text: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ sender, text }) => {
    return (
        <div className={`flex items-start mb-2 ${sender === "user" ? "justify-end" : "justify-start"}`}>
            {sender === "bot" && <BotAvatar />}
            <div
                className={`max-w-xs p-3 rounded-2xl whitespace-pre-wrap text-sm shadow-md ${
                    sender === "user" ? "bg-blue-100 text-right" : "bg-gray-100"
                }`}
            >
                <ReactMarkdown>{text}</ReactMarkdown>
            </div>
        </div>
    );
};

export default ChatMessage;