import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { ArrowRight, Calendar, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import { ctaVariants } from "@/components/site/Cta";
import { CampaignDetailModal } from "@/components/site/CampaignDetailModal";
import { useI18n } from "@/lib/i18n";
import type { AssociatedCampaign } from "@/lib/api";

const statusMeta: Record<string, { label: string; color: string; dot: string }> = {
  "active":   { label: "Active",          color: "bg-emerald-100 text-emerald-700", dot: "bg-emerald-500" },
  "limited":  { label: "Offre limitée",   color: "bg-amber-100 text-amber-700",   dot: "bg-amber-500" },
  "upcoming": { label: "À venir",         color: "bg-blue-100 text-blue:700",     dot: "bg-blue-500" },
  "expired":  { label: "Expirée",         color: "bg-gray-100 text-gray-500",     dot: "bg-gray-400" },
};

export function AssociatedCampaignCard({
  campaign,
}: {
  campaign: AssociatedCampaign;
}) {
  const { t, locale } = useI18n();
  const [modalOpen, setModalOpen] = useState(false);
  const meta = statusMeta[campaign.status] ?? statusMeta["active"]!;

  const category = (locale === "en" && campaign.category_en) ? campaign.category_en : campaign.category;
  const title = (locale === "en" && campaign.title_en) ? campaign.title_en : campaign.title;
  const description = (locale === "en" && campaign.description_en) ? campaign.description_en : campaign.description;
  const badge = (locale === "en" && campaign.badge_en) ? campaign.badge_en : campaign.badge;
  const validUntil = campaign.valid_until || campaign.validUntil || "";

  const formatDate = (iso: string) => {
    try {
      return new Intl.DateTimeFormat(locale === "en" ? "en-US" : "fr-FR", {
        day: "numeric",
        month: "short",
        year: "numeric",
      }).format(new Date(iso));
    } catch {
      return iso;
    }
  };

  return (
    <>
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
            <span className="eyebrow text-[0.65rem]">{category}</span>
            <span className="rounded-full bg-navy/10 px-2.5 py-0.5 text-[0.65rem] font-bold uppercase tracking-wide text-navy dark:bg-navy-foreground/10 dark:text-navy-foreground">
              {badge}
            </span>
          </div>

          {/* Title */}
          <h4 className="mt-3 font-display text-base font-bold leading-snug text-navy">
            {title}
          </h4>

          {/* Description */}
          <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
            {description}
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
                {t(`campaign.status.${campaign.status}`) || meta.label}
              </span>
              <span className="flex items-center gap-1 text-[0.65rem] text-muted-foreground">
                <Calendar className="h-3 w-3" />
                {formatDate(validUntil)}
              </span>
            </div>

            <button
              type="button"
              onClick={() => setModalOpen(true)}
              className={cn(
                ctaVariants({ variant: "soft", size: "md" }),
                "h-9 px-3.5 text-xs gap-1",
              )}
            >
              <Info className="h-3.5 w-3.5" />
              {t("campaign.details")}
            </button>
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
