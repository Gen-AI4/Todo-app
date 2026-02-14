"use client";

import { useState } from "react";
import useSWR from "swr";
import { fetchTasks, toggleTaskComplete, deleteTask, createTask, updateTask, TaskItem } from "@/lib/api";
import { cn } from "@/lib/cn";
import Card from "@/components/ui/Card";
import { useToast } from "@/components/ui/Toast";

interface TasksPanelProps {
  token: string;
  refreshKey: number;
}

type ViewMode = "list" | "grid";

function timeAgo(dateStr: string): string {
  // Ensure the date is treated as UTC by appending 'Z' if not present
  const utcDateStr = dateStr.endsWith('Z') ? dateStr : dateStr + 'Z';
  const seconds = Math.floor(
    (Date.now() - new Date(utcDateStr).getTime()) / 1000
  );
  if (seconds < 0) return "just now"; // Handle slight clock differences
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function TasksPanel({ token, refreshKey }: TasksPanelProps) {
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [loadingTaskId, setLoadingTaskId] = useState<string | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingTask, setEditingTask] = useState<TaskItem | null>(null);
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();

  const { data: tasks, error, isLoading, mutate } = useSWR(
    [`tasks`, token, refreshKey],
    () => fetchTasks(token)
  );

  const handleToggleComplete = async (task: TaskItem) => {
    setLoadingTaskId(task.id);
    try {
      await toggleTaskComplete(task.id, task.is_completed, token);
      await mutate();
      toast("success", task.is_completed ? "Task marked incomplete" : "Task completed!");
    } catch {
      toast("error", "Failed to update task");
    } finally {
      setLoadingTaskId(null);
    }
  };

  const handleDelete = async (task: TaskItem) => {
    if (!confirm(`Delete "${task.title}"?`)) return;
    setLoadingTaskId(task.id);
    try {
      await deleteTask(task.id, token);
      await mutate();
      toast("success", "Task deleted");
    } catch {
      toast("error", "Failed to delete task");
    } finally {
      setLoadingTaskId(null);
    }
  };

  const handleAddTask = async () => {
    if (!newTitle.trim()) return;
    setIsSubmitting(true);
    try {
      await createTask(newTitle.trim(), newDescription.trim() || null, token);
      await mutate();
      toast("success", "Task created!");
      setNewTitle("");
      setNewDescription("");
      setShowAddModal(false);
    } catch {
      toast("error", "Failed to create task");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEditTask = async () => {
    if (!editingTask || !newTitle.trim()) return;
    setIsSubmitting(true);
    try {
      await updateTask(editingTask.id, newTitle.trim(), newDescription.trim() || null, token);
      await mutate();
      toast("success", "Task updated!");
      setEditingTask(null);
      setNewTitle("");
      setNewDescription("");
    } catch {
      toast("error", "Failed to update task");
    } finally {
      setIsSubmitting(false);
    }
  };

  const openEditModal = (task: TaskItem) => {
    setEditingTask(task);
    setNewTitle(task.title);
    setNewDescription(task.description || "");
  };

  const closeModal = () => {
    setShowAddModal(false);
    setEditingTask(null);
    setNewTitle("");
    setNewDescription("");
  };

  // Loading skeleton
  if (isLoading) {
    return (
      <div className="p-4 space-y-3">
        <div className="flex items-center justify-between mb-4">
          <div className="h-4 w-16 animate-shimmer rounded" />
          <div className="h-6 w-14 animate-shimmer rounded" />
        </div>
        {[1, 2, 3].map((i) => (
          <div key={i} className="p-3 rounded-[var(--radius-lg)] border border-[var(--border-subtle)]">
            <div className="flex items-start gap-3">
              <div className="w-5 h-5 animate-shimmer rounded-full mt-0.5 flex-shrink-0" />
              <div className="flex-1 space-y-2">
                <div className="h-4 animate-shimmer rounded w-3/4" />
                <div className="h-3 animate-shimmer rounded w-1/2" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="p-4 flex flex-col items-center justify-center h-full">
        <div className="w-12 h-12 rounded-full bg-red-100 dark:bg-red-950/30 flex items-center justify-center mb-3">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-error)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
        </div>
        <p className="text-sm text-[var(--color-error)] mb-3 font-medium">
          Failed to load tasks
        </p>
        <button
          onClick={() => mutate()}
          className="text-sm text-[var(--color-primary-600)] dark:text-[var(--color-primary-400)] hover:underline font-medium"
        >
          Try again
        </button>
      </div>
    );
  }

  const taskList = tasks || [];
  const sorted = [...taskList].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );
  const completedCount = taskList.filter((t) => t.is_completed).length;

  return (
    <div className="p-4">
      {/* Header with view toggle and add button */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <h2 className="text-sm font-semibold text-[var(--text-secondary)] uppercase tracking-wide">
            Tasks
          </h2>
          {taskList.length > 0 && (
            <span className="inline-flex items-center px-2 py-0.5 rounded-[var(--radius-full)] text-xs font-medium bg-[var(--color-primary-100)] dark:bg-[var(--color-primary-900)] text-[var(--color-primary-700)] dark:text-[var(--color-primary-300)]">
              {completedCount}/{taskList.length}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {/* Add button */}
          <button
            onClick={() => setShowAddModal(true)}
            className="p-1.5 rounded-[var(--radius-md)] bg-[var(--color-primary-600)] text-white hover:bg-[var(--color-primary-700)] transition-colors"
            title="Add task"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
          </button>
          {/* View toggle */}
          <div className="flex items-center bg-[var(--surface-tertiary)] rounded-[var(--radius-md)] p-0.5">
            <button
              onClick={() => setViewMode("list")}
              className={cn(
                "p-1.5 rounded-[var(--radius-sm)] transition-all duration-[var(--transition-fast)]",
                viewMode === "list"
                  ? "bg-[var(--surface-elevated)] text-[var(--text-primary)] shadow-[var(--shadow-xs)]"
                  : "text-[var(--text-tertiary)] hover:text-[var(--text-secondary)]"
              )}
              title="List view"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="8" y1="6" x2="21" y2="6" />
                <line x1="8" y1="12" x2="21" y2="12" />
                <line x1="8" y1="18" x2="21" y2="18" />
                <line x1="3" y1="6" x2="3.01" y2="6" />
                <line x1="3" y1="12" x2="3.01" y2="12" />
                <line x1="3" y1="18" x2="3.01" y2="18" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode("grid")}
              className={cn(
                "p-1.5 rounded-[var(--radius-sm)] transition-all duration-[var(--transition-fast)]",
                viewMode === "grid"
                  ? "bg-[var(--surface-elevated)] text-[var(--text-primary)] shadow-[var(--shadow-xs)]"
                  : "text-[var(--text-tertiary)] hover:text-[var(--text-secondary)]"
              )}
              title="Grid view"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="3" width="7" height="7" />
                <rect x="14" y="3" width="7" height="7" />
                <rect x="14" y="14" width="7" height="7" />
                <rect x="3" y="14" width="7" height="7" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Progress bar */}
      {taskList.length > 0 && (
        <div className="mb-4">
          <div className="h-1.5 bg-[var(--surface-tertiary)] rounded-[var(--radius-full)] overflow-hidden">
            <div
              className="h-full bg-[var(--color-primary-500)] rounded-[var(--radius-full)] transition-all duration-500 ease-out"
              style={{ width: `${taskList.length > 0 ? (completedCount / taskList.length) * 100 : 0}%` }}
            />
          </div>
        </div>
      )}

      {/* Empty state */}
      {taskList.length === 0 && (
        <div className="flex flex-col items-center justify-center min-h-[300px]">
          <div className="w-16 h-16 rounded-[var(--radius-2xl)] bg-[var(--surface-tertiary)] flex items-center justify-center mb-4">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--text-tertiary)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11" />
            </svg>
          </div>
          <p className="text-sm font-medium text-[var(--text-secondary)] mb-1">
            No tasks yet
          </p>
          <p className="text-xs text-[var(--text-tertiary)] text-center max-w-[200px] mb-4">
            Click the + button to create your first task
          </p>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 bg-[var(--color-primary-600)] text-white text-sm font-medium rounded-[var(--radius-lg)] hover:bg-[var(--color-primary-700)] transition-colors"
          >
            Add Task
          </button>
        </div>
      )}

      {/* Task list/grid */}
      {taskList.length > 0 && (
        <div className={cn(
          viewMode === "grid" ? "grid grid-cols-2 gap-2" : "space-y-2"
        )}>
          {sorted.map((task: TaskItem, index: number) => (
            <Card
              key={task.id}
              hoverable
              className={cn(
                "p-3 animate-fade-in group",
                task.is_completed && "opacity-60",
                loadingTaskId === task.id && "opacity-50 pointer-events-none"
              )}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <div className={cn(
                "flex gap-3",
                viewMode === "grid" ? "flex-col" : "items-start"
              )}>
                {/* Checkbox - clickable */}
                <button
                  onClick={() => handleToggleComplete(task)}
                  className="flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] rounded-full"
                  title={task.is_completed ? "Mark incomplete" : "Mark complete"}
                >
                  {task.is_completed ? (
                    <div className="w-5 h-5 rounded-full bg-[var(--color-success)] flex items-center justify-center hover:bg-green-600 transition-colors">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    </div>
                  ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-[var(--border-default)] transition-colors duration-[var(--transition-fast)] hover:border-[var(--color-primary-500)] hover:bg-[var(--color-primary-50)] dark:hover:bg-[var(--color-primary-900)]" />
                  )}
                </button>

                {/* Task content */}
                <div className="flex-1 min-w-0">
                  <p
                    className={cn(
                      "text-sm leading-snug",
                      task.is_completed
                        ? "line-through text-[var(--text-tertiary)]"
                        : "text-[var(--text-primary)] font-medium"
                    )}
                  >
                    {task.title}
                  </p>
                  {task.description && (
                    <p className="text-xs text-[var(--text-tertiary)] truncate mt-1">
                      {task.description}
                    </p>
                  )}
                  <p className="text-[10px] text-[var(--text-tertiary)] mt-1.5 tracking-wide uppercase">
                    {timeAgo(task.created_at)}
                  </p>
                </div>

                {/* Action buttons */}
                <div className={cn(
                  "flex items-center gap-1 flex-shrink-0",
                  viewMode === "list" ? "opacity-0 group-hover:opacity-100" : ""
                )}>
                  {/* Edit button */}
                  <button
                    onClick={() => openEditModal(task)}
                    className="p-1 rounded text-[var(--text-tertiary)] hover:text-[var(--color-primary-600)] hover:bg-[var(--color-primary-50)] dark:hover:bg-[var(--color-primary-900)] transition-all"
                    title="Edit task"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                      <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                    </svg>
                  </button>
                  {/* Delete button */}
                  <button
                    onClick={() => handleDelete(task)}
                    className="p-1 rounded text-[var(--text-tertiary)] hover:text-[var(--color-error)] hover:bg-red-50 dark:hover:bg-red-950/30 transition-all"
                    title="Delete task"
                  >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6" />
                      <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                    </svg>
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Add/Edit Modal */}
      {(showAddModal || editingTask) && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" onClick={closeModal}>
          <div
            className="bg-[var(--surface-elevated)] rounded-2xl shadow-2xl w-full max-w-md animate-scale-in"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-[var(--border-default)]">
              <h3 className="text-lg font-semibold text-[var(--text-primary)]">
                {editingTask ? "Edit Task" : "Add New Task"}
              </h3>
              <button
                onClick={closeModal}
                className="p-1 rounded-full text-[var(--text-tertiary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-tertiary)] transition-colors"
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">
                  Title <span className="text-[var(--color-error)]">*</span>
                </label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="Enter task title"
                  className="w-full px-3 py-2.5 border border-[var(--border-default)] bg-[var(--surface-bg)] text-[var(--text-primary)] rounded-[var(--radius-lg)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent placeholder:text-[var(--text-tertiary)]"
                  autoFocus
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1.5">
                  Description
                </label>
                <textarea
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Enter task description (optional)"
                  rows={3}
                  className="w-full px-3 py-2.5 border border-[var(--border-default)] bg-[var(--surface-bg)] text-[var(--text-primary)] rounded-[var(--radius-lg)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary-500)] focus:border-transparent placeholder:text-[var(--text-tertiary)] resize-none"
                />
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-end gap-2 px-4 py-3 border-t border-[var(--border-default)]">
              <button
                onClick={closeModal}
                className="px-4 py-2 text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-tertiary)] rounded-[var(--radius-lg)] transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={editingTask ? handleEditTask : handleAddTask}
                disabled={!newTitle.trim() || isSubmitting}
                className="px-4 py-2 text-sm font-medium bg-[var(--color-primary-600)] text-white rounded-[var(--radius-lg)] hover:bg-[var(--color-primary-700)] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? "Saving..." : editingTask ? "Update" : "Add Task"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
