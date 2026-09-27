import { cn } from "@/lib/utils";

export function Logo({ light = false, className }: { light?: boolean; className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-3", className)}>
      <span className="grid h-10 w-10 place-items-center rounded-xl bg-primary text-primary-foreground shadow-card">
        <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" aria-hidden="true">
          <path
            d="M3 16h18M5 16l1.6-5.2A2 2 0 0 1 8.5 9.4h7a2 2 0 0 1 1.9 1.4L19 16M3 19.5c1.2 0 1.2-1 2.4-1s1.2 1 2.4 1 1.2-1 2.4-1 1.2 1 2.4 1 1.2-1 2.4-1 1.2 1 2.4 1M12 9.4V4.5"
            stroke="currentColor"
            strokeWidth="1.7"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </span>
      <span className="leading-none">
        <span
          className={cn(
            "block font-display text-xl font-extrabold tracking-tight",
            light ? "text-navy-foreground" : "text-navy",
          )}
        >
          ESC
        </span>
        <span
          className={cn(
            "mt-1 block text-[10px] font-semibold uppercase tracking-[0.18em]",
            light ? "text-navy-foreground/60" : "text-muted-foreground",
          )}
        >
          Express Shipping
        </span>
      </span>
    </span>
  );
}
