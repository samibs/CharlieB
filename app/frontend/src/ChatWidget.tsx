import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

const plugins = [
    {
        command: "/time",
        description: "Get the current time",
        handler: async () => `🕒 ${new Date().toLocaleTimeString()}`,
    },
    {
        command: "/date",
        description: "Get today's date",
        handler: async () => `📅 ${new Date().toLocaleDateString()}`,
    },
];

const HISTORY_KEY = "chat_history";
const loadHistory = () => {
    try {
        const stored = localStorage.getItem(HISTORY_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch {
        return [];
    }
};
const saveHistory = (messages: any[]) => {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(messages));
};

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState(loadHistory());
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const chatContainerRef = useRef<HTMLDivElement>(null);

    const toggleChat = () => setIsOpen(!isOpen);

    const sendMessage = async () => {
        const trimmedInput = input.trim();
        if (!trimmedInput) return;

        const newMessages = [...messages, { sender: "user", text: trimmedInput, time: new Date().toLocaleTimeString() }];
        setMessages(newMessages);
        saveHistory(newMessages);
        setInput("");
        setIsLoading(true);

        const plugin = plugins.find(p => trimmedInput.startsWith(p.command));
        if (plugin) {
            const pluginOutput = await plugin.handler(trimmedInput);
            const updated = [...newMessages, { sender: "bot", text: pluginOutput, time: new Date().toLocaleTimeString() }];
            setMessages(updated);
            saveHistory(updated);
            setIsLoading(false);
            return;
        }

        try {
            const health = await fetch("http://127.0.0.1:8000/health");
            if (!health.ok) throw new Error("Backend is down");
        } catch (error) {
            console.error("Health check failed:", error);
            const failMessage = [...newMessages, { sender: "bot", text: "⚠️ Backend is not available. Please try again later.", time: new Date().toLocaleTimeString() }];
            setMessages(failMessage);
            saveHistory(failMessage);
            setIsLoading(false);
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: trimmedInput }),
            });

            const contentType = response.headers.get("content-type");
            if (!response.ok || !contentType?.includes("application/json")) {
                throw new Error("Bad response from backend.");
            }

            const data = await response.json();
            const updated = [...newMessages, { sender: "bot", text: data.answer, time: new Date().toLocaleTimeString() }];
            setMessages(updated);
            saveHistory(updated);
        } catch (error) {
            console.error("Fetch error:", error);
            const errMessage = [...newMessages, { sender: "bot", text: "⚠️ Failed to reach backend. Please try again later.", time: new Date().toLocaleTimeString() }];
            setMessages(errMessage);
            saveHistory(errMessage);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className="fixed bottom-0 left-0 w-full flex justify-center items-end z-50">
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 50 }}
                        transition={{ duration: 0.3 }}
                        className="absolute bottom-12 w-96 bg-white bg-opacity-90 backdrop-blur-md shadow-xl rounded-2xl p-4 h-96 flex flex-col"
                    >
                        <div ref={chatContainerRef} className="flex-1 overflow-y-auto mb-2 pr-1">
                            {messages.map((msg, idx) => (
                                <div
                                    key={idx}
                                    className={`mb-2 text-sm ${msg.sender === "user" ? "text-right" : "text-left"}`}
                                >
                                    <span className="text-xs text-gray-400 block mb-1">{msg.time}</span>
                                    <span className={`inline-block px-3 py-2 rounded-xl max-w-xs break-words whitespace-pre-line ${msg.sender === "user" ? "bg-blue-100" : "bg-gray-100"}`}>
                                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                                    </span>
                                </div>
                            ))}
                            {isLoading && <div className="text-left text-sm text-gray-500 animate-pulse">🤖 typing...</div>}
                        </div>
                        <div className="flex">
                            <input
                                type="text"
                                className="flex-1 border rounded-l-xl p-2 text-sm focus:outline-none"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                                placeholder="Type your message..."
                                autoFocus
                            />
                            <button
                                className="bg-blue-500 text-white px-4 rounded-r-xl"
                                onClick={sendMessage}
                            >
                                Send
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
            <motion.button
                layout
                onClick={toggleChat}
                className="bg-blue-600 text-white px-6 py-2 rounded-t-xl shadow-md mb-1"
                aria-label="Toggle chat"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
            >
                💬 Chat
            </motion.button>
        </div>
    );
};

export default ChatWidget;
