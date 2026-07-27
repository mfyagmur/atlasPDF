import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Lock, ShieldCheck, Sparkles, Zap } from "lucide-react";

gsap.registerPlugin(ScrollTrigger);

const REASONS = [
  {
    title: "Hızlı",
    description: "Dosyalarınız saniyeler içinde işlenir.",
    icon: Zap,
  },
  {
    title: "Anonim",
    description: "Kayıt olmadan, hesap açmadan kullanın.",
    icon: Lock,
  },
  {
    title: "Güvenli",
    description: "Dosyalarınız işlem sonrası otomatik olarak silinir.",
    icon: ShieldCheck,
  },
  {
    title: "Ücretsiz",
    description: "Tüm araçlar herkese açık ve ücretsizdir.",
    icon: Sparkles,
  },
];

export function WhyUs() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const items = gsap.utils.toArray<HTMLElement>("[data-why-us-item]");

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
      <h2 className="text-center text-2xl font-bold">Neden AtlasPDF</h2>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {REASONS.map((reason) => (
          <div
            key={reason.title}
            data-why-us-item
            className="flex flex-col items-center gap-2 rounded-xl border p-6 text-center"
          >
            <reason.icon className="size-6" />
            <h3 className="font-semibold">{reason.title}</h3>
            <p className="text-sm text-muted-foreground">{reason.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
