/**
 * AssociatedCampaignCard — Compact card for a related/associated campaign.
 * Features: category label, badge pill, description, status chip, CTA.
 */

import { ArrowRight, Calendar } from "lucide-react";
import { cn } from "@/lib/utils";
import { ctaVariants } from "@/components/site/Cta";
import type { AssociatedCampaign } from "@/lib/api";

const statusMeta: Record<string, { label: string; color: string; dot: string }> = {
  "active":   { label: "Active",          color: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-500" },
  "limited":  { label: "Offre limitée",   color: "bg-amber-100 text-amber-700",   dot: "bg-amber-500" },
  "upcoming": { label: "À venir",         color: "bg-blue-100 text-blue:700",     dot: "bg-blue-500" },
  "expired":  { label: "Expirée",         color: "bg-gray-100 text-gray-500",     dot: "bg-gray-400" },
};

function formatDate(iso: string) {
  return new Intl.DateTimeFormat("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(iso));
}

export function AssociatedCampaignCard({
  campaign,
}: {
  campaign: AssociatedCampaign;
}) {
  const meta = statusMeta[campaign.status] ?? statusMeta["active"]!;

  return (
    <article className="group flex flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-card transition-all duration-300 hover:-translate-y-1 hover:shadow-lift">
      {/* Left-side colour stripe rendered as a top border gradient */}
      <div
        className={cn(
          "h-0.5 w-full",
          campaign.status === "active"   && "bg-gradient-to-r from-emerald-400 to-emerald-600",
          campaign.status === "limited"  && "bg-gradient-to-r from-amber-400  to-amber-600",
          campaign.status === "upcoming" && "bg-gradient-to-r from-primary    to-blue-700",
          campaign.status === "expired"  && "bg-border",
        )}
      />

      <div className="flex flex-1 flex-col p-5">
        {/* Top row: category + badge */}
        <div className="flex items-center justify-between gap-2">
          <span className="eyebrow text-[0.65rem]">{campaign.category}</span>
          <span className="rounded-full bg-navy/10 px-2.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-wide text-navy dark:bg-navy-foreground/10 dark:text-navy-foreground">
            {campaign.badge}
          </span>
        </div>

        {/* Title */}
        <h4 className="mt-3 font-display text-base font-bold leading-snug text-navy">
          {campaign.title}
        </h4>

        {/* Description */}
        <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
          {campaign.description}
        </p>

        {/* Footer */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-border pt-3">
          <div className="flex flex-col gap-1">
            <span
              className={cn(
                "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[0.65rem] font-semibold",
                meta.color,
              )}
            >
              <span className={cn("h-1.5 w-1.5 rounded-full", meta.dot)} />
              {meta.label}
            </span>
            <span className="flex items-center gap-1 text-[0.65rem] text-muted-foreground">
              <Calendar className="h-3 w-3" />
              {formatDate(campaign.valid_until)}
            </span>
          </div>

          <button
            type="button"
            disabled={campaign.status === "expired"}
            className={cn(
              ctaVariants({ variant: "soft", size: "md" }),
              "h-9 px-4 text-xs",
              campaign.status === "expired" && "opacity-40 cursor-not-allowed",
            )}
          >
            Voir les détails
            <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
          </button>
        </div>
      </div>
    </article>
  );
}
