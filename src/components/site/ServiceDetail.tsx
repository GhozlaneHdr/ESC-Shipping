import { CheckCircle2 } from "lucide-react";
import { Layout } from "./Layout";
import { PageHero } from "./PageHero";
import { SectionHeading } from "./SectionHeading";
import { Reveal } from "./Reveal";
import { ServiceCard } from "./ServiceCard";
import { QuoteForm } from "./QuoteForm";
import { serviceBySlug, services } from "@/data/site";

export function serviceHead(slug: string) {
  const s = serviceBySlug(slug);
  const title = `${s.name} — Express Shipping Company`;
  return {
    meta: [
      { title },
      { name: "description", content: s.short },
      { property: "og:title", content: title },
      { property: "og:description", content: s.short },
    ],
  };
}

export function ServiceDetail({ slug }: { slug: string }) {
  const s = serviceBySlug(slug);
  const others = services.filter((o) => o.slug !== slug).slice(0, 3);
  return (
    <Layout>
      <PageHero image={s.image} eyebrow="Services" title={s.name} description={s.intro} />
      <section className="section">
        <div className="container-esc grid gap-12 lg:grid-cols-2">
          <div>
            <SectionHeading align="left" eyebrow="Ce que nous proposons" title="Les points clés" />
            <ul className="mt-8 space-y-4">
              {s.benefits.map((b) => (
                <li key={b} className="flex gap-3"><CheckCircle2 className="h-5 w-5 shrink-0 text-primary" />{b}</li>
              ))}
            </ul>
          </div>
          <div>
            <SectionHeading align="left" eyebrow="Pourquoi ESC" title="Nos atouts" />
            <ul className="mt-8 space-y-4">
              {s.why.map((b) => (
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
            {s.steps.map((st, i) => (
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
          <SectionHeading eyebrow="Devis" title={`Un besoin en ${s.name.toLowerCase()} ?`} />
          <div className="mt-10"><QuoteForm /></div>
        </div>
      </section>
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading eyebrow="Autres services" title="Découvrez aussi" />
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {others.map((o) => <ServiceCard key={o.slug} service={o} />)}
          </div>
        </div>
      </section>
    </Layout>
  );
}
