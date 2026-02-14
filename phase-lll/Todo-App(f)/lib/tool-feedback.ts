export function getToolFeedback(message: string): string | null {
  const lower = message.toLowerCase();

  const patterns: [RegExp, string][] = [
    [/\b(add|create|new)\b.*\btask\b/, "Adding task..."],
    [/\b(list|show|what)\b.*\btask/, "Fetching tasks..."],
    [/\b(complete|finish|done|mark)\b/, "Completing task..."],
    [/\b(delete|remove)\b/, "Deleting task..."],
    [/\b(update|change|rename|edit)\b/, "Updating task..."],
  ];

  for (const [pattern, feedback] of patterns) {
    if (pattern.test(lower)) return feedback;
  }

  return null;
}
