"use client";

import { useState, useRef, useEffect, KeyboardEvent } from "react";
import { sendChatMessage } from "@/lib/api";
import { getToolFeedback } from "@/lib/tool-feedback";
import { useToast } from "@/components/ui/Toast";
import Spinner from "@/components/ui/Spinner";
import { cn } from "@/lib/cn";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatPopupProps {
  token: string;
  onMessageComplete?: () => void;
}

export default function ChatPopup({ token, onMessageComplete }: ChatPopupProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [toolFeedback, setToolFeedback] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Focus input when popup opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  async function handleSend() {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);

    const feedback = getToolFeedback(userMessage);
    setToolFeedback(feedback);
    setLoading(true);

    try {
      const data = await sendChatMessage(userMessage, conversationId, token);
      setConversationId(data.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
      onMessageComplete?.();
    } catch {
      setError("Unable to reach the assistant. Please try again.");
      toast("error", "Failed to send message");
    } finally {
      setLoading(false);
      setToolFeedback(null);
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <>
      {/* Floating Action Button - Todo AI Assistant */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          "fixed bottom-6 right-6 w-16 h-16 rounded-2xl shadow-xl flex items-center justify-center transition-all duration-300 z-50 group",
          isOpen
            ? "bg-gradient-to-br from-gray-500 to-gray-700 rotate-0 scale-95"
            : "bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 hover:scale-110 hover:shadow-2xl hover:shadow-purple-500/30"
        )}
      >
        {/* Pulse ring animation when closed */}
        {!isOpen && (
          <span className="absolute inset-0 rounded-2xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 animate-ping opacity-20" />
        )}

        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="transition-transform duration-300">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        ) : (
          <div className="relative flex items-center justify-center">
            {/* Todo checkmark with sparkle */}
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" className="transition-transform duration-300 group-hover:scale-110">
              {/* Checkbox background */}
              <rect x="3" y="3" width="18" height="18" rx="4" fill="white" fillOpacity="0.2" />
              {/* Checkmark */}
              <path d="M7 12.5l3 3 7-7" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              {/* AI sparkle */}
              <circle cx="18" cy="6" r="2" fill="#FFD700" className="animate-pulse" />
              <path d="M17 5l2 2M19 5l-2 2" stroke="#FFD700" strokeWidth="1" strokeLinecap="round" />
            </svg>
          </div>
        )}
      </button>

      {/* Chat Popup Window */}
      <div
        className={cn(
          "fixed bottom-24 right-6 w-[360px] sm:w-[400px] h-[500px] bg-[var(--surface-elevated)] rounded-2xl shadow-2xl border border-[var(--border-default)] flex flex-col overflow-hidden z-40 transition-all duration-300 origin-bottom-right",
          isOpen
            ? "opacity-100 scale-100 translate-y-0"
            : "opacity-0 scale-95 translate-y-4 pointer-events-none"
        )}
      >
        {/* Header */}
        <div className="flex-shrink-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 px-4 py-3 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="3" width="18" height="18" rx="4" fill="white" fillOpacity="0.3" />
              <path d="M7 12.5l3 3 7-7" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="18" cy="6" r="2" fill="#FFD700" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-white font-semibold text-sm">Todo AI Assistant</h3>
            <p className="text-white/70 text-xs">Ask me to manage your tasks</p>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-3 bg-[var(--surface-secondary)]">
          {messages.length === 0 && !loading && (
            <div className="text-center mt-8 animate-fade-in">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)] text-[var(--color-primary-600)] mb-3">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
                </svg>
              </div>
              <p className="text-sm font-medium text-[var(--text-primary)] mb-1">
                Hello! How can I help?
              </p>
              <p className="text-xs text-[var(--text-tertiary)] px-4">
                Try &quot;Add a task&quot; or &quot;Show my tasks&quot;
              </p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={cn(
                "flex animate-fade-in",
                msg.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={cn(
                  "max-w-[85%] px-3 py-2 text-sm rounded-2xl shadow-sm",
                  msg.role === "user"
                    ? "bg-[var(--color-primary-600)] text-white rounded-br-md"
                    : "bg-[var(--surface-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] rounded-bl-md"
                )}
              >
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))}

          {/* Loading indicator */}
          {loading && (
            <div className="flex justify-start animate-fade-in">
              <div className="bg-[var(--surface-elevated)] border border-[var(--border-default)] px-3 py-2 rounded-2xl rounded-bl-md shadow-sm">
                {toolFeedback ? (
                  <div className="flex items-center gap-2">
                    <Spinner size={14} className="text-[var(--color-primary-500)]" />
                    <p className="text-sm text-[var(--text-secondary)]">
                      {toolFeedback}
                    </p>
                  </div>
                ) : (
                  <div className="flex space-x-1.5 py-1">
                    <div className="w-2 h-2 bg-[var(--text-tertiary)] rounded-full animate-bounce" />
                    <div
                      className="w-2 h-2 bg-[var(--text-tertiary)] rounded-full animate-bounce"
                      style={{ animationDelay: "0.15s" }}
                    />
                    <div
                      className="w-2 h-2 bg-[var(--text-tertiary)] rounded-full animate-bounce"
                      style={{ animationDelay: "0.3s" }}
                    />
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="flex justify-center animate-scale-in">
              <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/30 text-[var(--color-error)] text-xs px-3 py-1.5 rounded-lg border border-red-200 dark:border-red-900">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {error}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="flex-shrink-0 border-t border-[var(--border-default)] bg-[var(--surface-elevated)] px-3 py-2">
          <div className="flex items-center gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a message..."
              disabled={loading}
              className="flex-1 px-3 py-2 border border-[var(--border-default)] bg-[var(--surface-bg)] text-[var(--text-primary)] rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent disabled:opacity-50 placeholder:text-[var(--text-tertiary)] transition-all"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="w-10 h-10 bg-[var(--color-primary-600)] text-white rounded-full flex items-center justify-center hover:bg-[var(--color-primary-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-95"
            >
              {loading ? (
                <Spinner size={16} />
              ) : (
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 z-30 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
