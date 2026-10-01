/* ------------------------------------------------------------------ *
 *  ESC — Campagnes Maritimes data                                      *
 *  Swap placeholder data for real API/CMS values when available.       *
 * ------------------------------------------------------------------ */

export type CampaignStatus = "active" | "limited" | "upcoming" | "expired";

export interface MaritimeCampaign {
  id: string;
  title: string;
  title_en?: string;
  subtitle: string;
  subtitle_en?: string;
  route: { from: string; to: string };
  route_from?: string;
  route_to?: string;
  discount: string; // e.g. "–15%"
  description: string;
  description_en?: string;
  validUntil?: string; // ISO date string
  valid_until?: string;
  status: CampaignStatus;
  highlights?: string[];
  highlights_en?: string[];
  highlights_list?: string[];
}

export interface AssociatedCampaign {
  id: string;
  category: string; // e.g. "Logistique portuaire"
  category_en?: string;
  title: string;
  title_en?: string;
  description: string;
  description_en?: string;
  badge: string;
  badge_en?: string;
  status: CampaignStatus;
  validUntil?: string;
  valid_until?: string;
}

/* ── Maritime campaigns ─────────────────────────────────────────── */
export const maritimeCampaigns: MaritimeCampaign[] = [
  {
    id: "mc-01",
    title: "Offre Méditerranée Express",
    title_en: "Express Mediterranean Deal",
    subtitle: "Ligne Europe – Algérie",
    subtitle_en: "Europe – Algeria Line",
    route: { from: "Marseille / Gênes", to: "Alger / Béjaïa" },
    route_from: "Marseille / Genoa",
    route_to: "Algiers / Bejaia",
    discount: "–15 %",
    description:
      "Profitez d'un tarif préférentiel sur le fret conteneurisé FCL et LCL entre les ports méditerranéens et les principaux ports algériens. Idéal pour les importateurs réguliers.",
    description_en:
      "Enjoy preferential rates on containerized FCL and LCL freight between Mediterranean ports and main Algerian ports. Ideal for regular importers.",
    validUntil: "2026-12-31",
    valid_until: "2026-12-31",
    status: "active",
    highlights: [
      "FCL 20' et 40' inclus",
      "Délai garanti 5 à 7 jours",
      "Documentation prise en charge",
    ],
    highlights_en: [
      "20' and 40' FCL included",
      "Guaranteed 5 to 7 days lead time",
      "Full documentation handling included",
    ],
    highlights_list: [
      "FCL 20' et 40' inclus",
      "Délai garanti 5 à 7 jours",
      "Documentation prise en charge",
    ],
  },
  {
    id: "mc-02",
    title: "Pack Asie – Algérie Winter Deal",
    title_en: "Asia – Algeria Winter Pack",
    subtitle: "Ligne Asie – Maghreb",
    subtitle_en: "Asia – Maghreb Line",
    route: { from: "Shanghai / Guangzhou", to: "Oran / Alger" },
    route_from: "Shanghai / Guangzhou",
    route_to: "Oran / Algiers",
    discount: "–12 %",
    description:
      "Réduction saisonnière sur les expéditions FCL en provenance des grands ports chinois vers l'Algérie. Valable pour les bookings confirmés avant le 31 octobre.",
    description_en:
      "Seasonal discount on FCL shipments from major Chinese ports to Algeria. Valid for bookings confirmed before October 31.",
    validUntil: "2026-10-31",
    valid_until: "2026-10-31",
    status: "limited",
    highlights: [
      "Transbordement rapide à Tanger",
      "Suivi en temps réel",
      "Offre limitée aux 50 premiers bookings",
    ],
    highlights_en: [
      "Fast transshipment via Tangier",
      "Real-time tracking",
      "Offer limited to first 50 bookings",
    ],
    highlights_list: [
      "Transbordement rapide à Tanger",
      "Suivi en temps réel",
      "Offre limitée aux 50 premiers bookings",
    ],
  },
  {
    id: "mc-03",
    title: "Groupage Turquie Premium",
    title_en: "Premium Turkey LCL Groupage",
    subtitle: "Ligne Turquie – Algérie",
    subtitle_en: "Turkey – Algeria Line",
    route: { from: "Istanbul / Mersin", to: "Annaba / Skikda" },
    route_from: "Istanbul / Mersin",
    route_to: "Annaba / Skikda",
    discount: "–10 %",
    description:
      "Service LCL dédié avec départs hebdomadaires garantis depuis la Turquie. Regroupez vos marchandises avec d'autres chargeurs et réduisez vos coûts.",
    description_en:
      "Dedicated LCL service with guaranteed weekly departures from Turkey. Consolidate your cargo with other shippers and reduce shipping costs.",
    validUntil: "2026-11-30",
    valid_until: "2026-11-30",
    status: "active",
    highlights: [
      "Départs chaque lundi",
      "Min. 1 CBM accepté",
      "Consolidation professionnelle",
    ],
    highlights_en: [
      "Departures every Monday",
      "Min. 1 CBM accepted",
      "Professional cargo consolidation",
    ],
    highlights_list: [
      "Départs chaque lundi",
      "Min. 1 CBM accepté",
      "Consolidation professionnelle",
    ],
  },
  {
    id: "mc-04",
    title: "Ligne Amérique du Nord Q1 2027",
    title_en: "North America Line Q1 2027",
    subtitle: "Ligne USA / Canada – Algérie",
    subtitle_en: "USA / Canada – Algeria Line",
    route: { from: "New York / Houston", to: "Alger" },
    route_from: "New York / Houston",
    route_to: "Algiers",
    discount: "–8 %",
    description:
      "Lancement d'une nouvelle ligne directe Amérique du Nord — Algérie. Réservez dès maintenant à tarif early-bird et bénéficiez d'une priorité de chargement.",
    description_en:
      "Launch of a new direct North America — Algeria ocean line. Book now at early-bird rates and benefit from loading priority.",
    validUntil: "2027-03-31",
    valid_until: "2027-03-31",
    status: "upcoming",
    highlights: [
      "Tarif early-bird garanti",
      "Priorité de chargement",
      "Accompagnement douanier inclus",
    ],
    highlights_en: [
      "Guaranteed early-bird rate",
      "Priority loading",
      "Customs assistance included",
    ],
    highlights_list: [
      "Tarif early-bird garanti",
      "Priorité de chargement",
      "Accompagnement douanier inclus",
    ],
  },
];

