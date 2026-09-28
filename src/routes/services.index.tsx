import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "@/components/site/Layout";
import { PageHero } from "@/components/site/PageHero";
import { ServiceCard } from "@/components/site/ServiceCard";
import { Reveal } from "@/components/site/Reveal";
import { services } from "@/data/site";
import port from "@/assets/svc-maritime.jpg";

export const Route = createFileRoute("/services/")({
  head: () => ({
    meta: [
      { title: "Nos services — Express Shipping Company" },
      { name: "description", content: "Transport maritime, aérien, routier, dédouanement, entreposage, agent de fret et agent maritime." },
      { property: "og:title", content: "Nos services — Express Shipping Company" },
      { property: "og:description", content: "Sept services logistiques pour vos opérations d'import-export." },
    ],
  }),
  component: ServicesPage,
});

function ServicesPage() {
  return (
    <Layout>
      <PageHero image={port} eyebrow="Services" title="Nos services logistiques" description="Une offre complète pour organiser, sécuriser et accélérer vos expéditions." />
      <section className="section">
        <div className="container-esc grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((s, i) => (
            <Reveal key={s.slug} delay={i * 60}><ServiceCard service={s} /></Reveal>
          ))}
        </div>
      </section>
    </Layout>
  );
}
