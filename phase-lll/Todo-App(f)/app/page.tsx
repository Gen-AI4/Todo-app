import { redirect } from "next/navigation";

export default function Home() {
  // For now, redirect to dashboard.
  // Auth check can be added later to redirect to /login if unauthenticated.
  redirect("/dashboard");
}
