import { cn } from "@/lib/cn";
import type { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export default function Card({ className, hoverable, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "bg-[var(--surface-elevated)] rounded-[var(--radius-xl)] border border-[var(--border-default)] shadow-[var(--shadow-sm)]",
        hoverable && "transition-all duration-[var(--transition-fast)] hover:shadow-[var(--shadow-md)] hover:-translate-y-0.5",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
