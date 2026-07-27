import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Upload, Wrench, Download } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const STEPS = [
  {
    title: "1. Yükle",
    description: "PDF dosyanızı sürükleyip bırakın veya seçin.",
    icon: Upload,
  },
  {
    title: "2. Aracı Seç",
    description: "Birleştir, böl, sıkıştır ya da Word/Excel'e çevir.",
    icon: Wrench,
  },
  {
    title: "3. İndir",
    description: "İşlenmiş dosyanızı hemen indirin.",
    icon: Download,
  },
];

export function HowItWorks() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const items = gsap.utils.toArray<HTMLElement>("[data-how-it-works-item]");

      gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
        gsap.from(items, {
          opacity: 0,
          y: 24,
          stagger: 0.15,
          duration: 0.5,
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top 80%",
          },
        });
      });
    },
    { scope: containerRef }
  );

  return (
    <section ref={containerRef} className="flex flex-col gap-6 py-8">
      <h2 className="text-center text-2xl font-bold">Nasıl Çalışır</h2>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {STEPS.map((step) => (
          <div
            key={step.title}
            data-how-it-works-item
            className="flex flex-col items-center gap-2 rounded-xl border p-6 text-center"
          >
            <step.icon className="size-6" />
            <h3 className="font-semibold">{step.title}</h3>
            <p className="text-sm text-muted-foreground">{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
