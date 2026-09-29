import { createFileRoute } from "@tanstack/react-router";
import { Anchor, BadgePercent, LayoutGrid } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { SectionHeading } from "@/components/site/SectionHeading";
import { Reveal } from "@/components/site/Reveal";
import { CtaLink } from "@/components/site/Cta";
import { MaritimeCampaignCard } from "@/components/site/MaritimeCampaignCard";
import { AssociatedCampaignCard } from "@/components/site/AssociatedCampaignCard";
import { maritimeCampaigns, associatedCampaigns, statusMeta } from "@/data/campaigns";
import type { CampaignStatus } from "@/data/campaigns";

export const Route = createFileRoute("/campagnes-maritimes")({
  head: () => ({
    meta: [
      { title: "Campagnes Maritimes — Express Shipping Company" },
      {
        name: "description",
        content:
          "Découvrez nos offres et promotions sur le transport maritime : réductions sur les lignes Europe, Asie, Turquie et Amériques vers l'Algérie.",
      },
      {
        property: "og:title",
        content: "Campagnes Maritimes — Express Shipping Company",
      },
    ],
  }),
  component: CampagnesMaritimes,
});

/* ── Filter bar helper ──────────────────────────────────────────── */
const filters: { value: CampaignStatus | "all"; label: string }[] = [
  { value: "all",      label: "Toutes"         },
  { value: "active",   label: "Actives"         },
  { value: "limited",  label: "Offres limitées" },
  { value: "upcoming", label: "À venir"         },
];

/* ── Stats strip ────────────────────────────────────────────────── */
const pageStats = [
  { icon: BadgePercent, value: "–15 %",    label: "Remise maximale"      },
  { icon: Anchor,       value: "4",         label: "Lignes en promotion"  },
  { icon: LayoutGrid,   value: "5",         label: "Offres associées"     },
];

/* ================================================================= *
 *  Page component                                                     *
 * ================================================================= */
function CampagnesMaritimes() {
  return (
    <Layout>
      {/* ── Hero ─────────────────────────────────────────────────── */}
      <section className="relative isolate overflow-hidden bg-navy pt-20">
        {/* Grid-lines overlay */}
        <div className="absolute inset-0 -z-10 grid-lines" />
        {/* Blue radial glow */}
        <div
          className="pointer-events-none absolute inset-0 -z-10"
          style={{
            background:
              "radial-gradient(ellipse 80% 60% at 50% 0%, oklch(0.523 0.201 262.5 / 0.35), transparent)",
          }}
        />

        <div className="container-esc py-20 sm:py-28 text-center">
          <Reveal>
            <p className="eyebrow text-navy-foreground/70">Promotions &amp; Offres spéciales</p>
            <h1 className="mt-4 font-display text-4xl font-extrabold leading-[1.05] text-navy-foreground sm:text-5xl lg:text-6xl">
              Campagnes Maritimes
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-navy-foreground/70">
              Des réductions exclusives sur nos principales lignes maritimes — Europe, Asie, Turquie
              et Amériques — pour optimiser vos coûts d'import-export.
            </p>
            <div className="mt-10 flex flex-wrap justify-center gap-4">
              <CtaLink to="/contact" size="lg">
                Demander un devis
              </CtaLink>
              <CtaLink to="/contact" variant="ghostLight" size="lg">
                Nous contacter
              </CtaLink>
            </div>
          </Reveal>
        </div>

        {/* Stats strip */}
        <div className="border-t border-navy-foreground/10">
          <div className="container-esc grid grid-cols-3 divide-x divide-navy-foreground/10 py-6">
            {pageStats.map(({ icon: Icon, value, label }) => (
              <div key={label} className="flex flex-col items-center gap-1 px-4 text-center">
                <Icon className="h-5 w-5 text-primary" />
                <p className="font-display text-2xl font-extrabold text-navy-foreground sm:text-3xl">
                  {value}
                </p>
                <p className="text-xs text-navy-foreground/60">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Active status legend strip ────────────────────────────── */}
      <section className="border-b border-border bg-surface">
        <div className="container-esc flex flex-wrap items-center gap-3 py-4">
          <span className="text-xs font-semibold text-muted-foreground uppercase tracking-widest mr-2">
            Légende :
          </span>
          {(["active", "limited", "upcoming", "expired"] as CampaignStatus[]).map((s) => {
            const m = statusMeta[s];
            return (
              <span
                key={s}
                className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold ${m.color}`}
              >
                <span className={`h-1.5 w-1.5 rounded-full ${m.dot}`} />
                {m.label}
              </span>
            );
          })}
        </div>
      </section>

      {/* ── Maritime Campaigns ───────────────────────────────────── */}
      <section className="section">
        <div className="container-esc">
          <SectionHeading
            eyebrow="Campagnes maritimes"
            title="Nos offres sur les lignes maritimes"
            description="Bénéficiez de tarifs préférentiels sur les principales liaisons maritimes desservant l'Algérie."
          />

          <div className="mt-12 grid gap-6 sm:grid-cols-2 xl:grid-cols-2">
            {maritimeCampaigns.map((campaign, i) => (
              <Reveal key={campaign.id} delay={i * 80}>
                <MaritimeCampaignCard campaign={campaign} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── Associated Campaigns ─────────────────────────────────── */}
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading
            eyebrow="Campagnes associées"
            title="Offres complémentaires"
            description="Maximisez la valeur de vos expéditions maritimes avec nos packs logistiques, douaniers et d'assurance associés."
          />

          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {associatedCampaigns.map((campaign, i) => (
              <Reveal key={campaign.id} delay={i * 70}>
                <AssociatedCampaignCard campaign={campaign} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA banner ───────────────────────────────────────────── */}
      <section className="section bg-navy">
        <div className="container-esc text-center">
          <SectionHeading
            light
            title="Une expédition à planifier ?"
            description="Contactez-nous pour bénéficier de l'une de nos campagnes ou obtenir une offre personnalisée."
          />
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <CtaLink to="/contact" size="lg">
              Demander un devis
            </CtaLink>
            <CtaLink to="/services/transport-maritime" variant="ghostLight" size="lg">
              Voir nos services maritimes
            </CtaLink>
          </div>
        </div>
      </section>
    </Layout>
  );
}
