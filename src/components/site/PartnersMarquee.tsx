/**
 * PartnersMarquee — infinite horizontal scrolling partner logos strip.
 * Fetches partner data from the Django API.
 */

import { useQuery } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";
import { getTrustedPartners, type TrustedPartner } from "@/lib/api";

/** Simple SVG text-badge that mimics a brand word-mark. */
function WordMark({
  label,
  accent = "#0B5ED7",
}: {
  label: string;
  accent?: string;
}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 160 48"
      aria-label={label}
      className="h-8 w-auto"
    >
      <rect x="0" y="12" width="5" height="24" rx="2.5" fill={accent} />
      <text
        x="14"
        y="33"
        fontFamily="Manrope, Inter, ui-sans-serif"
        fontWeight="700"
        fontSize="22"
        fill="currentColor"
        letterSpacing="-0.6"
      >
        {label}
      </text>
    </svg>
  );
}

/* ------------------------------------------------------------------ */
/* PartnerItem                                                           */
/* ------------------------------------------------------------------ */

function PartnerItem({ partner }: { partner: TrustedPartner }) {
  return (
    <div
      title={partner.name}
      className={cn(
        "mx-10 flex shrink-0 items-center",
        "opacity-40 grayscale transition-all duration-500 ease-out",
        "hover:opacity-100 hover:grayscale-0",
      )}
    >
      {partner.logo ? (
        <img
          src={partner.logo}
          alt={partner.name}
          className="h-10 w-auto object-contain"
          loading="lazy"
        />
      ) : (
        <WordMark label={partner.name} />
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* PartnersMarquee                                                       */
/* ------------------------------------------------------------------ */

export function PartnersMarquee() {
  const { data: partners, isLoading } = useQuery({
    queryKey: ["partners"],
    queryFn: getTrustedPartners,
  });
  const { t } = useI18n();

  if (isLoading || !partners || partners.length === 0) {
    return (
      <section
        aria-label={t("partners.title")}
        className="border-y border-border bg-background py-14"
      >
        <div className="container-esc mb-10 text-center">
          <p className="eyebrow">{t("partners.eyebrow")}</p>
          <h2 className="mt-3 font-display text-2xl font-extrabold text-navy sm:text-3xl">
            {t("partners.title")}
          </h2>
        </div>
      </section>
    );
  }

  /* Duplicate list for seamless loop */
  const items = [...partners, ...partners];

  return (
    <section
      aria-label={t("partners.title")}
      className="border-y border-border bg-background py-14"
    >
      <div className="container-esc mb-10 text-center">
        <p className="eyebrow">{t("partners.eyebrow")}</p>
        <h2 className="mt-3 font-display text-2xl font-extrabold text-navy sm:text-3xl">
          {t("partners.title")}
        </h2>
      </div>

      {/* Mask edges so logos fade in/out */}
      <div
        className="relative overflow-hidden"
        style={{
          maskImage:
            "linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%)",
          WebkitMaskImage:
            "linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%)",
        }}
      >
        <div className="partners-track flex w-max">
          {items.map((partner, i) => (
            <PartnerItem
              key={`${partner.id}-${i}`}
              partner={partner}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
