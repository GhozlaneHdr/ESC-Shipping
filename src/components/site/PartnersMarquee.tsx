/**
 * PartnersMarquee — infinite horizontal scrolling partner logos strip.
 * Logos render in grayscale / low-opacity by default and transition to
 * full colour on hover. The marquee duplicates the list so the loop is
 * seamless.
 */

import { cn } from "@/lib/utils";

/* ------------------------------------------------------------------ */
/* Partner data — swap SVG placeholders for real <img> tags later      */
/* ------------------------------------------------------------------ */

interface Partner {
  id: string;
  name: string;
  logo: React.ReactNode;
}

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
      {/* Decorative left bar */}
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

/** Ship / anchor icon mark. */
function IconMark({ color = "#0B5ED7" }: { color?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 48 48"
      className="h-10 w-auto"
      aria-hidden="true"
    >
      <circle cx="24" cy="24" r="22" fill={color} opacity="0.12" />
      <path
        d="M24 10v6M21 14h6M14 28l10 6 10-6-3-10H17L14 28Z"
        stroke={color}
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

/** Globe / network icon mark. */
function GlobeMark({ color = "#0B5ED7" }: { color?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 48 48"
      className="h-10 w-auto"
      aria-hidden="true"
    >
      <circle cx="24" cy="24" r="22" fill={color} opacity="0.12" />
      <circle
        cx="24"
        cy="24"
        r="13"
        stroke={color}
        strokeWidth="2.5"
        fill="none"
      />
      <path
        d="M24 11c-4 5-4 21 0 26M24 11c4 5 4 21 0 26M11 24h26"
        stroke={color}
        strokeWidth="2"
        fill="none"
      />
    </svg>
  );
}

const partners: Partner[] = [
  {
    id: "globalTrans",
    name: "GlobalTrans",
    logo: (
      <div className="flex items-center gap-2">
        <IconMark color="#0B5ED7" />
        <WordMark label="GlobalTrans" accent="#0B5ED7" />
      </div>
    ),
  },
  {
    id: "medilog",
    name: "MediLog",
    logo: (
      <div className="flex items-center gap-2">
        <GlobeMark color="#1e40af" />
        <WordMark label="MediLog" accent="#1e40af" />
      </div>
    ),
  },
  {
    id: "alphaFreight",
    name: "AlphaFreight",
    logo: (
      <div className="flex items-center gap-2">
        <IconMark color="#0369a1" />
        <WordMark label="AlphaFreight" accent="#0369a1" />
      </div>
    ),
  },
  {
    id: "nexusPort",
    name: "NexusPort",
    logo: (
      <div className="flex items-center gap-2">
        <GlobeMark color="#075985" />
        <WordMark label="NexusPort" accent="#075985" />
      </div>
    ),
  },
  {
    id: "blueRoute",
    name: "BlueRoute",
    logo: (
      <div className="flex items-center gap-2">
        <IconMark color="#1d4ed8" />
        <WordMark label="BlueRoute" accent="#1d4ed8" />
      </div>
    ),
  },
  {
    id: "seaLink",
    name: "SeaLink",
    logo: (
      <div className="flex items-center gap-2">
        <GlobeMark color="#2563eb" />
        <WordMark label="SeaLink" accent="#2563eb" />
      </div>
    ),
  },
];

/* ------------------------------------------------------------------ */
/* PartnerItem                                                           */
/* ------------------------------------------------------------------ */

function PartnerItem({ partner }: { partner: Partner }) {
  return (
    <div
      title={partner.name}
      className={cn(
        "mx-10 flex shrink-0 items-center",
        /* default: greyscale + soft opacity */
        "opacity-40 grayscale transition-all duration-500 ease-out",
        /* hover: full colour */
        "hover:opacity-100 hover:grayscale-0",
      )}
    >
      {partner.logo}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* PartnersMarquee                                                       */
/* ------------------------------------------------------------------ */

export function PartnersMarquee() {
  /* Duplicate list for seamless loop */
  const items = [...partners, ...partners];

  return (
    <section
      aria-label="Nos partenaires"
      className="border-y border-border bg-background py-14"
    >
      <div className="container-esc mb-10 text-center">
        <p className="eyebrow">Ils nous font confiance</p>
        <h2 className="mt-3 font-display text-2xl font-extrabold text-navy sm:text-3xl">
          Nos partenaires &amp; clients
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
