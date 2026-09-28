import { createFileRoute } from "@tanstack/react-router";
import { Clock, Mail, MapPin, Phone } from "lucide-react";
import { Layout } from "@/components/site/Layout";
import { PageHero } from "@/components/site/PageHero";
import { SectionHeading } from "@/components/site/SectionHeading";
import { QuoteForm } from "@/components/site/QuoteForm";
import { contact, offices } from "@/data/site";
import port from "@/assets/hero-port.jpg";

export const Route = createFileRoute("/contact")({
  head: () => ({
    meta: [
      { title: "Contact — Express Shipping Company" },
      { name: "description", content: "Contactez ESC à Sétif ou Alger pour un devis transport, dédouanement ou entreposage." },
      { property: "og:title", content: "Contact — Express Shipping Company" },
      { property: "og:description", content: "Nos bureaux de Sétif et d'Alger, téléphones et horaires." },
    ],
  }),
  component: ContactPage,
});

function ContactPage() {
  return (
    <Layout>
      <PageHero image={port} eyebrow="Contact" title="Parlons de votre projet" description="Demandez un devis ou posez-nous vos questions : notre équipe vous répond rapidement." />
      <section className="section">
        <div className="container-esc grid gap-12 lg:grid-cols-[1fr_1.3fr]">
          <div className="space-y-8">
            <div>
              <h3 className="flex items-center gap-2 font-display text-lg font-bold text-navy"><Phone className="h-5 w-5 text-primary" />Téléphone</h3>
              {contact.phones.map((p) => <a key={p} href={`tel:${p.replace(/\s/g, "")}`} className="mt-2 block text-muted-foreground hover:text-primary">{p}</a>)}
            </div>
            <div>
              <h3 className="flex items-center gap-2 font-display text-lg font-bold text-navy"><Mail className="h-5 w-5 text-primary" />E-mail</h3>
              {contact.emails.map((e) => <a key={e} href={`mailto:${e}`} className="mt-2 block text-muted-foreground hover:text-primary">{e}</a>)}
            </div>
            <div>
              <h3 className="flex items-center gap-2 font-display text-lg font-bold text-navy"><Clock className="h-5 w-5 text-primary" />Horaires</h3>
              {contact.hours.map((h) => <p key={h.days} className="mt-2 text-muted-foreground">{h.days} : {h.time}</p>)}
            </div>
          </div>
          <div><QuoteForm /></div>
        </div>
      </section>
      <section className="section bg-muted/40">
        <div className="container-esc">
          <SectionHeading eyebrow="Nos bureaux" title="Sétif & Alger" />
          <div className="mt-12 grid gap-6 md:grid-cols-2">
            {offices.map((o) => (
              <div key={o.name} className="overflow-hidden rounded-2xl border border-border bg-card shadow-card">
                <iframe title={o.name} src={o.map} className="h-64 w-full border-0" loading="lazy" />
                <div className="p-6">
                  <h3 className="font-display text-lg font-bold text-navy">{o.name}</h3>
                  <p className="mt-2 flex gap-2 text-sm text-muted-foreground"><MapPin className="h-4 w-4 shrink-0 text-primary" />{o.address}</p>
                  <p className="mt-2 text-sm text-muted-foreground">{o.phones.join(" · ")}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </Layout>
  );
}