/* ── Associated campaigns ───────────────────────────────────────── */
export const associatedCampaigns: AssociatedCampaign[] = [
  {
    id: "ac-01",
    category: "Logistique portuaire",
    category_en: "Port Logistics",
    title: "Pack Port Intégré",
    title_en: "Integrated Port Package",
    description:
      "Combinaison transport maritime + manutention portuaire + entreposage court terme à tarif négocié. Idéal pour les opérations d'import régulières.",
    description_en:
      "Combination of ocean freight + port handling + short-term warehousing at negotiated rates. Ideal for regular import operations.",
    badge: "Bundle",
    badge_en: "Bundle",
    status: "active",
    validUntil: "2026-12-31",
    valid_until: "2026-12-31",
  },
  {
    id: "ac-02",
    category: "Dédouanement",
    category_en: "Customs Clearance",
    title: "Clearance Express",
    title_en: "Clearance Express",
    description:
      "Prise en charge prioritaire de vos déclarations douanières dans un délai de 48 h. Inclut la constitution du dossier et le suivi jusqu'à la mainlevée.",
    description_en:
      "Priority processing of your customs declarations within 48 hours. Includes file setup and tracking through release.",
    badge: "Offre rapide",
    badge_en: "Fast Track",
    status: "active",
    validUntil: "2026-11-30",
    valid_until: "2026-11-30",
  },
  {
    id: "ac-03",
    category: "Assurance cargo",
    category_en: "Cargo Insurance",
    title: "Couverture Tous Risques Maritime",
    title_en: "All-Risk Marine Cover",
    description:
      "Assurance tous risques pour vos conteneurs FCL et LCL. Tarif préférentiel négocié avec nos partenaires assureurs pour les expéditions maritimes.",
    description_en:
      "All-risk insurance for your FCL and LCL containers. Preferential rates negotiated with our insurance partners for sea freight.",
    badge: "Recommandé",
    badge_en: "Recommended",
    status: "limited",
    validUntil: "2026-10-31",
    valid_until: "2026-10-31",
  },
  {
    id: "ac-04",
    category: "Entreposage",
    category_en: "Warehousing",
    title: "Stockage Tampon 30 Jours Offerts",
    title_en: "30 Days Free Buffer Storage",
    description:
      "Premier mois d'entreposage offert pour tout contrat de transport maritime signé dans le cadre d'une campagne active ESC.",
    description_en:
      "First month of warehousing free for any sea freight contract signed under an active ESC campaign.",
    badge: "Nouveau",
    badge_en: "New",
    status: "upcoming",
    validUntil: "2027-01-31",
    valid_until: "2027-01-31",
  },
  {
    id: "ac-05",
    category: "Transport routier",
    category_en: "Road Freight",
    title: "Pré/Post Acheminement Inclus",
    title_en: "Free Pre/Post Drayage",
    description:
      "Enlèvement ou livraison porte-à-port offert sur les 200 premiers km pour toute réservation maritime confirmée via ESC.",
    description_en:
      "Door-to-port pickup or delivery free for the first 200 km on any sea freight booking confirmed with ESC.",
    badge: "Exclusif",
    badge_en: "Exclusive",
    status: "active",
    validUntil: "2026-12-15",
    valid_until: "2026-12-15",
  },
];

/* ── Helpers ────────────────────────────────────────────────────── */
export const statusMeta: Record<
  CampaignStatus,
  { label: string; color: string; dot: string }
> = {
  active:   { label: "Active",          color: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400",  dot: "bg-emerald-500" },
  limited:  { label: "Offre limitée",   color: "bg-amber-100  text-amber-700  dark:bg-amber-900/40  dark:text-amber-400",   dot: "bg-amber-500"   },
  upcoming: { label: "À venir",         color: "bg-blue-100   text-blue-700   dark:bg-blue-900/40   dark:text-blue-400",    dot: "bg-blue-500"    },
  expired:  { label: "Expirée",         color: "bg-gray-100   text-gray-500   dark:bg-gray-800      dark:text-gray-400",    dot: "bg-gray-400"    },
};
