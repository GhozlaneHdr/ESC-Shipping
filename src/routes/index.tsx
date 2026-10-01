import { createFileRoute } from "@tanstack/react-router";
import { CheckCircle2, Phone } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { CtaLink, CtaAnchor } from "@/components/site/Cta";
import { SectionHeading } from "@/components/site/SectionHeading";
import { ServiceCard } from "@/components/site/ServiceCard";
import { Reveal } from "@/components/site/Reveal";
import { Counter } from "@/components/site/Counter";
import { PartnersMarquee } from "@/components/site/PartnersMarquee";
import { useI18n } from "@/lib/i18n";
import { services as staticServices, stats as staticStats, contact } from "@/data/site";
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
  loader: async () => {
    try {
      const [statsRes, servicesRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/api/v1/cms/stats/"),
        fetch("http://127.0.0.1:8000/api/v1/cms/services/"),
      ]);

      const statsData = statsRes.ok ? await statsRes.json() : null;
      const servicesData = servicesRes.ok ? await servicesRes.json() : null;

      const dbStats = statsData?.results ?? null;
      const dbServices = servicesData?.results ?? null;

      return { dbStats, dbServices };
    } catch (error) {
      console.error("[CMS loader] Failed to fetch from Django API:", error);
      return { dbStats: null, dbServices: null };
    }
  },
  component: Home,
});

function Home() {
  const { dbStats, dbServices } = Route.useLoaderData();
  const { t } = useI18n();

  const displayStats = dbStats && dbStats.length > 0 ? dbStats : staticStats;
  const displayServices = dbServices && dbServices.length > 0 ? dbServices : staticServices;

  return (
    <Layout>
      <section className="relative isolate -mt-20 overflow-hidden bg-navy pt-20">
        <img src={hero} alt="Port de commerce" className="absolute inset-0 -z-10 h-full w-full object-cover opacity-40" />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-navy via-navy/80 to-transparent" />
        <div className="container-esc py-28 sm:py-40">
          <p className="eyebrow text-navy-foreground/70">{t("home.hero.eyebrow")}</p>
          <h1 className="mt-5 max-w-3xl font-display text-4xl font-extrabold leading-[1.05] text-navy-foreground sm:text-6xl">
            {t("home.hero.title")}
          </h1>
          <p className="mt-6 max-w-xl text-lg text-navy-foreground/75">
            {t("home.hero.subtitle")}
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <CtaLink to="/contact" size="lg">{t("home.hero.cta")}</CtaLink>
            <CtaAnchor href={`tel:${contact.phones[0]!.replace(/\s/g, "")}`} variant="ghostLight" size="lg">
              <Phone className="h-4 w-4" /> {contact.phones[0]}
            </CtaAnchor>
          </div>
        </div>
      </section>

      <section className="border-b border-border bg-background">
        <div className="container-esc grid gap-8 py-12 sm:grid-cols-3">
          {displayStats.map((s: any) => (
            <div key={s.label} className="text-center">
              <p className="font-display text-4xl font-extrabold text-primary">
                <Counter value={s.value} suffix={s.suffix} />
              </p>
              <p className="mt-2 text-sm text-muted-foreground">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      <PartnersMarquee />

      <section className="section">
        <div className="container-esc">
          <SectionHeading eyebrow={t("home.services.eyebrow")} title={t("home.services.title")} description={t("home.services.subtitle")} />
          <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {displayServices.map((s: any, i: number) => (
              <Reveal key={s.slug} delay={i * 60}><ServiceCard service={s} /></Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="section bg-muted/40">
        <div className="container-esc grid items-center gap-12 lg:grid-cols-2">
          <Reveal><img src={team} alt="Équipe ESC" loading="lazy" className="rounded-2xl shadow-lift" /></Reveal>
          <div>
            <SectionHeading align="left" eyebrow={t("home.why.eyebrow")} title={t("home.why.title")} />
            <ul className="mt-8 space-y-4">
              {[t("home.why.1"), t("home.why.2"), t("home.why.3"), t("home.why.4")].map((item) => (
                <li key={item} className="flex gap-3 text-foreground"><CheckCircle2 className="h-5 w-5 shrink-0 text-primary" />{item}</li>
              ))}
            </ul>
            <CtaLink to="/a-propos" variant="outline" className="mt-10">{t("common.learnMore")}</CtaLink>
          </div>
        </div>
      </section>

      <section className="section bg-navy">
        <div className="container-esc text-center">
          <SectionHeading light title={t("home.cta.title")} description={t("home.cta.subtitle")} />
          <CtaLink to="/contact" size="lg" className="mt-10">{t("home.cta.button")}</CtaLink>
        </div>
      </section>
    </Layout>
  );
}
