/**
 * LanguageSwitcher — Toggle between French and English.
 */

import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { Globe } from "lucide-react";

export function LanguageSwitcher() {
  const { locale, setLocale } = useI18n();

  return (
    <div className="flex items-center gap-1 rounded-full border border-border bg-background p-1">
      <Globe className="ml-2 h-4 w-4 text-muted-foreground" />
      <button
        type="button"
        onClick={() => setLocale("fr")}
        className={cn(
          "rounded-full px-3 py-1 text-xs font-semibold transition-colors",
          locale === "fr"
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:text-foreground"
        )}
        aria-label="Français"
      >
        FR
      </button>
      <button
        type="button"
        onClick={() => setLocale("en")}
        className={cn(
          "rounded-full px-3 py-1 text-xs font-semibold transition-colors",
          locale === "en"
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:text-foreground"
        )}
        aria-label="English"
      >
        EN
      </button>
    </div>
  );
}
