/* ------------------------------------------------------------------ *
 *  ESC — Campagnes Maritimes data                                      *
 *  Swap placeholder data for real API/CMS values when available.       *
 * ------------------------------------------------------------------ */

export type CampaignStatus = "active" | "limited" | "upcoming" | "expired";

export interface MaritimeCampaign {
  id: string;
  title: string;
  subtitle: string;
  route: { from: string; to: string };
  discount: string; // e.g. "–15%"
  description: string;
  validUntil: string; // ISO date string
  status: CampaignStatus;
  highlights: string[];
}

export interface AssociatedCampaign {
  id: string;
  category: string; // e.g. "Logistique portuaire"
  title: string;
  description: string;
  badge: string;
  status: CampaignStatus;
  validUntil: string;
}

/* ── Maritime campaigns ─────────────────────────────────────────── */
export const maritimeCampaigns: MaritimeCampaign[] = [
  {
    id: "mc-01",
    title: "Offre Méditerranée Express",
    subtitle: "Ligne Europe – Algérie",
    route: { from: "Marseille / Gênes", to: "Alger / Béjaïa" },
    discount: "–15 %",
    description:
      "Profitez d'un tarif préférentiel sur le fret conteneurisé FCL et LCL entre les ports méditerranéens et les principaux ports algériens. Idéal pour les importateurs réguliers.",
    validUntil: "2026-12-31",
    status: "active",
    highlights: [
      "FCL 20' et 40' inclus",
      "Délai garanti 5 à 7 jours",
      "Documentation prise en charge",
    ],
  },
  {
    id: "mc-02",
    title: "Pack Asie – Algérie Winter Deal",
    subtitle: "Ligne Asie – Maghreb",
    route: { from: "Shanghai / Guangzhou", to: "Oran / Alger" },
    discount: "–12 %",
    description:
      "Réduction saisonnière sur les expéditions FCL en provenance des grands ports chinois vers l'Algérie. Valable pour les bookings confirmés avant le 31 octobre.",
    validUntil: "2026-10-31",
    status: "limited",
    highlights: [
      "Transbordement rapide à Tanger",
      "Suivi en temps réel",
      "Offre limitée aux 50 premiers bookings",
    ],
  },
  {
    id: "mc-03",
    title: "Groupage Turquie Premium",
    subtitle: "Ligne Turquie – Algérie",
    route: { from: "Istanbul / Mersin", to: "Annaba / Skikda" },
    discount: "–10 %",
    description:
      "Service LCL dédié avec départs hebdomadaires garantis depuis la Turquie. Regroupez vos marchandises avec d'autres chargeurs et réduisez vos coûts.",
    validUntil: "2026-11-30",
    status: "active",
    highlights: [
      "Départs chaque lundi",
      "Min. 1 CBM accepté",
      "Consolidation professionnelle",
    ],
  },
  {
    id: "mc-04",
    title: "Ligne Amérique du Nord Q1 2027",
    subtitle: "Ligne USA / Canada – Algérie",
    route: { from: "New York / Houston", to: "Alger" },
    discount: "–8 %",
    description:
      "Lancement d'une nouvelle ligne directe Amérique du Nord — Algérie. Réservez dès maintenant à tarif early-bird et bénéficiez d'une priorité de chargement.",
    validUntil: "2027-03-31",
    status: "upcoming",
    highlights: [
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
    title: "Pack Port Intégré",
    description:
      "Combinaison transport maritime + manutention portuaire + entreposage court terme à tarif négocié. Idéal pour les opérations d'import régulières.",
    badge: "Bundle",
    status: "active",
    validUntil: "2026-12-31",
  },
  {
    id: "ac-02",
    category: "Dédouanement",
    title: "Clearance Express",
    description:
      "Prise en charge prioritaire de vos déclarations douanières dans un délai de 48 h. Inclut la constitution du dossier et le suivi jusqu'à la mainlevée.",
    badge: "Offre rapide",
    status: "active",
    validUntil: "2026-11-30",
  },
  {
    id: "ac-03",
    category: "Assurance cargo",
    title: "Couverture Tous Risques Maritime",
    description:
      "Assurance tous risques pour vos conteneurs FCL et LCL. Tarif préférentiel négocié avec nos partenaires assureurs pour les expéditions maritimes.",
    badge: "Recommandé",
    status: "limited",
    validUntil: "2026-10-31",
  },
  {
    id: "ac-04",
    category: "Entreposage",
    title: "Stockage Tampon 30 Jours Offerts",
    description:
      "Premier mois d'entreposage offert pour tout contrat de transport maritime signé dans le cadre d'une campagne active ESC.",
    badge: "Nouveau",
    status: "upcoming",
    validUntil: "2027-01-31",
  },
  {
    id: "ac-05",
    category: "Transport routier",
    title: "Pré/Post Acheminement Inclus",
    description:
      "Enlèvement ou livraison porte-à-port offert sur les 200 premiers km pour toute réservation maritime confirmée via ESC.",
    badge: "Exclusif",
    status: "active",
    validUntil: "2026-12-15",
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
