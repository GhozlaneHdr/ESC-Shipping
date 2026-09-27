import maritime from "@/assets/svc-maritime.jpg";
import aerien from "@/assets/svc-aerien.jpg";
import routier from "@/assets/svc-routier.jpg";
import entreposage from "@/assets/svc-entreposage.jpg";
import dedouanement from "@/assets/svc-dedouanement.jpg";
import agent from "@/assets/svc-agent.jpg";
import port from "@/assets/hero-port.jpg";

export const contact = {
  phones: ["+213 555 50 86 21", "+213 555 50 86 20", "+213 555 50 86 19"],
  emails: ["contact@ex-shipping.com", "sales@ex-shipping.com"],
  facebook: "https://www.facebook.com/people/Express-Shipping-Company/100063539442443/",
  hours: [
    { days: "Dimanche – Jeudi", time: "08:00 – 17:00" },
    { days: "Vendredi – Samedi", time: "Fermé" },
  ],
};

export const offices = [
  {
    name: "ESC — SÉTIF",
    address: "Cité 326 logts ZHUN, Bâtiment A06, Local n°24, Sétif",
    phones: ["+213 36 54 74 41", "+213 555 50 86 21", "+213 555 50 86 20", "+213 555 50 86 19"],
    map: "https://www.google.com/maps?q=Setif%2C%20Alg%C3%A9rie&output=embed",
  },
  {
    name: "ESC — ALGER",
    address: "1 Rue Mohamed Belouizdad, Sidi M'Hamed, Alger",
    phones: ["+213 28 13 37 70", "+213 555 57 24 40"],
    map: "https://www.google.com/maps?q=1%20Rue%20Mohamed%20Belouizdad%2C%20Sidi%20M'Hamed%2C%20Alger&output=embed",
  },
];

export type Service = {
  slug: string;
  path: string;
  name: string;
  short: string;
  image: string;
  intro: string;
  benefits: string[];
  steps: { title: string; text: string }[];
  why: string[];
};

