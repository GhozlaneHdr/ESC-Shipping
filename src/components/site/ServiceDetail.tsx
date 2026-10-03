import { CheckCircle2 } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { Layout } from "./Layout";
import { PageHero } from "./PageHero";
import { SectionHeading } from "./SectionHeading";
import { Reveal } from "./Reveal";
import { ServiceCard } from "./ServiceCard";
import { QuoteForm } from "./QuoteForm";
import { getServiceBySlug, getServices } from "@/lib/api";
import { services as staticServices } from "@/data/site";

export function serviceHead(slug: string) {
  const title = `Service — Express Shipping Company`;
  return {
    meta: [
      { title },
      { name: "description", content: "Service ESC" },
    ],
  };
}

export function ServiceDetail({ slug }: { slug: string }) {
  const { data: apiService, isLoading } = useQuery({
    queryKey: ["service", slug],
    queryFn: () => getServiceBySlug(slug),
  });

  const { data: allServices } = useQuery({
    queryKey: ["services"],
    queryFn: getServices,
  });

  const staticService = staticServices.find((item) => item.slug === slug);
  const service = apiService ?? (staticService ? {
    ...staticService,
    short_description: staticService.short,
    long_intro: staticService.intro,
    benefits_list: staticService.benefits,
    why_us_list: staticService.why,
    steps: staticService.steps,
  } : null);

  if (isLoading && !service) {
    return (
      <Layout>
        <div className="container-esc py-20 text-center">
          <p className="text-muted-foreground">Chargement...</p>
        </div>
      </Layout>
    );
  }

  if (!service) {
    return (
      <Layout>
        <div className="container-esc py-20 text-center">
          <p className="text-muted-foreground">Service introuvable.</p>
        </div>
      </Layout>
    );
  }

  const others = (allServices || [])
    .filter((o: any) => o.slug !== slug)
    .slice(0, 3);

  return (
    <Layout>
      <PageHero image={service.image} eyebrow="Services" title={service.name} description={service.short_description} />
      <section className="section">
        <div className="container-esc grid gap-12 lg:grid-cols-2">
          <div>
            <p className="max-w-2xl text-lg leading-relaxed text-muted-foreground">{service.long_intro}</p>
            <SectionHeading align="left" eyebrow="Ce que nous proposons" title="Les points clés" />
            <ul className="mt-8 space-y-4">
              {service.benefits_list.map((b: string) => (
                <li key={b} className="flex gap-3"><CheckCircle2 className="h-5 w-5 shrink-0 text-primary" />{b}</li>
              ))}
            </ul>
          </div>
          <div>
            <SectionHeading align="left" eyebrow="Pourquoi ESC" title="Nos atouts" />
            <ul className="mt-8 space-y-4">
              {service.why_us_list.map((b: string) => (
                <li key={b} className="flex gap-3"><CheckCircle2 className="h-5 w-5 shrink-0 text-primary" />{b}</li>
              ))}
            </ul>
          </div>
        </div>
      </section>
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading eyebrow="Déroulement" title="Comment nous travaillons" />
          <ol className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {service.steps.map((st: any, i: number) => (
              <Reveal as="li" key={st.title} delay={i * 80} className="rounded-2xl border border-border bg-card p-6 shadow-card">
                <span className="font-display text-3xl font-extrabold text-primary">0{i + 1}</span>
                <h3 className="mt-3 font-display text-lg font-bold text-navy">{st.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{st.text}</p>
              </Reveal>
            ))}
          </ol>
        </div>
      </section>
      <section className="section">
        <div className="container-esc mx-auto max-w-3xl">
          <SectionHeading eyebrow="Devis" title={`Un besoin en ${service.name.toLowerCase()} ?`} />
          <div className="mt-10"><QuoteForm /></div>
        </div>
      </section>
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading eyebrow="Autres services" title="Découvrez aussi" />
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {others.map((o: any) => <ServiceCard key={o.slug} service={o} />)}
          </div>
        </div>
      </section>
    </Layout>
  );
}
