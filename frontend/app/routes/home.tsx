import type { Route } from "./+types/home";
import { HealthCheck } from "../components/shared/HealthCheck";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "AtlasPDF" },
    { name: "description", content: "Mikro PDF araç seti" },
  ];
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 p-8">
      <h1 className="text-4xl font-bold">AtlasPDF</h1>
      <HealthCheck />
    </main>
  );
}
