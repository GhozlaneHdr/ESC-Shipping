/**
 * Internationalization (i18n) system for ESC Shipping.
 * Supports French (default) and English.
 */

import { createContext, useContext, useState, useCallback, type ReactNode } from "react";

export type Locale = "fr" | "en";

interface I18nContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: string) => string;
}

const I18nContext = createContext<I18nContextType | null>(null);

const translations: Record<Locale, Record<string, string>> = {
  fr: {
    // Navigation
    "nav.home": "Accueil",
    "nav.about": "À propos",
    "nav.services": "Services",
    "nav.resources": "Ressources",
    "nav.campaigns": "Campagnes",
    "nav.contact": "Contact",

    // Common
    "common.loading": "Chargement...",
    "common.error": "Une erreur est survenue.",
    "common.submit": "Envoyer",
    "common.cancel": "Annuler",
    "common.save": "Enregistrer",
    "common.delete": "Supprimer",
    "common.edit": "Modifier",
    "common.search": "Rechercher",
    "common.close": "Fermer",
    "common.back": "Retour",
    "common.next": "Suivant",
    "common.previous": "Précédent",
    "common.viewAll": "Voir tout",
    "common.learnMore": "En savoir plus",

    // Home page
    "home.hero.eyebrow": "Transitaire & commissionnaire en Algérie",
    "home.hero.title": "Vos marchandises, acheminées en toute confiance.",
    "home.hero.subtitle": "Maritime, aérien, routier, dédouanement et entreposage : ESC coordonne l'ensemble de vos opérations d'import-export.",
    "home.hero.cta": "Demander un devis",
    "home.hero.phone": "Nous appeler",

    "home.stats.experience": "Années d'expérience",
    "home.stats.clients": "Clients accompagnés",
    "home.stats.partners": "Partenaires internationaux",

    "home.services.eyebrow": "Nos services",
    "home.services.title": "Une offre logistique complète",
    "home.services.subtitle": "Sept métiers complémentaires pour accompagner vos flux de bout en bout.",

    "home.why.eyebrow": "Pourquoi ESC",
    "home.why.title": "Un partenaire local, un réseau international",
    "home.why.1": "Équipes basées à Sétif et à Alger",
    "home.why.2": "Un interlocuteur unique pour tout votre dossier",
    "home.why.3": "Maîtrise des procédures douanières et portuaires algériennes",
    "home.why.4": "Réseau de partenaires dans le monde entier",

    "home.offices.eyebrow": "Nos implantations",
    "home.offices.title": "Deux bureaux, un même engagement",
    "home.offices.subtitle": "À Sétif comme à Alger, nos équipes sont proches de vos opérations pour vous accompagner avec réactivité.",
    "home.offices.cta": "Voir nos coordonnées",

    "home.cta.title": "Un projet d'expédition ?",
    "home.cta.subtitle": "Parlez-nous de votre besoin, nous revenons vers vous rapidement avec une solution adaptée.",
    "home.cta.button": "Demander un devis",

    // Services page
    "services.hero.eyebrow": "Services",
    "services.hero.title": "Nos services logistiques",
    "services.hero.subtitle": "Une offre complète pour organiser, sécuriser et accélérer vos expéditions.",

    // Campaigns page
    "campaigns.hero.eyebrow": "Promotions & Offres spéciales",
    "campaigns.hero.title": "Campagnes Maritimes",
    "campaigns.hero.subtitle": "Des réductions exclusives sur nos principales lignes maritimes — Europe, Asie, Turquie et Amériques — pour optimiser vos coûts d'import-export.",
    "campaigns.hero.cta1": "Demander un devis",
    "campaigns.hero.cta2": "Nous contacter",

    "campaigns.maritime.eyebrow": "Campagnes maritimes",
    "campaigns.maritime.title": "Nos offres sur les lignes maritimes",
    "campaigns.maritime.subtitle": "Bénéficiez de tarifs préférentiels sur les principales liaisons maritimes desservant l'Algérie.",

    "campaigns.associated.eyebrow": "Campagnes associées",
    "campaigns.associated.title": "Offres complémentaires",
    "campaigns.associated.subtitle": "Maximisez la valeur de vos expéditions maritimes avec nos packs logistiques, douaniers et d'assurance associés.",

    "campaigns.cta.title": "Une expédition à planifier ?",
    "campaigns.cta.subtitle": "Contactez-nous pour bénéficier de l'une de nos campagnes ou obtenir une offre personnalisée.",
    "campaigns.cta.button1": "Demander un devis",
    "campaigns.cta.button2": "Voir nos services maritimes",

    // Campaign statuses
    "campaign.status.active": "Active",
    "campaign.status.limited": "Offre limitée",
    "campaign.status.upcoming": "À venir",
    "campaign.status.expired": "Expirée",

    // Contact page
    "contact.hero.eyebrow": "Contact",
    "contact.hero.title": "Parlons de votre projet",
    "contact.hero.subtitle": "Demandez un devis ou posez-nous vos questions : notre équipe vous répond rapidement.",

    "contact.phone": "Téléphone",
    "contact.email": "E-mail",
    "contact.hours": "Horaires",
    "contact.offices.eyebrow": "Nos bureaux",
    "contact.offices.title": "Sétif & Alger",

    // Quote form
    "quote.title": "Demandez votre devis",
    "quote.subtitle": "Décrivez votre besoin, nous revenons vers vous avec une proposition adaptée.",
    "quote.name": "Nom complet *",
    "quote.name.placeholder": "Votre nom",
    "quote.company": "Entreprise",
    "quote.company.placeholder": "Nom de votre société",
    "quote.email": "Email *",
    "quote.email.placeholder": "vous@entreprise.com",
    "quote.phone": "Téléphone *",
    "quote.phone.placeholder": "+213 ...",
    "quote.service": "Type de service *",
    "quote.service.placeholder": "Sélectionnez un service",
    "quote.service.other": "Autre / plusieurs services",
    "quote.departure": "Ville / Pays de départ *",
    "quote.departure.placeholder": "Ex. Alger, Algérie",
    "quote.destination": "Ville / Pays de destination *",
    "quote.destination.placeholder": "Ex. Marseille, France",
    "quote.message": "Message",
    "quote.message.placeholder": "Nature de la marchandise, volume, délais souhaités...",
    "quote.submit": "Envoyer ma demande",
    "quote.submitting": "Envoi en cours...",
    "quote.success": "Demande enregistrée",
    "quote.success.message": "Merci {name}. Notre équipe vous recontacte rapidement.",
    "quote.error": "Erreur",
    "quote.error.message": "Impossible d'envoyer votre demande. Veuillez réessayer.",
    "quote.contact": "Vous pouvez aussi nous écrire à contact@ex-shipping.com",

    // Footer
    "footer.tagline": "Express Shipping Company — Votre partenaire logistique pour des solutions de fret fiables, rapides et sécurisées.",
    "footer.navigation": "Navigation",
    "footer.services": "Services",
    "footer.contact": "Contact",
    "footer.copyright": "© 2026 ESC — Express Shipping Company. Tous droits réservés.",
    "footer.credit": "Designed & Developed by IntellectSoft — Zetoutou Faycal",
    "footer.location": "Transitaire & commissionnaire — Sétif · Alger",

    // Campaign buttons & cards
    "campaign.claim": "Profiter de l'offre",
    "campaign.notify": "Me notifier",
    "campaign.details": "Voir les détails",
    "campaign.learnMore": "En savoir plus",
    "campaign.validUntil": "Valide jusqu'au",
    "campaign.legend": "Légende :",

    // Campaign Modal
    "modal.close": "Fermer",
    "modal.included": "Inclus dans cette offre :",
    "modal.requestQuote": "Demander un devis pour cette offre",
    "modal.validUntil": "Offre valide jusqu'au",

    // Partners
    "partners.eyebrow": "Lignes maritimes partenaires",
    "partners.title": "Les compagnies qui acheminent vos marchandises",
  },
  en: {
    // Navigation
    "nav.home": "Home",
    "nav.about": "About",
    "nav.services": "Services",
    "nav.resources": "Resources",
    "nav.campaigns": "Campaigns",
    "nav.contact": "Contact",

    // Common
    "common.loading": "Loading...",
    "common.error": "An error occurred.",
    "common.submit": "Submit",
    "common.cancel": "Cancel",
    "common.save": "Save",
    "common.delete": "Delete",
    "common.edit": "Edit",
    "common.search": "Search",
    "common.close": "Close",
    "common.back": "Back",
    "common.next": "Next",
    "common.previous": "Previous",
    "common.viewAll": "View all",
    "common.learnMore": "Learn more",

    // Home page
    "home.hero.eyebrow": "Freight Forwarder & Customs Broker in Algeria",
    "home.hero.title": "Your goods, delivered with confidence.",
    "home.hero.subtitle": "Sea, air, road, customs clearance and warehousing: ESC coordinates all your import-export operations.",
    "home.hero.cta": "Request a quote",
    "home.hero.phone": "Call us",

    "home.stats.experience": "Years of experience",
    "home.stats.clients": "Clients supported",
    "home.stats.partners": "International partners",

    "home.services.eyebrow": "Our services",
    "home.services.title": "A complete logistics offering",
    "home.services.subtitle": "Seven complementary services to support your flows end-to-end.",

    "home.why.eyebrow": "Why ESC",
    "home.why.title": "A local partner, an international network",
    "home.why.1": "Teams based in Setif and Algiers",
    "home.why.2": "A single contact for your entire file",
    "home.why.3": "Expertise in Algerian customs and port procedures",
    "home.why.4": "Network of partners worldwide",

    "home.offices.eyebrow": "Our locations",
    "home.offices.title": "Two offices, one commitment",
    "home.offices.subtitle": "From Setif to Algiers, our teams stay close to your operations and ready to support you.",
    "home.offices.cta": "View contact details",

    "home.cta.title": "A shipment to plan?",
    "home.cta.subtitle": "Tell us about your needs, we'll get back to you quickly with a tailored solution.",
    "home.cta.button": "Request a quote",

    // Services page
    "services.hero.eyebrow": "Services",
    "services.hero.title": "Our logistics services",
    "services.hero.subtitle": "A complete offering to organize, secure and accelerate your shipments.",

    // Campaigns page
    "campaigns.hero.eyebrow": "Promotions & Special Offers",
    "campaigns.hero.title": "Maritime Campaigns",
    "campaigns.hero.subtitle": "Exclusive discounts on our main maritime lines — Europe, Asia, Turkey and the Americas — to optimize your import-export costs.",
    "campaigns.hero.cta1": "Request a quote",
    "campaigns.hero.cta2": "Contact us",

    "campaigns.maritime.eyebrow": "Maritime campaigns",
    "campaigns.maritime.title": "Our offers on maritime lines",
    "campaigns.maritime.subtitle": "Benefit from preferential rates on the main maritime routes serving Algeria.",

    "campaigns.associated.eyebrow": "Associated campaigns",
    "campaigns.associated.title": "Complementary offers",
    "campaigns.associated.subtitle": "Maximize the value of your maritime shipments with our associated logistics, customs and insurance packages.",

    "campaigns.cta.title": "A shipment to plan?",
    "campaigns.cta.subtitle": "Contact us to benefit from one of our campaigns or get a personalized offer.",
    "campaigns.cta.button1": "Request a quote",
    "campaigns.cta.button2": "View our maritime services",

    // Campaign statuses
    "campaign.status.active": "Active",
    "campaign.status.limited": "Limited offer",
    "campaign.status.upcoming": "Upcoming",
    "campaign.status.expired": "Expired",

    // Contact page
    "contact.hero.eyebrow": "Contact",
    "contact.hero.title": "Let's talk about your project",
    "contact.hero.subtitle": "Request a quote or ask us your questions: our team will respond quickly.",

    "contact.phone": "Phone",
    "contact.email": "Email",
    "contact.hours": "Hours",
    "contact.offices.eyebrow": "Our offices",
    "contact.offices.title": "Setif & Algiers",

    // Quote form
    "quote.title": "Request your quote",
    "quote.subtitle": "Describe your needs, we'll get back to you with a tailored proposal.",
    "quote.name": "Full name *",
    "quote.name.placeholder": "Your name",
    "quote.company": "Company",
    "quote.company.placeholder": "Your company name",
    "quote.email": "Email *",
    "quote.email.placeholder": "you@company.com",
    "quote.phone": "Phone *",
    "quote.phone.placeholder": "+213 ...",
    "quote.service": "Service type *",
    "quote.service.placeholder": "Select a service",
    "quote.service.other": "Other / multiple services",
    "quote.departure": "Departure city / country *",
    "quote.departure.placeholder": "e.g. Algiers, Algeria",
    "quote.destination": "Destination city / country *",
    "quote.destination.placeholder": "e.g. Marseille, France",
    "quote.message": "Message",
    "quote.message.placeholder": "Nature of goods, volume, desired deadlines...",
    "quote.submit": "Send my request",
    "quote.submitting": "Sending...",
    "quote.success": "Request saved",
    "quote.success.message": "Thank you {name}. Our team will contact you shortly.",
    "quote.error": "Error",
    "quote.error.message": "Unable to send your request. Please try again.",
    "quote.contact": "You can also write to us at contact@ex-shipping.com",

    // Footer
    "footer.tagline": "Express Shipping Company — Your logistics partner for reliable, fast and secure freight solutions.",
    "footer.navigation": "Navigation",
    "footer.services": "Services",
    "footer.contact": "Contact",
    "footer.copyright": "© 2026 ESC — Express Shipping Company. All rights reserved.",
    "footer.credit": "Designed & Developed by IntellectSoft — Zetoutou Faycal",
    "footer.location": "Freight forwarder & customs broker — Setif · Algiers",

    // Campaign buttons & cards
    "campaign.claim": "Claim offer",
    "campaign.notify": "Notify me",
    "campaign.details": "View details",
    "campaign.learnMore": "Learn more",
    "campaign.validUntil": "Valid until",
    "campaign.legend": "Legend:",

    // Campaign Modal
    "modal.close": "Close",
    "modal.included": "Included in this offer:",
    "modal.requestQuote": "Request a quote for this offer",
    "modal.validUntil": "Offer valid until",

    // Partners
    "partners.eyebrow": "Maritime line partners",
    "partners.title": "The carriers moving your goods",
  },
};

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("fr");

  const setLocale = useCallback((newLocale: Locale) => {
    setLocaleState(newLocale);
    localStorage.setItem("esc-locale", newLocale);
  }, []);

  const t = useCallback(
    (key: string): string => {
      return translations[locale][key] || key;
    },
    [locale]
  );

  return (
    <I18nContext.Provider value={{ locale, setLocale, t }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error("useI18n must be used within an I18nProvider");
  }
  return context;
}
