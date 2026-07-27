import { Link } from "react-router";
import { motion } from "motion/react";
import { Combine, FileSpreadsheet, FileText, Minimize2, Scissors } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { HowItWorks } from "../components/home/HowItWorks";
import { WhyUs } from "../components/home/WhyUs";
import type { Route } from "./+types/home";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "AtlasPDF" },
    { name: "description", content: "Mikro PDF araç seti" },
  ];
}

const TOOLS = [
  {
    slug: "araclar/birlestir",
    title: "PDF Birleştir",
    description: "Birden fazla PDF dosyasını tek dosyada birleştirin.",
    icon: Combine,
  },
  {
    slug: "araclar/bol",
    title: "PDF Böl",
    description: "PDF dosyasını sayfa aralıklarına göre bölün.",
    icon: Scissors,
  },
  {
    slug: "araclar/sikistir",
    title: "PDF Sıkıştır",
    description: "PDF dosyanızın boyutunu küçültün.",
    icon: Minimize2,
  },
  {
    slug: "araclar/word-cevir",
    title: "PDF'i Word'e Çevir",
    description: "PDF'i düzenlenebilir bir Word dosyasına çevirin.",
    icon: FileText,
  },
  {
    slug: "araclar/pdf-excel",
    title: "PDF'i Excel'e Çevir",
    description: "PDF içindeki tabloları Excel dosyasına çıkarın.",
    icon: FileSpreadsheet,
  },
];

const gridVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0 },
};

const MotionLink = motion.create(Link);

export default function Home() {
  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-8 p-8">
      <div className="flex flex-col items-center gap-2 py-8 text-center">
        <h1 className="text-4xl font-bold">AtlasPDF</h1>
        <p className="text-muted-foreground">
          PDF dosyalarınızı birleştirin, bölün, sıkıştırın ya da başka formatlara çevirin.
        </p>
      </div>

      <motion.div
        className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
        variants={gridVariants}
        initial="hidden"
        animate="visible"
      >
        {TOOLS.map((tool) => (
          <MotionLink
            key={tool.slug}
            to={`/${tool.slug}`}
            variants={cardVariants}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
          >
            <Card className="h-full transition-colors hover:bg-accent hover:shadow-md">
              <CardHeader>
                <tool.icon className="size-6" />
                <CardTitle>{tool.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{tool.description}</p>
              </CardContent>
            </Card>
          </MotionLink>
        ))}
      </motion.div>

      <HowItWorks />
      <WhyUs />
    </main>
  );
}
