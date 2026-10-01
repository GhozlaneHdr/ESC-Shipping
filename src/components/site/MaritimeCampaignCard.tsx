import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { ArrowRight, Calendar, Info, MapPin, Tag } from "lucide-react";
import { cn } from "@/lib/utils";
import { ctaVariants } from "@/components/site/Cta";
import { CampaignDetailModal } from "@/components/site/CampaignDetailModal";
import { useI18n } from "@/lib/i18n";
import type { MaritimeCampaign } from "@/lib/api";

const statusMeta: Record<string, { label: string; color: string; dot: string }> = {
  "active":   { label: "Active",          color: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-500" },
  "limited":  { label: "Offre limitée",   color: "bg-amber-100 text-amber-700",   dot: "bg-amber-500" },
  "upcoming": { label: "À venir",         color: "bg-blue-100 text-blue-700",     dot: "bg-blue-500" },
  "expired":  { label: "Expirée",         color: "bg-gray-100 text-gray-500",     dot: "bg-gray-400" },
};

function formatDate(iso: string) {
  try {
    return new Intl.DateTimeFormat("fr-FR", {
      day: "numeric",
      month: "long",
      year: "numeric",
    }).format(new Date(iso));
  } catch {
    return iso;
  }
}

export function MaritimeCampaignCard({
  campaign,
}: {
  campaign: MaritimeCampaign;
}) {
  const { t, locale } = useI18n();
  const [modalOpen, setModalOpen] = useState(false);
  const meta = statusMeta[campaign.status] ?? statusMeta["active"]!;

  const formatDate = (iso: string) => {
    try {
      return new Intl.DateTimeFormat(locale === "en" ? "en-US" : "fr-FR", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }).format(new Date(iso));
    } catch {
      return iso;
    }
  };

  const title = (locale === "en" && campaign.title_en) ? campaign.title_en : campaign.title;
  const subtitle = (locale === "en" && campaign.subtitle_en) ? campaign.subtitle_en : campaign.subtitle;
  const description = (locale === "en" && campaign.description_en) ? campaign.description_en : campaign.description;
  const rawHighlights = (locale === "en" && campaign.highlights_en) 
    ? campaign.highlights_en 
    : (campaign.highlights_list || campaign.highlights || []);
  const highlightsList: string[] = Array.isArray(rawHighlights) ? rawHighlights : [rawHighlights];
  const validUntil = campaign.valid_until || campaign.validUntil || "";

  return (
    <>
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
              {t(`campaign.status.${campaign.status}`) || meta.label}
            </span>

            {/* Discount pill */}
            <span className="flex items-center gap-1 rounded-full bg-primary/10 px-3 py-1 text-sm font-bold text-primary">
              <Tag className="h-3.5 w-3.5" />
              {campaign.discount}
            </span>
          </div>

          {/* Title */}
          <h3 className="mt-4 font-display text-xl font-extrabold leading-snug text-navy">
            {title}
          </h3>
          <p className="mt-0.5 text-xs font-semibold uppercase tracking-widest text-muted-foreground">
            {subtitle}
          </p>

          {/* Route pill */}
          <div className="mt-4 flex items-center gap-2 rounded-xl bg-surface px-4 py-2.5 text-sm">
            <MapPin className="h-4 w-4 shrink-0 text-primary" />
            <span className="font-medium text-foreground">
              {campaign.route_from || campaign.route?.from}
            </span>
            <ArrowRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <span className="font-medium text-foreground">
              {campaign.route_to || campaign.route?.to}
            </span>
          </div>

          {/* Description */}
          <p className="mt-4 flex-1 text-sm leading-relaxed text-muted-foreground">
            {description}
          </p>

          {/* Highlights */}
          <ul className="mt-5 space-y-1.5">
            {highlightsList.map((h: string) => (
              <li key={h} className="flex items-center gap-2 text-sm text-foreground/80">
                <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                {h}
              </li>
            ))}
          </ul>

          {/* Footer: validity + action buttons */}
          <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
            <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <Calendar className="h-3.5 w-3.5" />
              {t("campaign.validUntil")} {formatDate(validUntil)}
            </span>
            <div className="flex flex-wrap items-center gap-2">
              <button
                type="button"
                onClick={() => setModalOpen(true)}
                className={cn(
                  ctaVariants({ variant: "outline", size: "md" }),
                  "text-xs px-3.5 h-10 gap-1.5",
                )}
              >
                <Info className="h-3.5 w-3.5" />
                {t("campaign.learnMore")}
              </button>
              <Link
                to="/contact"
                search={{ service: campaign.title }}
                disabled={campaign.status === "expired"}
                className={cn(
                  ctaVariants({ variant: "primary", size: "md" }),
                  "text-xs px-4 h-10",
                  campaign.status === "expired" && "opacity-50 pointer-events-none cursor-not-allowed",
                )}
              >
                {campaign.status === "upcoming"
                  ? t("campaign.notify")
                  : t("campaign.claim")}
                <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" />
              </Link>
            </div>
          </div>
        </div>
      </article>

      <CampaignDetailModal
        campaign={campaign}
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
      />
    </>
  );
}
