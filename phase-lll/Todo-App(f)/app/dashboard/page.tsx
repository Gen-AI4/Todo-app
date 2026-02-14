"use client";

import { useState, useEffect, useCallback } from "react";
import ChatPopup from "@/components/ChatPopup";
import TasksPanel from "@/components/TasksPanel";
import Button from "@/components/ui/Button";

export default function DashboardPage() {
  const [token, setToken] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const storedToken = localStorage.getItem("auth_token");
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const handleChatComplete = useCallback(() => {
    setRefreshKey((prev) => prev + 1);
  }, []);

  if (!token) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-[var(--surface-secondary)]">
        <div className="text-center animate-fade-in">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-[var(--radius-2xl)] bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)] text-[var(--color-primary-600)] mb-6">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0110 0v4" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-2">
            Not authenticated
          </h2>
          <p className="text-[var(--text-secondary)] mb-6 max-w-xs mx-auto">
            Please log in to access your tasks and chat with the AI assistant.
          </p>
          <a href="/login">
            <Button size="lg">
              Go to Login
            </Button>
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-[var(--surface-secondary)]">
      {/* Header */}
      <header className="flex-shrink-0 bg-[var(--surface-elevated)] border-b border-[var(--border-default)] px-4 py-3 shadow-[var(--shadow-xs)]">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-[var(--radius-lg)] bg-[var(--color-primary-600)] flex items-center justify-center shadow-[var(--shadow-sm)]">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 11l3 3L22 4" />
                <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
              </svg>
            </div>
            <h1 className="text-lg font-semibold text-[var(--text-primary)]">
              Todo AI
            </h1>
          </div>
          <button
            onClick={() => {
              localStorage.removeItem("auth_token");
              window.location.href = "/login";
            }}
            className="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors duration-[var(--transition-fast)] px-3 py-1.5 rounded-[var(--radius-md)] hover:bg-[var(--surface-tertiary)]"
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Main content - Full width tasks panel */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          <TasksPanel token={token} refreshKey={refreshKey} />
        </div>
      </main>

      {/* Chat popup (FAB + floating window) */}
      <ChatPopup token={token} onMessageComplete={handleChatComplete} />
    </div>
  );
}
