import { useState } from "react";
import { Link } from "@tanstack/react-router";
import { ArrowRight, Calendar, CheckCircle2, MapPin, Tag, X } from "lucide-react";
import { ctaVariants } from "./Cta";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export interface CampaignModalData {
  title: string;
  subtitle?: string;
  category?: string;
  badge?: string;
  discount?: string;
  route_from?: string;
  route_to?: string;
  description: string;
  valid_until?: string;
  status: string;
  highlights_list?: string[];
}

export function CampaignDetailModal({
  campaign,
  isOpen,
  onClose,
}: {
  campaign: CampaignModalData | null;
  isOpen: boolean;
  onClose: () => void;
}) {
  const { t, locale } = useI18n();

  if (!isOpen || !campaign) return null;

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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-navy/60 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      {/* Modal Dialog */}
      <div className="relative z-10 w-full max-w-lg overflow-hidden rounded-3xl border border-border bg-card p-6 shadow-lift sm:p-8">
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute right-4 top-4 grid h-9 w-9 place-items-center rounded-full border border-border text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </button>

        {/* Category / Badge header */}
        <div className="flex flex-wrap items-center gap-2 pr-8">
          {campaign.category && (
            <span className="eyebrow text-xs">{campaign.category}</span>
          )}
          {campaign.badge && (
            <span className="rounded-full bg-navy/10 px-3 py-1 text-xs font-bold uppercase tracking-wide text-navy dark:bg-navy-foreground/10 dark:text-navy-foreground">
              {campaign.badge}
            </span>
          )}
          {campaign.discount && (
            <span className="flex items-center gap-1 rounded-full bg-primary/10 px-3 py-1 text-xs font-bold text-primary">
              <Tag className="h-3.5 w-3.5" />
              {campaign.discount}
            </span>
          )}
        </div>

        {/* Title */}
        <h3 className="mt-4 font-display text-2xl font-extrabold text-navy">
          {campaign.title}
        </h3>

        {campaign.subtitle && (
          <p className="mt-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            {campaign.subtitle}
          </p>
        )}

        {/* Route if available */}
        {campaign.route_from && campaign.route_to && (
          <div className="mt-4 flex items-center gap-2 rounded-xl bg-surface px-4 py-3 text-sm">
            <MapPin className="h-4 w-4 shrink-0 text-primary" />
            <span className="font-semibold text-foreground">
              {campaign.route_from}
            </span>
            <ArrowRight className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            <span className="font-semibold text-foreground">
              {campaign.route_to}
            </span>
          </div>
        )}

        {/* Description */}
        <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
          {campaign.description}
        </p>

        {/* Highlights */}
        {campaign.highlights_list && campaign.highlights_list.length > 0 && (
          <div className="mt-5 rounded-2xl bg-muted/40 p-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-navy mb-3">
              {t("modal.included")}
            </h4>
            <ul className="space-y-2">
              {campaign.highlights_list.map((item) => (
                <li key={item} className="flex items-center gap-2 text-sm text-foreground">
                  <CheckCircle2 className="h-4 w-4 shrink-0 text-primary" />
                  {item}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Validity */}
        <div className="mt-5 flex items-center gap-2 text-xs text-muted-foreground">
          <Calendar className="h-4 w-4 text-primary" />
          <span>{t("modal.validUntil")} {formatDate(campaign.valid_until || "")}</span>
        </div>

        {/* Action button */}
        <div className="mt-6 flex flex-wrap justify-end gap-3 pt-4 border-t border-border">
          <button
            type="button"
            onClick={onClose}
            className={cn(ctaVariants({ variant: "outline", size: "md" }), "h-11 px-5 text-xs")}
          >
            {t("modal.close")}
          </button>
          <Link
            to="/contact"
            search={{ service: campaign.title }}
            onClick={onClose}
            className={cn(ctaVariants({ variant: "primary", size: "md" }), "h-11 px-6 text-xs")}
          >
            {t("modal.requestQuote")}
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
