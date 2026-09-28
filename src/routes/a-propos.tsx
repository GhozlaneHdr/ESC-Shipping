import { createFileRoute } from "@tanstack/react-router";
import { Target, ShieldCheck, Handshake } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { PageHero } from "@/components/site/PageHero";
import { SectionHeading } from "@/components/site/SectionHeading";
import { Reveal } from "@/components/site/Reveal";
import { CtaLink } from "@/components/site/Cta";
import team from "@/assets/about-team.jpg";
import port from "@/assets/hero-port.jpg";

export const Route = createFileRoute("/a-propos")({
  head: () => ({
    meta: [
      { title: "À propos — Express Shipping Company" },
      { name: "description", content: "Découvrez ESC, transitaire algérien basé à Sétif et Alger, et ses valeurs." },
      { property: "og:title", content: "À propos — Express Shipping Company" },
      { property: "og:description", content: "Transitaire algérien basé à Sétif et Alger." },
    ],
  }),
  component: About,
});

const values = [
  { icon: Target, title: "Réactivité", text: "Des réponses rapides et un suivi attentif de chaque dossier." },
  { icon: ShieldCheck, title: "Rigueur", text: "Une gestion documentaire et douanière précise et conforme." },
  { icon: Handshake, title: "Proximité", text: "Un interlocuteur dédié qui connaît votre activité." },
];

function About() {
  return (
    <Layout>
      <PageHero image={port} eyebrow="À propos" title="Express Shipping Company" description="Transitaire et commissionnaire en douane, ESC accompagne les entreprises dans leurs opérations d'import-export depuis et vers l'Algérie." />
      <section className="section">
        <div className="container-esc grid items-center gap-12 lg:grid-cols-2">
          <div>
            <SectionHeading align="left" eyebrow="Notre histoire" title="Plus de dix ans au service de vos flux" />
            <p className="mt-6 leading-relaxed text-muted-foreground">
              Implantée à Sétif et à Alger, ESC organise le transport maritime, aérien et routier de vos marchandises, prend en charge les formalités de dédouanement et propose des solutions d'entreposage. Notre force : une équipe locale expérimentée, appuyée par un réseau de partenaires internationaux.
            </p>
          </div>
          <Reveal><img src={team} alt="Équipe ESC" loading="lazy" className="rounded-2xl shadow-lift" /></Reveal>
        </div>
      </section>
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading eyebrow="Nos valeurs" title="Ce qui nous guide" />
          <div className="mt-14 grid gap-6 md:grid-cols-3">
            {values.map((v, i) => (
              <Reveal key={v.title} delay={i * 80} className="rounded-2xl border border-border bg-card p-8 shadow-card">
                <v.icon className="h-8 w-8 text-primary" />
                <h3 className="mt-5 font-display text-xl font-bold text-navy">{v.title}</h3>
                <p className="mt-3 text-sm text-muted-foreground">{v.text}</p>
              </Reveal>
            ))}
          </div>
          <div className="mt-14 text-center"><CtaLink to="/contact" size="lg">Nous contacter</CtaLink></div>
        </div>
      </section>
    </Layout>
  );
}
