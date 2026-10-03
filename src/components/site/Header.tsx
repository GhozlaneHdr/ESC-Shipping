import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronDown, Menu, X } from "lucide-react";
import { Logo } from "./Logo";
import { CtaLink } from "./Cta";
import { LanguageSwitcher } from "./LanguageSwitcher";
import { getServices } from "@/lib/api";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

const navLinks = [
  { to: "/", key: "nav.home" },
  { to: "/a-propos", key: "nav.about" },
  { to: "/services", key: "nav.services" },
  { to: "/resources", key: "nav.resources" },
  { to: "/contact", key: "nav.contact" },
];

export function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [servicesOpen, setServicesOpen] = useState(false);
  const { t } = useI18n();

  const { data: services } = useQuery({
    queryKey: ["services"],
    queryFn: getServices,
  });

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all duration-300",
        scrolled
          ? "border-b border-border bg-background/90 shadow-header backdrop-blur-xl"
          : "border-b border-transparent bg-background/70 backdrop-blur-md",
      )}
    >
      <div className="container-esc flex h-20 items-center justify-between gap-6">
        <Link to="/" aria-label="ESC — Accueil" onClick={() => setOpen(false)}>
          <Logo />
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Navigation principale">
          {navLinks.map((link) =>
            link.key === "nav.services" ? (
              <div key={link.to} className="relative" onMouseLeave={() => setServicesOpen(false)}>
                <Link
                  to="/services"
                  onMouseEnter={() => setServicesOpen(true)}
                  onFocus={() => setServicesOpen(true)}
                  className="flex items-center gap-1 rounded-full px-4 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-accent hover:text-primary [&.active]:text-primary"
                >
                  {t("nav.services")}
                  <ChevronDown className="h-4 w-4" />
                </Link>
                <div
                  className={cn(
                    "absolute left-1/2 top-full w-80 -translate-x-1/2 pt-3 transition-all duration-200",
                    servicesOpen
                      ? "visible translate-y-0 opacity-100"
                      : "invisible -translate-y-1 opacity-0",
                  )}
                >
                  <div className="overflow-hidden rounded-2xl border border-border bg-popover p-2 shadow-lift">
                    {(services || []).map((s) => (
                      <Link
                        key={s.slug}
                        to={`/services/${s.slug}` as any}
                        onClick={() => setServicesOpen(false)}
                        className="block rounded-xl px-4 py-3 text-sm font-medium text-foreground/80 transition-colors hover:bg-accent hover:text-primary"
                      >
                        {s.name}
                      </Link>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <Link
                key={link.to}
                to={link.to}
                activeOptions={{ exact: link.to === "/" }}
                className="rounded-full px-4 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-accent hover:text-primary [&.active]:text-primary"
              >
                {t(link.key)}
              </Link>
            ),
          )}
        </nav>

        <div className="hidden items-center gap-4 lg:flex">
          <LanguageSwitcher />
          <CtaLink to="/contact" hash="devis">
            {t("home.hero.cta")}
          </CtaLink>
        </div>

        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          aria-label={open ? "Fermer le menu" : "Ouvrir le menu"}
          aria-expanded={open}
          className="grid h-11 w-11 place-items-center rounded-xl border border-border text-navy transition-colors hover:border-primary hover:text-primary lg:hidden"
        >
          {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      <div
        className={cn(
          "overflow-hidden border-t border-border bg-background transition-[max-height] duration-400 lg:hidden",
          open ? "max-h-[85vh] overflow-y-auto" : "max-h-0",
        )}
      >
        <nav className="container-esc space-y-1 py-6" aria-label="Navigation mobile">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
              activeOptions={{ exact: link.to === "/" }}
              className="block rounded-xl px-4 py-3 font-display text-lg font-semibold text-navy transition-colors hover:bg-accent hover:text-primary"
            >
              {t(link.key)}
            </Link>
          ))}
          <div className="mt-2 rounded-2xl bg-surface p-3">
            <p className="px-2 pb-2 text-xs font-semibold uppercase tracking-[0.18em] text-muted-foreground">
              Nos services
            </p>
            {(services || []).map((s) => (
              <Link
                key={s.slug}
                to={`/services/${s.slug}` as any}
                onClick={() => setOpen(false)}
                className="block rounded-xl px-2 py-2.5 text-sm font-medium text-foreground/80 transition-colors hover:text-primary"
              >
                {s.name}
              </Link>
            ))}
          </div>
          <CtaLink to="/contact" hash="devis" block className="mt-4" onClick={() => setOpen(false)}>
            Demander un devis
          </CtaLink>
        </nav>
      </div>
    </header>
  );
}
