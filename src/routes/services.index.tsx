import { createFileRoute } from "@tanstack/react-router";
import { Layout } from "@/components/site/Layout";
import { PageHero } from "@/components/site/PageHero";
import { ServiceCard } from "@/components/site/ServiceCard";
import { Reveal } from "@/components/site/Reveal";
import { useI18n } from "@/lib/i18n";
import { services as staticServices } from "@/data/site";
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
  loader: async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/cms/services/");
      const data = res.ok ? await res.json() : null;
      const dbServices = data?.results ?? null;
      return { dbServices };
    } catch {
      console.error("[Services loader] Failed to fetch from Django API");
      return { dbServices: null };
    }
  },
  component: ServicesPage,
});

function ServicesPage() {
  const { dbServices } = Route.useLoaderData();
  const { t } = useI18n();
  const displayServices = dbServices && dbServices.length > 0 ? dbServices : staticServices;

  return (
    <Layout>
      <PageHero image={port} eyebrow={t("services.hero.eyebrow")} title={t("services.hero.title")} description={t("services.hero.subtitle")} />
      <section className="section">
        <div className="container-esc grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {displayServices.map((s: any, i: number) => (
            <Reveal key={s.slug} delay={i * 60}><ServiceCard service={s} /></Reveal>
          ))}
        </div>
      </section>
    </Layout>
  );
}
