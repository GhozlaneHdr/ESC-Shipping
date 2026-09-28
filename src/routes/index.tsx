import { createFileRoute } from "@tanstack/react-router";
import { CheckCircle2, Phone } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { CtaLink, CtaAnchor } from "@/components/site/Cta";
import { SectionHeading } from "@/components/site/SectionHeading";
import { ServiceCard } from "@/components/site/ServiceCard";
import { Reveal } from "@/components/site/Reveal";
import { Counter } from "@/components/site/Counter";
import { services, stats, contact } from "@/data/site";
import hero from "@/assets/hero-port.jpg";
import team from "@/assets/about-team.jpg";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Express Shipping Company — Transitaire en Algérie" },
      { name: "description", content: "ESC : transport maritime, aérien, routier, dédouanement et entreposage depuis Sétif et Alger." },
      { property: "og:title", content: "Express Shipping Company — Transitaire en Algérie" },
      { property: "og:description", content: "Transport, dédouanement et entreposage : un interlocuteur unique pour vos opérations d'import-export." },
    ],
  }),
  component: Home,
});

function Home() {
  return (
    <Layout>
      <section className="relative isolate -mt-20 overflow-hidden bg-navy pt-20">
        <img src={hero} alt="Port de commerce" className="absolute inset-0 -z-10 h-full w-full object-cover opacity-40" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-navy via-navy/80 to-transparent" />
        <div className="container-esc py-28 sm:py-40">
          <p className="eyebrow text-navy-foreground/70">Transitaire & commissionnaire en Algérie</p>
          <h1 className="mt-5 max-w-3xl font-display text-4xl font-extrabold leading-[1.05] text-navy-foreground sm:text-6xl">
            Vos marchandises, acheminées en toute confiance.
          </h1>
          <p className="mt-6 max-w-xl text-lg text-navy-foreground/75">
            Maritime, aérien, routier, dédouanement et entreposage : ESC coordonne l'ensemble de vos opérations d'import-export.
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <CtaLink to="/contact" size="lg">Demander un devis</CtaLink>
            <CtaAnchor href={`tel:${contact.phones[0]!.replace(/\s/g, "")}`} variant="ghostLight" size="lg">
              <Phone className="h-4 w-4" /> {contact.phones[0]}
            </CtaAnchor>
          </div>
        </div>
      </section>

      <section className="border-b border-border bg-background">
        <div className="container-esc grid gap-8 py-12 sm:grid-cols-3">
          {stats.map((s) => (
            <div key={s.label} className="text-center">
              <p className="font-display text-4xl font-extrabold text-primary">
                <Counter value={s.value} suffix={s.suffix} />
              </p>
              <p className="mt-2 text-sm text-muted-foreground">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="container-esc">
          <SectionHeading eyebrow="Nos services" title="Une offre logistique complète" description="Sept métiers complémentaires pour accompagner vos flux de bout en bout." />
          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {services.map((s, i) => (
              <Reveal key={s.slug} delay={i * 60}><ServiceCard service={s} /></Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="section bg-muted/40">
        <div className="container-esc grid items-center gap-12 lg:grid-cols-2">
          <Reveal><img src={team} alt="Équipe ESC" loading="lazy" className="rounded-2xl shadow-lift" /></Reveal>
          <div>
            <SectionHeading align="left" eyebrow="Pourquoi ESC" title="Un partenaire local, un réseau international" />
            <ul className="mt-8 space-y-4">
              {["Équipes basées à Sétif et à Alger", "Un interlocuteur unique pour tout votre dossier", "Maîtrise des procédures douanières et portuaires algériennes", "Réseau de partenaires dans le monde entier"].map((t) => (
                <li key={t} className="flex gap-3 text-foreground"><CheckCircle2 className="h-5 w-5 shrink-0 text-primary" />{t}</li>
              ))}
            </ul>
            <CtaLink to="/a-propos" variant="outline" className="mt-10">Découvrir ESC</CtaLink>
          </div>
        </div>
      </section>

      <section className="section bg-navy">
        <div className="container-esc text-center">
          <SectionHeading light title="Un projet d'expédition ?" description="Parlez-nous de votre besoin, nous revenons vers vous rapidement avec une solution adaptée." />
          <CtaLink to="/contact" size="lg" className="mt-10">Demander un devis</CtaLink>
        </div>
      </section>
    </Layout>
  );
}