export const services: Service[] = [
  {
    slug: "transport-maritime",
    path: "/services/transport-maritime",
    name: "Transport maritime",
    short:
      "Acheminement de vos marchandises par voie maritime, en conteneur complet ou en groupage, sur les principales lignes internationales.",
    image: maritime,
    intro:
      "Le transport maritime constitue le cœur de notre activité de transitaire. ESC organise l'acheminement de vos marchandises depuis et vers l'Algérie, en coordination avec les compagnies maritimes et les opérateurs portuaires.",
    benefits: [
      "Expéditions en conteneur complet (FCL) et en groupage (LCL)",
      "Coordination avec les compagnies maritimes et les terminaux portuaires",
      "Suivi documentaire complet de l'expédition",
      "Solution adaptée aux volumes importants à l'import comme à l'export",
    ],
    steps: [
      { title: "Analyse du besoin", text: "Nous étudions la nature, le volume et la destination de votre marchandise." },
      { title: "Cotation et réservation", text: "Nous vous proposons une cotation, puis réservons l'espace auprès de la compagnie." },
      { title: "Préparation documentaire", text: "Nous préparons et contrôlons l'ensemble des documents d'expédition." },
      { title: "Acheminement et livraison", text: "Nous suivons l'expédition jusqu'à la mise à disposition de la marchandise." },
    ],
    why: [
      "Une équipe basée en Algérie qui connaît les procédures locales",
      "Un interlocuteur unique pour l'ensemble de votre dossier",
      "Un réseau de partenaires internationaux",
    ],
  },
  {
    slug: "entreposage",
    path: "/services/entreposage",
    name: "Entreposage",
    short:
      "Stockage, entrepôt sous douane, réception et expédition de vos marchandises avec contrôle et gestion des formalités.",
    image: entreposage,
    intro:
      "ESC met à disposition des solutions de stockage pour vos marchandises, y compris l'entreposage sous douane, avec la réception, le contrôle et l'expédition des produits ainsi que la gestion des formalités associées.",
    benefits: [
      "Installations de stockage pour vos marchandises",
      "Entreposage sous douane",
      "Réception et expédition des marchandises",
      "Contrôle des produits et gestion des formalités",
    ],
    steps: [
      { title: "Réception", text: "Réception de la marchandise et contrôle à l'arrivée." },
      { title: "Stockage", text: "Mise en stock dans nos installations, y compris sous régime douanier." },
      { title: "Gestion", text: "Suivi des produits stockés et gestion des formalités." },
      { title: "Expédition", text: "Préparation et expédition selon vos instructions." },
    ],
    why: [
      "Une gestion des formalités prise en charge de bout en bout",
      "Un suivi rigoureux des marchandises stockées",
      "Une solution combinable avec nos services de transport",
    ],
  },
  {
    slug: "agent-de-fret",
    path: "/services/agent-de-fret",
    name: "Agent de fret",
    short:
      "Organisation complète de vos opérations de fret : choix des modes de transport, documentation et coordination des intervenants.",
    image: port,
    intro:
      "En tant qu'agent de fret, ESC organise et coordonne vos expéditions de bout en bout : sélection des modes de transport, relation avec les compagnies et les prestataires, et suivi documentaire de vos opérations d'import-export.",
    benefits: [
      "Organisation multimodale de vos expéditions",
      "Coordination des différents intervenants de la chaîne",
      "Préparation et contrôle des documents de transport",
      "Accompagnement personnalisé de vos opérations",
    ],
    steps: [
      { title: "Cadrage", text: "Nous définissons avec vous le schéma logistique adapté." },
      { title: "Organisation", text: "Nous réservons et coordonnons les différents maillons du transport." },
      { title: "Documentation", text: "Nous établissons et vérifions les documents nécessaires." },
      { title: "Suivi", text: "Nous assurons le suivi jusqu'à la livraison finale." },
    ],
    why: [
      "Un interlocuteur unique pour toute la chaîne logistique",
      "Une expérience confirmée de l'import-export en Algérie",
      "Un service personnalisé pour chaque client",
    ],
  },
  {
    slug: "agent-maritime",
    path: "/services/agent-maritime",
    name: "Agent maritime",
    short:
      "Représentation et assistance des navires à l'escale : formalités portuaires, coordination des opérations et relation avec les autorités.",
    image: agent,
    intro:
      "ESC assure la représentation des armateurs et l'assistance des navires lors de leurs escales : accomplissement des formalités portuaires, coordination des opérations à quai et relation avec les autorités et les prestataires locaux.",
    benefits: [
      "Assistance du navire pendant l'escale",
      "Accomplissement des formalités portuaires",
      "Coordination des opérations de manutention",
      "Interface avec les autorités portuaires locales",
    ],
    steps: [
      { title: "Annonce d'escale", text: "Préparation de l'escale et information des parties prenantes." },
      { title: "Formalités", text: "Traitement des formalités administratives et portuaires." },
      { title: "Opérations", text: "Coordination des opérations commerciales du navire." },
      { title: "Clôture", text: "Suivi post-escale et transmission des documents." },
    ],
    why: [
      "Une présence locale en Algérie",
      "Une bonne connaissance des procédures portuaires",
      "Une réactivité adaptée aux contraintes d'escale",
    ],
  },
  {
    slug: "dedouanement",
    path: "/services/dedouanement",
    name: "Dédouanement",
    short:
      "Prise en charge des formalités douanières à l'import et à l'export, avec préparation et suivi des déclarations.",
    image: dedouanement,
    intro:
      "ESC prend en charge les formalités de dédouanement de vos marchandises à l'import comme à l'export : constitution des dossiers, déclarations et suivi des opérations auprès des services douaniers.",
    benefits: [
      "Formalités douanières import et export",
      "Constitution et contrôle des dossiers",
      "Suivi des déclarations jusqu'à la mainlevée",
      "Conseil sur les documents requis",
    ],
    steps: [
      { title: "Collecte des documents", text: "Nous réunissons les pièces nécessaires au dossier." },
      { title: "Déclaration", text: "Nous établissons la déclaration en douane." },
      { title: "Suivi", text: "Nous suivons le traitement du dossier auprès des services concernés." },
      { title: "Mise à disposition", text: "Nous organisons l'enlèvement de la marchandise après mainlevée." },
    ],
    why: [
      "Une maîtrise des procédures douanières algériennes",
      "Un traitement rigoureux des dossiers",
      "Une coordination directe avec vos opérations de transport",
    ],
  },
  {
    slug: "transport-aerien",
    path: "/services/transport-aerien",
    name: "Transport aérien",
    short:
      "Solutions de fret aérien pour vos envois urgents ou à forte valeur, vers et depuis l'Algérie.",
    image: aerien,
    intro:
      "Le fret aérien répond aux besoins d'expéditions rapides. ESC organise l'acheminement de vos marchandises par voie aérienne, avec la préparation documentaire et la coordination des opérations au départ comme à l'arrivée.",
    benefits: [
      "Délais d'acheminement réduits",
      "Adapté aux envois urgents et à forte valeur",
      "Préparation complète des documents de transport aérien",
      "Coordination au départ et à l'arrivée",
    ],
    steps: [
      { title: "Demande", text: "Vous nous transmettez les caractéristiques de votre envoi." },
      { title: "Cotation", text: "Nous proposons une solution et un délai adaptés." },
      { title: "Expédition", text: "Nous organisons l'enlèvement et le départ de la marchandise." },
      { title: "Livraison", text: "Nous suivons l'envoi jusqu'à sa mise à disposition." },
    ],
    why: [
      "Une réactivité adaptée aux expéditions urgentes",
      "Un suivi assuré par un interlocuteur dédié",
      "Une complémentarité avec nos autres modes de transport",
    ],
  },
  {
    slug: "transport-routier",
    path: "/services/transport-routier",
    name: "Transport routier",
    short:
      "Transport en charge complète (FTL) ou groupage (LTL), avec suivi en temps réel et livraison dans les délais.",
    image: routier,
    intro:
      "ESC organise le transport routier de vos marchandises en charge complète (FTL) ou en groupage (LTL), avec une couverture assurée par notre flotte et notre réseau de partenaires, un suivi en temps réel et une attention particulière portée à la sécurité des marchandises.",
    benefits: [
      "Transport en charge complète (FTL) et en groupage (LTL)",
      "Couverture assurée par la flotte et le réseau de partenaires",
      "Suivi en temps réel des expéditions",
      "Sécurité des marchandises et respect des délais",
    ],
    steps: [
      { title: "Planification", text: "Nous définissons l'itinéraire et le type de chargement." },
      { title: "Enlèvement", text: "Nous organisons le chargement au point de départ." },
      { title: "Acheminement", text: "Nous assurons le transport avec suivi de l'expédition." },
      { title: "Livraison", text: "Nous livrons la marchandise à destination dans les délais convenus." },
    ],
    why: [
      "Une couverture nationale par la route",
      "Un suivi en temps réel de vos expéditions",
      "Une solution facilement combinable avec le maritime et l'aérien",
    ],
  },
];

export const serviceBySlug = (slug: string) => services.find((s) => s.slug === slug)!;

export const stats = [
  { value: 10, suffix: "+", label: "Années d'expérience" },
  { value: 300, suffix: "+", label: "Clients accompagnés" },
  { value: 40, suffix: "+", label: "Partenaires internationaux" },
];
