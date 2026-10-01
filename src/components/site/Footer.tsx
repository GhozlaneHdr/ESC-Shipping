import { Link } from "@tanstack/react-router";
import { Facebook, Mail, MapPin, Phone } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { Logo } from "./Logo";
import { getServices } from "@/lib/api";

export function Footer() {
  const { data: services } = useQuery({
    queryKey: ["services"],
    queryFn: getServices,
  });

  const contact = {
    phones: ["+213 555 50 86 21", "+213 555 50 86 20", "+213 555 50 86 19"],
    emails: ["contact@ex-shipping.com", "sales@ex-shipping.com"],
    facebook: "https://www.facebook.com/people/Express-Shipping-Company/100063539442443/",
  };

  const offices = [
    {
      name: "ESC — SÉTIF",
      address: "Cité 326 logts ZHUN, Bâtiment A06, Local n°24, Sétif",
    },
    {
      name: "ESC — ALGER",
      address: "1 Rue Mohamed Belouizdad, Sidi M'Hamed, Alger",
    },
  ];

  return (
    <footer className="bg-navy-deep text-navy-foreground">
      <div className="container-esc grid gap-12 py-16 md:grid-cols-2 lg:grid-cols-12 lg:py-20">
        <div className="lg:col-span-4">
          <Logo light />
          <p className="mt-6 max-w-sm text-sm leading-relaxed text-navy-foreground/70">
            Express Shipping Company — Votre partenaire logistique pour des solutions de fret
            fiables, rapides et sécurisées.
          </p>
          <a
            href={contact.facebook}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-6 inline-flex h-11 w-11 items-center justify-center rounded-xl border border-navy-foreground/20 text-navy-foreground/80 transition-colors hover:border-primary hover:bg-primary hover:text-primary-foreground"
            aria-label="Facebook ESC"
          >
            <Facebook className="h-5 w-5" />
          </a>
        </div>

        <div className="lg:col-span-2">
          <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-navy-foreground">
            Navigation
          </h3>
          <ul className="mt-5 space-y-3 text-sm text-navy-foreground/70">
            {[
              { to: "/", label: "Accueil" },
              { to: "/a-propos", label: "À propos" },
              { to: "/services", label: "Services" },
              { to: "/contact", label: "Contact" },
            ].map((l) => (
              <li key={l.to}>
                <Link to={l.to} className="transition-colors hover:text-primary-foreground">
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="lg:col-span-3">
          <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-navy-foreground">
            Services
          </h3>
          <ul className="mt-5 space-y-3 text-sm text-navy-foreground/70">
            {(services || []).map((s) => (
              <li key={s.slug}>
                <Link to={`/services/${s.slug}` as any} className="transition-colors hover:text-primary-foreground">
                  {s.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        <div className="lg:col-span-3">
          <h3 className="text-sm font-semibold uppercase tracking-[0.16em] text-navy-foreground">
            Contact
          </h3>
          <ul className="mt-5 space-y-3 text-sm text-navy-foreground/70">
            {contact.phones.map((p) => (
              <li key={p} className="flex items-center gap-2">
                <Phone className="h-4 w-4 shrink-0 text-primary" />
                <a
                  href={`tel:${p.replace(/\s/g, "")}`}
                  className="transition-colors hover:text-primary-foreground"
                >
                  {p}
                </a>
              </li>
            ))}
            {contact.emails.map((e) => (
              <li key={e} className="flex items-center gap-2">
                <Mail className="h-4 w-4 shrink-0 text-primary" />
                <a href={`mailto:${e}`} className="transition-colors hover:text-primary-foreground">
                  {e}
                </a>
              </li>
            ))}
            {offices.map((o) => (
              <li key={o.name} className="flex gap-2">
                <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
                <span>
                  <span className="block font-medium text-navy-foreground">{o.name}</span>
                  {o.address}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="border-t border-navy-foreground/10">
        <div className="container-esc flex flex-col items-center gap-2 py-5 text-xs text-navy-foreground/60 sm:flex-row sm:justify-between">
          {/* Left — copyright */}
          <p className="text-center sm:text-left">
            © 2026 ESC — Express Shipping Company. Tous droits réservés.
          </p>

          {/* Centre — designer credit */}
          <p className="text-center">
            Designed &amp; Developed by&nbsp;
            <span className="font-semibold text-navy-foreground/80">IntellectSoft</span>
            &nbsp;—&nbsp;
            <span className="font-semibold text-navy-foreground/80">Zetoutou Faycal</span>
          </p>

          {/* Right — location */}
          <p className="text-center sm:text-right">
            Transitaire &amp; commissionnaire — Sétif · Alger
          </p>
        </div>
      </div>
    </footer>
  );
}
