"use client";

import { useState, useRef, useEffect, KeyboardEvent } from "react";
import { sendChatMessage } from "@/lib/api";
import { getToolFeedback } from "@/lib/tool-feedback";
import { useToast } from "@/components/ui/Toast";
import Spinner from "@/components/ui/Spinner";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatInterfaceProps {
  token: string;
  onMessageComplete?: () => void;
}

export default function ChatInterface({ token, onMessageComplete }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [toolFeedback, setToolFeedback] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
    <div className="flex flex-col h-full max-w-3xl mx-auto">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-3 py-4 md:px-4 md:py-6 space-y-4">
        {messages.length === 0 && !loading && (
          <div className="text-center mt-20 animate-fade-in">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-[var(--radius-2xl)] bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)] text-[var(--color-primary-600)] mb-4">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
              </svg>
            </div>
            <p className="text-lg font-medium text-[var(--text-primary)] mb-2">
              Hello! I can help you manage your tasks.
            </p>
            <p className="text-sm text-[var(--text-tertiary)]">
              Try saying &quot;Add a task called Buy milk&quot; or &quot;What are
              my tasks?&quot;
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} animate-fade-in`}
          >
            <div className="max-w-[85%] sm:max-w-[75%]">
              <p
                className={`text-xs font-medium mb-1 text-[var(--text-tertiary)] ${
                  msg.role === "user" ? "text-right" : "text-left"
                }`}
              >
                {msg.role === "user" ? "You" : "Assistant"}
              </p>
              <div
                className={`px-4 py-2.5 shadow-[var(--shadow-xs)] ${
                  msg.role === "user"
                    ? "bg-[var(--color-primary-600)] text-white rounded-2xl rounded-br-md"
                    : "bg-[var(--surface-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] rounded-2xl rounded-bl-md"
                }`}
              >
                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {loading && (
          <div className="flex justify-start animate-fade-in">
            <div className="max-w-[85%] sm:max-w-[75%]">
              <p className="text-xs font-medium mb-1 text-[var(--text-tertiary)]">
                Assistant
              </p>
              <div className="bg-[var(--surface-elevated)] border border-[var(--border-default)] text-[var(--text-primary)] px-4 py-2.5 rounded-2xl rounded-bl-md shadow-[var(--shadow-xs)]">
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
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="flex justify-center animate-scale-in">
            <div className="flex items-center gap-2 bg-red-50 dark:bg-red-950/30 text-[var(--color-error)] text-sm px-4 py-2 rounded-[var(--radius-lg)] border border-red-200 dark:border-red-900">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
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
      <div className="flex-shrink-0 sticky bottom-0 border-t border-[var(--border-default)] bg-[var(--surface-bg)] px-3 py-3 md:px-4">
        <div className="flex items-center space-x-3 max-w-3xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
            disabled={loading}
            className="flex-1 px-4 py-2.5 border border-[var(--border-default)] bg-[var(--surface-bg)] text-[var(--text-primary)] rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-[var(--text-tertiary)] transition-all duration-[var(--transition-fast)]"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="min-h-[44px] min-w-[44px] px-5 py-2.5 bg-[var(--color-primary-600)] text-white text-sm font-medium rounded-full hover:bg-[var(--color-primary-700)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-[var(--transition-fast)] active:scale-95"
          >
            {loading ? <Spinner size={16} /> : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
