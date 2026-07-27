import { Link, Outlet } from "react-router";
import { MotionConfig } from "motion/react";
import { Button } from "../ui/button";

export default function AppLayout() {
  return (
    <MotionConfig reducedMotion="user">
      <div className="flex min-h-screen flex-col">
        <header className="border-b">
          <div className="mx-auto flex max-w-5xl items-center justify-between p-4">
            <Link to="/" className="text-lg font-bold">
              AtlasPDF
            </Link>
            <Button type="button" variant="outline" size="sm" disabled>
              Giriş Yap
            </Button>
          </div>
        </header>

        <div className="flex-1">
          <Outlet />
        </div>

        <footer className="border-t">
          <div className="mx-auto flex max-w-5xl flex-col items-center gap-1 p-4 text-center text-sm text-muted-foreground">
            <p>© 2026 AtlasPDF</p>
            <p>Mikro PDF araç seti</p>
          </div>
        </footer>
      </div>
    </MotionConfig>
  );
}
