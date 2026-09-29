/**
 * MaritimeCampaignCard — Hero card for a maritime campaign.
 * Features: route pill, discount badge, status badge, highlights, CTA.
 */

import { ArrowRight, Calendar, MapPin, Tag } from "lucide-react";
import { cn } from "@/lib/utils";
import { ctaVariants } from "@/components/site/Cta";
import type { MaritimeCampaign } from "@/data/campaigns";
import { statusMeta } from "@/data/campaigns";

function formatDate(iso: string) {
  return new Intl.DateTimeFormat("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(iso));
}

export function MaritimeCampaignCard({
  campaign,
}: {
  campaign: MaritimeCampaign;
}) {
  const meta = statusMeta[campaign.status];

  return (
    <article className="group relative flex flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-card transition-all duration-300 hover:-translate-y-1.5 hover:shadow-lift">
      {/* Top accent bar — colour by status */}
      <div
        className={cn(
          "h-1 w-full",
          campaign.status === "active"   && "bg-emerald-500",
          campaign.status === "limited"  && "bg-amber-500",
          campaign.status === "upcoming" && "bg-primary",
          campaign.status === "expired"  && "bg-gray-300",
        )}
      />

      <div className="flex flex-1 flex-col p-6">
        {/* Header row: status badge + discount */}
        <div className="flex items-start justify-between gap-3">
          {/* Status badge */}
          <span
            className={cn(
              "inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold",
              meta.color,
            )}
          >
            <span className={cn("h-1.5 w-1.5 rounded-full", meta.dot)} />
            {meta.label}
          </span>

          {/* Discount pill */}
          <span className="flex items-center gap-1 rounded-full bg-primary/10 px-3 py-1 text-sm font-bold text-primary">
            <Tag className="h-3.5 w-3.5" />
            {campaign.discount}
          </span>
        </div>

        {/* Title */}
        <h3 className="mt-4 font-display text-xl font-extrabold leading-snug text-navy">
          {campaign.title}
        </h3>
        <p className="mt-0.5 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          {campaign.subtitle}
        </p>

        {/* Route pill */}
        <div className="mt-4 flex items-center gap-2 rounded-xl bg-surface px-4 py-2.5 text-sm">
          <MapPin className="h-4 w-4 shrink-0 text-primary" />
          <span className="font-medium text-foreground">
            {campaign.route.from}
          </span>
          <ArrowRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
          <span className="font-medium text-foreground">
            {campaign.route.to}
          </span>
        </div>

        {/* Description */}
        <p className="mt-4 flex-1 text-sm leading-relaxed text-muted-foreground">
          {campaign.description}
        </p>

        {/* Highlights */}
        <ul className="mt-5 space-y-1.5">
          {campaign.highlights.map((h) => (
            <li key={h} className="flex items-center gap-2 text-sm text-foreground/80">
              <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
              {h}
            </li>
          ))}
        </ul>

        {/* Footer: validity + CTA */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
          <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <Calendar className="h-3.5 w-3.5" />
            Valide jusqu'au {formatDate(campaign.validUntil)}
          </span>
          <button
            type="button"
            disabled={campaign.status === "expired"}
            className={cn(
              ctaVariants({ variant: "primary", size: "md" }),
              "text-xs px-5 h-10",
              campaign.status === "expired" && "opacity-50 cursor-not-allowed",
            )}
          >
            {campaign.status === "upcoming"
              ? "Me notifier"
              : "Profiter de l'offre"}
            <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
          </button>
        </div>
      </div>
    </article>
  );
}
