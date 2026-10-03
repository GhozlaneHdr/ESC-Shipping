"""
Seed the database with front-end mock data.

This command populates the database with all static data from the
front-end codebase (services, campaigns, stats, partners) and creates
default user accounts for testing.

Usage:
    python manage.py seed_data
    python manage.py seed_data --flush  # Clear existing data first
"""

import os
import shutil
from urllib.request import Request, urlopen
from pathlib import Path

from io import BytesIO
from PIL import Image

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cms.models import (
    AssociatedCampaign,
    MaritimeCampaign,
    Service,
    ServiceStep,
    SiteBranding,
    Stat,
    TrustedPartner,
    ResourceItem,
)
from apps.users.models import User, UserProfile, UserRole


# =============================================================================
# DATA EXTRACTED FROM FRONT-END
# =============================================================================

SERVICES = [
    {
        "slug": "transport-maritime",
        "name": "Transport maritime",
        "short_description": "Acheminement de vos marchandises par voie maritime, en conteneur complet ou en groupage, sur les principales lignes internationales.",
        "long_intro": "Le transport maritime constitue le cœur de notre activité de transitaire. ESC organise l'acheminement de vos marchandises depuis et vers l'Algérie, en coordination avec les compagnies maritimes et les opérateurs portuaires.",
        "image": "svc-maritime.jpg",
        "benefits": [
            "Expéditions en conteneur complet (FCL) et en groupage (LCL)",
            "Coordination avec les compagnies maritimes et les terminaux portuaires",
            "Suivi documentaire complet de l'expédition",
            "Solution adaptée aux volumes importants à l'import comme à l'export",
        ],
        "steps": [
            {"title": "Analyse du besoin", "text": "Nous étudions la nature, le volume et la destination de votre marchandise."},
            {"title": "Cotation et réservation", "text": "Nous vous proposons une cotation, puis réservons l'espace auprès de la compagnie."},
            {"title": "Préparation documentaire", "text": "Nous préparons et contrôlons l'ensemble des documents d'expédition."},
            {"title": "Acheminement et livraison", "text": "Nous suivons l'expédition jusqu'à la mise à disposition de la marchandise."},
        ],
        "why_us": [
            "Une équipe basée en Algérie qui connaît les procédures locales",
            "Un interlocuteur unique pour l'ensemble de votre dossier",
            "Un réseau de partenaires internationaux",
        ],
    },
    {
        "slug": "entreposage",
        "name": "Entreposage",
        "short_description": "Stockage, entrepôt sous douane, réception et expédition de vos marchandises avec contrôle et gestion des formalités.",
        "long_intro": "ESC met à disposition des solutions de stockage pour vos marchandises, y compris l'entreposage sous douane, avec la réception, le contrôle et l'expédition des produits ainsi que la gestion des formalités associées.",
        "image": "svc-entreposage.jpg",
        "benefits": [
            "Installations de stockage pour vos marchandises",
            "Entreposage sous douane",
            "Réception et expédition des marchandises",
            "Contrôle des produits et gestion des formalités",
        ],
        "steps": [
            {"title": "Réception", "text": "Réception de la marchandise et contrôle à l'arrivée."},
            {"title": "Stockage", "text": "Mise en stock dans nos installations, y compris sous régime douanier."},
            {"title": "Gestion", "text": "Suivi des produits stockés et gestion des formalités."},
            {"title": "Expédition", "text": "Préparation et expédition selon vos instructions."},
        ],
        "why_us": [
            "Une gestion des formalités prise en charge de bout en bout",
            "Un suivi rigoureux des marchandises stockées",
            "Une solution combinable avec nos services de transport",
        ],
    },
    {
        "slug": "agent-de-fret",
        "name": "Agent de fret",
        "short_description": "Organisation complète de vos opérations de fret : choix des modes de transport, documentation et coordination des intervenants.",
        "long_intro": "En tant qu'agent de fret, ESC organise et coordonne vos expéditions de bout en bout : sélection des modes de transport, relation avec les compagnies et les prestataires, et suivi documentaire de vos opérations d'import-export.",
        "image": "hero-port.jpg",
        "benefits": [
            "Organisation multimodale de vos expéditions",
            "Coordination des différents intervenants de la chaîne",
            "Préparation et contrôle des documents de transport",
            "Accompagnement personnalisé de vos opérations",
        ],
        "steps": [
            {"title": "Cadrage", "text": "Nous définissons avec vous le schéma logistique adapté."},
            {"title": "Organisation", "text": "Nous réservons et coordonnons les différents maillons du transport."},
            {"title": "Documentation", "text": "Nous établissons et vérifions les documents nécessaires."},
            {"title": "Suivi", "text": "Nous assurons le suivi jusqu'à la livraison finale."},
        ],
        "why_us": [
            "Un interlocuteur unique pour toute la chaîne logistique",
            "Une expérience confirmée de l'import-export en Algérie",
            "Un service personnalisé pour chaque client",
        ],
    },
    {
        "slug": "agent-maritime",
        "name": "Agent maritime",
        "short_description": "Représentation et assistance des navires à l'escale : formalités portuaires, coordination des opérations et relation avec les autorités.",
        "long_intro": "ESC assure la représentation des armateurs et l'assistance des navires lors de leurs escales : accomplissement des formalités portuaires, coordination des opérations à quai et relation avec les autorités et les prestataires locaux.",
        "image": "svc-agent.jpg",
        "benefits": [
            "Assistance du navire pendant l'escale",
            "Accomplissement des formalités portuaires",
            "Coordination des opérations de manutention",
            "Interface avec les autorités portuaires locales",
        ],
        "steps": [
            {"title": "Annonce d'escale", "text": "Préparation de l'escale et information des parties prenantes."},
            {"title": "Formalités", "text": "Traitement des formalités administratives et portuaires."},
            {"title": "Opérations", "text": "Coordination des opérations commerciales du navire."},
            {"title": "Clôture", "text": "Suivi post-escale et transmission des documents."},
        ],
        "why_us": [
            "Une présence locale en Algérie",
            "Une bonne connaissance des procédures portuaires",
            "Une réactivité adaptée aux contraintes d'escale",
        ],
    },
    {
        "slug": "dedouanement",
        "name": "Dédouanement",
        "short_description": "Prise en charge des formalités douanières à l'import et à l'export, avec préparation et suivi des déclarations.",
        "long_intro": "ESC prend en charge les formalités de dédouanement de vos marchandises à l'import comme à l'export : constitution des dossiers, déclarations et suivi des opérations auprès des services douaniers.",
        "image": "svc-dedouanement.jpg",
        "benefits": [
            "Formalités douanières import et export",
            "Constitution et contrôle des dossiers",
            "Suivi des déclarations jusqu'à la mainlevée",
            "Conseil sur les documents requis",
        ],
        "steps": [
            {"title": "Collecte des documents", "text": "Nous réunissons les pièces nécessaires au dossier."},
            {"title": "Déclaration", "text": "Nous établissons la déclaration en douane."},
            {"title": "Suivi", "text": "Nous suivons le traitement du dossier auprès des services concernés."},
            {"title": "Mise à disposition", "text": "Nous organisons l'enlèvement de la marchandise après mainlevée."},
        ],
        "why_us": [
            "Une maîtrise des procédures douanières algériennes",
            "Un traitement rigoureux des dossiers",
            "Une coordination directe avec vos opérations de transport",
        ],
    },
    {
        "slug": "transport-aerien",
        "name": "Transport aérien",
        "short_description": "Solutions de fret aérien pour vos envois urgents ou à forte valeur, vers et depuis l'Algérie.",
        "long_intro": "Le fret aérien répond aux besoins d'expéditions rapides. ESC organise l'acheminement de vos marchandises par voie aérienne, avec la préparation documentaire et la coordination des opérations au départ comme à l'arrivée.",
        "image": "svc-aerien.jpg",
        "benefits": [
            "Délais d'acheminement réduits",
            "Adapté aux envois urgents et à forte valeur",
            "Préparation complète des documents de transport aérien",
            "Coordination au départ et à l'arrivée",
        ],
        "steps": [
            {"title": "Demande", "text": "Vous nous transmettez les caractéristiques de votre envoi."},
            {"title": "Cotation", "text": "Nous proposons une solution et un délai adaptés."},
            {"title": "Expédition", "text": "Nous organisons l'enlèvement et le départ de la marchandise."},
            {"title": "Livraison", "text": "Nous suivons l'envoi jusqu'à sa mise à disposition."},
        ],
        "why_us": [
            "Une réactivité adaptée aux expéditions urgentes",
            "Un suivi assuré par un interlocuteur dédié",
            "Une complémentarité avec nos autres modes de transport",
        ],
    },
    {
        "slug": "transport-routier",
        "name": "Transport routier",
        "short_description": "Transport en charge complète (FTL) ou groupage (LTL), avec suivi en temps réel et livraison dans les délais.",
        "long_intro": "ESC organise le transport routier de vos marchandises en charge complète (FTL) ou en groupage (LTL), avec une couverture assurée par notre flotte et notre réseau de partenaires, un suivi en temps réel et une attention particulière portée à la sécurité des marchandises.",
        "image": "svc-routier.jpg",
        "benefits": [
            "Transport en charge complète (FTL) et en groupage (LTL)",
            "Couverture assurée par la flotte et le réseau de partenaires",
            "Suivi en temps réel des expéditions",
            "Sécurité des marchandises et respect des délais",
        ],
        "steps": [
            {"title": "Planification", "text": "Nous définissons l'itinéraire et le type de chargement."},
            {"title": "Enlèvement", "text": "Nous organisons le chargement au point de départ."},
            {"title": "Acheminement", "text": "Nous assurons le transport avec suivi de l'expédition."},
            {"title": "Livraison", "text": "Nous livrons la marchandise à destination dans les délais convenus."},
        ],
        "why_us": [
            "Une couverture nationale par la route",
            "Un suivi en temps réel de vos expéditions",
            "Une solution facilement combinable avec le maritime et l'aérien",
        ],
    },
]

MARITIME_CAMPAIGNS = [
    {
        "title": "Offre Méditerranée Express",
        "subtitle": "Ligne Europe – Algérie",
        "route_from": "Marseille / Gênes",
        "route_to": "Alger / Béjaïa",
        "discount": "–15 %",
        "description": "Profitez d'un tarif préférentiel sur le fret conteneurisé FCL et LCL entre les ports méditerranéens et les principaux ports algériens. Idéal pour les importateurs réguliers.",
        "valid_until": "2026-12-31",
        "status": "active",
        "highlights": [
            "FCL 20' et 40' inclus",
            "Délai garanti 5 à 7 jours",
            "Documentation prise en charge",
        ],
    },
    {
        "title": "Pack Asie – Algérie Winter Deal",
        "subtitle": "Ligne Asie – Maghreb",
        "route_from": "Shanghai / Guangzhou",
        "route_to": "Oran / Alger",
        "discount": "–12 %",
        "description": "Réduction saisonnière sur les expéditions FCL en provenance des grands ports chinois vers l'Algérie. Valable pour les bookings confirmés avant le 31 octobre.",
        "valid_until": "2026-10-31",
        "status": "limited",
        "highlights": [
            "Transbordement rapide à Tanger",
            "Suivi en temps réel",
            "Offre limitée aux 50 premiers bookings",
        ],
    },
    {
        "title": "Groupage Turquie Premium",
        "subtitle": "Ligne Turquie – Algérie",
        "route_from": "Istanbul / Mersin",
        "route_to": "Annaba / Skikda",
        "discount": "–10 %",
        "description": "Service LCL dédié avec départs hebdomadaires garantis depuis la Turquie. Regroupez vos marchandises avec d'autres chargeurs et réduisez vos coûts.",
        "valid_until": "2026-11-30",
        "status": "active",
        "highlights": [
            "Départs chaque lundi",
            "Min. 1 CBM accepté",
            "Consolidation professionnelle",
        ],
    },
    {
        "title": "Ligne Amérique du Nord Q1 2027",
        "subtitle": "Ligne USA / Canada – Algérie",
        "route_from": "New York / Houston",
        "route_to": "Alger",
        "discount": "–8 %",
        "description": "Lancement d'une nouvelle ligne directe Amérique du Nord — Algérie. Réservez dès maintenant à tarif early-bird et bénéficiez d'une priorité de chargement.",
        "valid_until": "2027-03-31",
        "status": "upcoming",
        "highlights": [
            "Tarif early-bird garanti",
            "Priorité de chargement",
            "Accompagnement douanier inclus",
        ],
    },
]

ASSOCIATED_CAMPAIGNS = [
    {
        "category": "Logistique portuaire",
        "title": "Pack Port Intégré",
        "description": "Combinaison transport maritime + manutention portuaire + entreposage court terme à tarif négocié. Idéal pour les opérations d'import régulières.",
        "badge": "Bundle",
        "status": "active",
        "valid_until": "2026-12-31",
    },
    {
        "category": "Dédouanement",
        "title": "Clearance Express",
        "description": "Prise en charge prioritaire de vos déclarations douanières dans un délai de 48 h. Inclut la constitution du dossier et le suivi jusqu'à la mainlevée.",
        "badge": "Offre rapide",
        "status": "active",
        "valid_until": "2026-11-30",
    },
    {
        "category": "Assurance cargo",
        "title": "Couverture Tous Risques Maritime",
        "description": "Assurance tous risques pour vos conteneurs FCL et LCL. Tarif préférentiel négocié avec nos partenaires assureurs pour les expéditions maritimes.",
        "badge": "Recommandé",
        "status": "limited",
        "valid_until": "2026-10-31",
    },
    {
        "category": "Entreposage",
        "title": "Stockage Tampon 30 Jours Offerts",
        "description": "Premier mois d'entreposage offert pour tout contrat de transport maritime signé dans le cadre d'une campagne active ESC.",
        "badge": "Nouveau",
        "status": "upcoming",
        "valid_until": "2027-01-31",
    },
    {
        "category": "Transport routier",
        "title": "Pré/Post Acheminement Inclus",
        "description": "Enlèvement ou livraison porte-à-port offert sur les 200 premiers km pour toute réservation maritime confirmée via ESC.",
        "badge": "Exclusif",
        "status": "active",
        "valid_until": "2026-12-15",
    },
]

STATS = [
    {"value": 10, "suffix": "+", "label": "Années d'expérience", "order": 1},
    {"value": 300, "suffix": "+", "label": "Clients accompagnés", "order": 2},
    {"value": 40, "suffix": "+", "label": "Partenaires internationaux", "order": 3},
]

TRUSTED_PARTNERS = [
    {"name": "MSC", "domain": "msc.com", "order": 1},
    {"name": "COSCO Shipping", "domain": "lines.coscoshipping.com", "order": 2},
    {"name": "CMA CGM", "domain": "cma-cgm.com", "order": 3},
    {"name": "AKKON Lines", "domain": "akkonlines.com", "order": 4},
    {"name": "Maersk", "domain": "maersk.com", "order": 5},
    {"name": "Hapag-Lloyd", "domain": "www.hapag-lloyd.com", "order": 6},
    {"name": "ONE", "domain": "one-line.com", "order": 7},
    {"name": "Evergreen", "domain": "www.evergreen-marine.com", "order": 8},
    {"name": "Turkon Line", "domain": "turkon.com", "order": 9},
]

USERS = [
    {
        "email": "admin@esc-shipping.com",
        "username": "admin",
        "first_name": "Admin",
        "last_name": "ESC",
        "role": UserRole.ADMIN,
        "password": "admin123",
        "phone_number": "+213555508621",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "email": "manager@esc-shipping.com",
        "username": "manager",
        "first_name": "Mohamed",
        "last_name": "Benali",
        "role": UserRole.MANAGER,
        "password": "manager123",
        "phone_number": "+213555508620",
    },
    {
        "email": "client@esc-shipping.com",
        "username": "client",
        "first_name": "Ahmed",
        "last_name": "Kaci",
        "role": UserRole.CLIENT,
        "password": "client123",
        "phone_number": "+213555508619",
    },
    {
        "email": "driver@esc-shipping.com",
        "username": "driver",
        "first_name": "Yacine",
        "last_name": "Hamdi",
        "role": UserRole.DRIVER,
        "password": "driver123",
        "phone_number": "+213555508618",
    },
    {
        "email": "support@esc-shipping.com",
        "username": "support",
        "first_name": "Fatima",
        "last_name": "Zohra",
        "role": UserRole.SUPPORT,
        "password": "support123",
        "phone_number": "+213555508617",
    },
]

# Map service slugs to front-end image filenames
FRONTEND_IMAGES = {
    "svc-maritime.jpg": "svc-maritime.jpg",
    "svc-entreposage.jpg": "svc-entreposage.jpg",
    "hero-port.jpg": "hero-port.jpg",
    "svc-agent.jpg": "svc-agent.jpg",
    "svc-dedouanement.jpg": "svc-dedouanement.jpg",
    "svc-aerien.jpg": "svc-aerien.jpg",
    "svc-routier.jpg": "svc-routier.jpg",
}

BRANDING_IMAGE = "logo.png"

RESOURCES = [
    # Common maritime equipment, based on the Operplus container reference.
    {"resource_type": "container", "slug": "20-dry-van", "title": "20' DRY VAN", "summary": "General-purpose container for palletized and boxed cargo.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.591 m", "Interior": "5.898 × 2.352 × 2.393 m", "Max load": "28,260 kg", "MGW": "30,480 kg", "Tare": "2,220 kg", "Volume": "33.20 m³"}},
    {"resource_type": "container", "slug": "20-flat-rack", "title": "20' FLAT RACK", "summary": "Open-sided platform for oversized or project cargo.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.591 m", "Interior": "5.950 × 2.226 m", "Max load": "27,110 kg", "MGW": "30,000 kg", "Tare": "2,890 kg", "Volume": "32.30 m³"}},
    {"resource_type": "container", "slug": "20-flat-rack-hc", "title": "20' FLAT RACK HC", "summary": "High-cube flat rack for tall and heavy project cargo.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.896 m", "Interior": "5.950 × 2.226 m", "Max load": "27,110 kg", "MGW": "30,000 kg", "Tare": "2,890 kg", "Volume": "32.30 m³"}},
    {"resource_type": "container", "slug": "20-jaula", "title": "20' JAULA", "summary": "Ventilated cage-style unit for cargo requiring airflow.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.591 m", "Interior": "5.943 × 2.318 × 2.275 m", "Max load": "21,610 kg", "MGW": "24,000 kg", "Tare": "2,390 kg", "Volume": "31.40 m³"}},
    {"resource_type": "container", "slug": "20-jaula-hc", "title": "20' JAULA HC", "summary": "High-cube cage-style unit for ventilated, tall cargo.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.896 m", "Interior": "5.943 × 2.318 × 2.694 m", "Max load": "27,110 kg", "MGW": "30,000 kg", "Tare": "2,750 kg", "Volume": "37.10 m³"}},
    {"resource_type": "container", "slug": "20-open-top", "title": "20' OPEN TOP", "summary": "Removable-roof container for top-loaded and tall cargo.", "image": "resource-container-bulk.png", "specifications": {"Exterior": "6.058 × 2.438 × 2.591 m", "Interior": "5.940 × 2.352 × 2.360 m", "Max load": "24,000 kg", "MGW": "27,120 kg", "Tare": "3,120 kg", "Volume": "33.20 m³"}},
    {"resource_type": "container", "slug": "20-pallet-wide", "title": "20' PALLET WIDE", "summary": "Pallet-wide footprint for 14 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "5.898 × 2.426 × 2.393 m", "Max load": "27,990 kg", "MGW": "30,480 kg", "Tare": "2,490 kg", "Volume": "38.60 m³", "Capacity": "14 Euro pallets"}},
    {"resource_type": "container", "slug": "20-pallet-wide-hc", "title": "20' PALLET WIDE HC", "summary": "High-cube pallet-wide unit for 14 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "5.898 × 2.426 × 2.712 m", "Max load": "27,990 kg", "MGW": "30,480 kg", "Tare": "2,490 kg", "Volume": "36.60 m³", "Capacity": "14 Euro pallets"}},
    {"resource_type": "container", "slug": "20-reefer", "title": "20' REEFER", "summary": "Temperature-controlled container for chilled or frozen cargo.", "image": "resource-container-bulk.png", "specifications": {"Exterior": "6.058 × 2.484 × 2.591 m", "Interior": "5.456 × 2.294 × 2.275 m", "Max load": "27,540 kg", "MGW": "30,480 kg", "Tare": "2,940 kg", "Volume": "28.50 m³"}},
    {"resource_type": "container", "slug": "20-bulk", "title": "20' BULK", "summary": "Bulk container for dry loose commodities and dense cargo.", "image": "resource-container-bulk.png", "specifications": {"Exterior": "6.058 × 2.484 × 2.591 m", "Interior": "5.456 × 2.294 × 2.275 m", "Max load": "27,540 kg", "MGW": "30,480 kg", "Tare": "2,940 kg", "Volume": "28.50 m³"}},
    {"resource_type": "container", "slug": "20-tank", "title": "20' TANK", "summary": "Tank container for regulated liquid and bulk commodities.", "image": "resource-container-bulk.png", "specifications": {"Exterior": "7.820 × 2.550 × 2.670 m", "Max load": "27,540 kg", "Pressure": "4.0 bar", "Tare": "3,540–3,830 kg", "Volume": "21,000–26,000 l"}},
    {"resource_type": "container", "slug": "40-dry-van", "title": "40' DRY VAN", "summary": "Long general-purpose container for high-volume cargo.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "12.192 × 2.438 × 2.591 m", "Interior": "12.032 × 2.352 × 2.393 m", "Max load": "28,650 kg", "MGW": "30,480 kg", "Tare": "3,850 kg", "Volume": "67.70 m³"}},
    {"resource_type": "container", "slug": "40-flat-rack", "title": "40' FLAT RACK", "summary": "Heavy-duty platform for oversized machinery and project cargo.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "12.064 × 2.438 × 1.953 m", "Max load": "29,870 kg", "MGW": "35,000 kg", "Tare": "5,130 kg", "Volume": "57.41 m³"}},
    {"resource_type": "container", "slug": "40-flat-rack-hc", "title": "40' FLAT RACK HC", "summary": "High-cube flat rack for tall, heavy project cargo.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "12.064 × 2.438 × 1.953 m", "Max load": "29,870 kg", "MGW": "35,000 kg", "Tare": "5,130 kg", "Volume": "57.41 m³"}},
    {"resource_type": "container", "slug": "40-high-cube", "title": "40' HIGH CUBE", "summary": "Extra height for voluminous cargo and optimized pallet loading.", "image": "resource-container-high-cube.png", "specifications": {"Exterior": "12.192 × 2.438 × 2.896 m", "Interior": "12.064 × 2.438 × 2.692 m", "Max load": "29,870 kg", "MGW": "30,480 kg", "Tare": "5,130 kg", "Volume": "57.41 m³"}},
    {"resource_type": "container", "slug": "40-jaula", "title": "40' JAULA", "summary": "Ventilated cage-style equipment for airflow-sensitive cargo.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "12.086 × 2.320 × 1.120–2.275 m", "Max load": "26,760 kg", "MGW": "30,480 kg", "Tare": "3,720 kg", "Volume": "31.40 m³"}},
    {"resource_type": "container", "slug": "40-open-top", "title": "40' OPEN TOP", "summary": "Top-loading format for tall, dense or crane-handled cargo.", "image": "resource-container-bulk.png", "specifications": {"Interior": "12.032 × 2.352 × 2.360 m", "Max load": "26,530 kg", "MGW": "30,480 kg", "Tare": "3,950 kg", "Volume": "66.80 m³"}},
    {"resource_type": "container", "slug": "40-reefer-hc", "title": "40' REEFER HC", "summary": "High-cube refrigerated unit for temperature-sensitive cargo.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "11.590 × 2.294 × 2.557 m", "Max load": "30,420 kg", "MGW": "35,000 kg", "Tare": "4,580 kg", "Volume": "67.90 m³"}},
    {"resource_type": "container", "slug": "40-pallet-wide", "title": "40' PALLET WIDE", "summary": "Pallet-wide format for 30 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "12.100 × 2.426 × 2.383 m", "Max load": "29,850 kg", "MGW": "34,000 kg", "Tare": "4,150 kg", "Volume": "79.10 m³", "Capacity": "30 Euro pallets"}},
    {"resource_type": "container", "slug": "40-pallet-wide-hc", "title": "40' PALLET WIDE HC", "summary": "High-cube pallet-wide format for 30 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "12.100 × 2.426 × 2.694 m", "Max load": "29,850 kg", "MGW": "34,000 kg", "Tare": "4,150 kg", "Volume": "79.10 m³", "Capacity": "30 Euro pallets"}},
    {"resource_type": "container", "slug": "45-pallet-wide-hc", "title": "45' PALLET WIDE HC", "summary": "Maximum pallet capacity for 33 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "13.532 × 2.426 × 2.694 m", "Max load": "29,350 kg", "MGW": "34,000 kg", "Tare": "4,650 kg", "Volume": "88.40 m³", "Capacity": "33 Euro pallets"}},
    {"resource_type": "container", "slug": "45-reefer-pallet-wide-hc", "title": "45' REEFER PALLET WIDE HC", "summary": "Refrigerated pallet-wide format for 33 Euro pallets.", "image": "resource-container-high-cube.png", "specifications": {"Interior": "13.532 × 2.426 × 2.694 m", "Max load": "29,350 kg", "MGW": "34,000 kg", "Tare": "4,650 kg", "Volume": "88.40 m³", "Capacity": "33 Euro pallets"}},
    # Airframes and ULDs from the Operplus aircraft and cargo reference.
    {"resource_type": "aircraft", "slug": "airbus-a320", "title": "AIRBUS A320", "summary": "Narrow-body passenger aircraft with lower-deck cargo capability.", "image": "resource-aircraft-747.png", "specifications": {"Hold 1": "124 × 180 cm", "Hold 3": "124 × 180 cm", "Hold 5": "87 × 94 cm", "Capacity": "0.5 Ton", "ULD compatible": "AKH"}},
    {"resource_type": "aircraft", "slug": "airbus-a321", "title": "AIRBUS A321", "summary": "Narrow-body aircraft for regional cargo uplift.", "image": "resource-aircraft-747.png", "specifications": {"Hold 1": "124 × 180 cm", "Hold 3": "124 × 180 cm", "Hold 5": "87 × 94 cm", "Capacity": "1 Ton", "ULD compatible": "AKH"}},
    {"resource_type": "aircraft", "slug": "airbus-a330-200", "title": "AIRBUS A330-200", "summary": "Wide-body aircraft for intercontinental cargo flows.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "270 × 171 cm", "Stern door": "272 × 167 cm", "Loading door": "95 × 107 cm", "Capacity": "14 Ton", "ULD compatible": "LD3, LD9, PAP, PMC"}},
    {"resource_type": "aircraft", "slug": "airbus-a330-300", "title": "AIRBUS A330-300", "summary": "Wide-body aircraft with flexible lower-deck ULD positions.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "270 × 167 cm", "Stern door": "272 × 167 cm", "Loading door": "94 × 315 cm", "Capacity": "16 Ton", "ULD compatible": "LD3, LD9, PAP, PMC, LD11, PKC"}},
    {"resource_type": "aircraft", "slug": "airbus-a350-900", "title": "AIRBUS A350-900", "summary": "Long-range wide-body aircraft for high-value cargo.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "285 × 168 cm", "Stern door": "280 × 168 cm", "Capacity": "17 Ton", "ULD compatible": "LD3, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "airbus-a350-1000", "title": "AIRBUS A350-1000", "summary": "High-capacity long-range wide-body aircraft.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "176 × 291 cm", "Stern door": "175 × 285 cm", "Loading door": "76 × 95 cm", "Capacity": "25 Ton", "ULD compatible": "LD3, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "airbus-a380-800", "title": "AIRBUS A380-800", "summary": "Large wide-body platform with broad ULD compatibility.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "283 × 173 cm", "Stern door": "254 × 173 cm", "Capacity": "13.2 Ton", "ULD compatible": "LD3, LD9, PMC, PAP, LD11"}},
    {"resource_type": "aircraft", "slug": "boeing-787-8", "title": "BOEING 787-8", "summary": "Efficient wide-body aircraft for international cargo.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "268 × 170 cm", "Stern door": "268 × 170 cm", "Loading door": "101 × 114 cm", "Capacity": "9 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "boeing-787-9", "title": "BOEING 787-9", "summary": "Extended Dreamliner platform with additional cargo capacity.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "268 × 170 cm", "Stern door": "268 × 170 cm", "Loading door": "101 × 114 cm", "Capacity": "11 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "boeing-787-10", "title": "BOEING 787-10", "summary": "Longer Dreamliner variant for efficient cargo uplift.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "269 × 170 cm", "Stern door": "269 × 170 cm", "Loading door": "102 × 156 cm", "Capacity": "13 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "boeing-777-200", "title": "BOEING 777-200", "summary": "Long-range twin-engine wide-body aircraft.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "269 × 170 cm", "Stern door": "269 × 170 cm", "Loading door": "91 × 103 cm", "Capacity": "20 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "boeing-777-300", "title": "BOEING 777-300", "summary": "High-capacity long-range passenger aircraft.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "269 × 170 cm", "Stern door": "269 × 170 cm", "Loading door": "91 × 103 cm", "Capacity": "25 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "aircraft", "slug": "boeing-747-8f", "title": "BOEING 747-8F", "summary": "Dedicated freighter for oversized and intercontinental cargo.", "image": "resource-aircraft-747.png", "specifications": {"Bow door": "264 × 249 cm", "Stern door": "264 × 168 cm", "Loading door": "112 × 168 cm", "Capacity": "117 Ton", "ULD compatible": "LD3, LD9, LD11, PMC, PAP"}},
    {"resource_type": "air_freight", "slug": "akh", "title": "AKH", "summary": "Lower-deck container for narrow-body aircraft.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "62.9 × 244 × 117.8 × 156.2 × 154.4 cm", "Volume": "3.4 m³"}},
    {"resource_type": "air_freight", "slug": "ld3", "title": "LD3", "summary": "Contoured lower-deck ULD for wide-body aircraft.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "201.6 × 110.2 × 163.5 × 156.2 × 154.4 cm", "Volume": "4.2 m³"}},
    {"resource_type": "air_freight", "slug": "ld9", "title": "LD9", "summary": "Large lower-deck container for high-volume cargo.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "224.5 × 157.5 × 317.5 cm", "Volume": "10 m³"}},
    {"resource_type": "air_freight", "slug": "pap", "title": "PAP", "summary": "Main-deck pallet for wide-body aircraft loading systems.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "224.5 × 163.5 × 317.5 cm", "Volume": "11.9 m³"}},
    {"resource_type": "air_freight", "slug": "pmc", "title": "PMC", "summary": "Aluminium air cargo pallet with cargo net restraint.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "244 × 163.5 × 317.5 cm", "Volume": "12.7 m³"}},
    {"resource_type": "air_freight", "slug": "ld11", "title": "LD11", "summary": "Wide-body lower-deck ULD for dense or irregular loads.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "154.4 × 163.5 × 317.5 cm", "Volume": "7 m³"}},
    {"resource_type": "air_freight", "slug": "pkc", "title": "PKC", "summary": "Compact lower-deck air freight unit for fast handling.", "image": "resource-air-pmc.png", "specifications": {"Dimensions": "153.4 × 156.2 × 109 cm", "Volume": "2.02 m³"}},
    {"resource_type": "incoterm", "slug": "incoterms-2020", "title": "INCOTERMS® 2020", "summary": "A practical guide to handover points, costs and risk allocation.", "image": "hero-port.jpg", "specifications": {"terms": ["EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DAP", "DPU", "DDP"]}, "responsibilities": {"stages": ["Ready", "Origin handling", "Export customs", "Main carriage", "Import customs", "Final delivery"], "seller": {"EXW": 1, "FCA": 2, "FAS": 2, "FOB": 3, "CFR": 4, "CIF": 4, "CPT": 4, "CIP": 4, "DAP": 5, "DPU": 5, "DDP": 6}, "notes": {"EXW": "Buyer takes responsibility from the seller’s premises.", "FCA": "Seller clears goods for export and hands them to the carrier.", "FAS": "Seller places goods alongside the vessel at origin.", "FOB": "Seller loads goods on board the vessel.", "CFR": "Seller pays freight to destination; risk transfers at loading.", "CIF": "CFR plus seller-provided minimum cargo insurance.", "CPT": "Seller pays carriage to the named place; risk transfers earlier.", "CIP": "CPT plus seller-provided cargo insurance.", "DAP": "Seller delivers ready for unloading at the named destination.", "DPU": "Seller delivers after unloading at the named destination.", "DDP": "Seller manages costs and formalities through delivery, including import duties."}}},
]

LOAD_CHARTS = [
    {"resource_type": "load_chart", "slug": "dry-20-100x120", "title": "Dry 20' - 100 × 120 cm pallets", "summary": "20-foot dry container capacity plan with 100 × 120 cm pallets.", "image": "load-charts/load-chart-02.png", "specifications": {"Load plan": "100 × 120 cm pallets", "Loose cargo": "Equivalent to 1 or 1.5 pallets", "Max load": "28,260 kg", "MGW": "30,480 kg", "Tare": "2,220 kg", "Volume": "33.20 m³"}},
    {"resource_type": "load_chart", "slug": "dry-20-euro-pallets", "title": "Dry 20' - 10 Euro pallets", "summary": "20-foot dry container plan for 80 × 120 cm Euro pallets.", "image": "load-charts/load-chart-03.png", "specifications": {"Load plan": "10 Euro pallets, 80 × 120 cm", "Loose cargo": "Equivalent to 1 pallet", "Max load": "28,260 kg", "MGW": "30,480 kg", "Tare": "2,220 kg", "Volume": "33.20 m³"}},
    {"resource_type": "load_chart", "slug": "dry-20-100x120-pallets", "title": "Dry 20' - 10 pallets", "summary": "20-foot dry container plan for 10 pallets of 100 × 120 cm.", "image": "load-charts/load-chart-04.png", "specifications": {"Load plan": "10 pallets, 100 × 120 cm", "Loose cargo": "Equivalent to 1 pallet", "Max load": "28,260 kg", "MGW": "30,480 kg", "Tare": "2,220 kg", "Volume": "33.20 m³"}},
    {"resource_type": "load_chart", "slug": "dry-20-11-euro-pallets", "title": "Dry 20' - 11 Euro pallets", "summary": "20-foot dry container plan for 11 Euro pallets of 80 × 120 cm.", "image": "load-charts/load-chart-05.png", "specifications": {"Load plan": "11 Euro pallets, 80 × 120 cm", "Loose cargo": "Equivalent to 1 or 1.5 pallets", "Max load": "28,260 kg", "MGW": "30,480 kg", "Tare": "2,220 kg", "Volume": "33.20 m³"}},
    {"resource_type": "load_chart", "slug": "dry-40-21-pallets", "title": "Dry 40' - 21 pallets", "summary": "40-foot dry container plan for 21 pallets of 100 × 120 cm.", "image": "load-charts/load-chart-06.png", "specifications": {"Load plan": "21 pallets, 100 × 120 cm", "Loose cargo": "Equivalent to 1 pallet", "Max load": "28,650 kg", "MGW": "32,500 kg", "Tare": "3,850 kg", "Volume": "67.70 m³"}},
    {"resource_type": "load_chart", "slug": "dry-40-24-euro-pallets", "title": "Dry 40' - 24 Euro pallets", "summary": "40-foot dry container plan for 24 Euro pallets of 80 × 120 cm.", "image": "load-charts/load-chart-07.png", "specifications": {"Load plan": "24 Euro pallets, 80 × 120 cm", "Loose cargo": "Equivalent to 1 pallet", "Max load": "28,650 kg", "MGW": "32,500 kg", "Tare": "3,850 kg", "Volume": "67.70 m³"}},
    {"resource_type": "load_chart", "slug": "reefer-20-10-euro-pallets", "title": "Reefer 20' - 10 Euro pallets", "summary": "20-foot refrigerated container plan for 10 Euro pallets.", "image": "load-charts/load-chart-08.png", "specifications": {"Load plan": "10 Euro pallets, 80 × 120 cm", "Loose cargo": "Equivalent to 1 pallet", "Max load": "27,540 kg", "MGW": "30,480 kg", "Tare": "2,940 kg", "Volume": "28.50 m³"}},
    {"resource_type": "load_chart", "slug": "reefer-20-hc-9-pallets", "title": "Reefer 20' HC - 9 pallets", "summary": "20-foot high-cube reefer plan for 9 pallets of 100 × 120 cm.", "image": "load-charts/load-chart-09.png", "specifications": {"Load plan": "9 pallets, 100 × 120 cm", "Loose cargo": "Equivalent to 1 or 1.5 pallets", "Max load": "27,540 kg", "MGW": "30,480 kg", "Tare": "2,940 kg", "Volume": "28.50 m³"}},
    {"resource_type": "load_chart", "slug": "reefer-40-hc-20-pallets", "title": "Reefer 40' HC - 20 pallets", "summary": "40-foot high-cube reefer plan for 20 pallets of 100 × 120 cm.", "image": "load-charts/load-chart-10.png", "specifications": {"Load plan": "20 pallets, 100 × 120 cm", "Loose cargo": "Equivalent to 1 or 1.5 pallets", "Max load": "30,420 kg", "MGW": "35,000 kg", "Tare": "4,580 kg", "Volume": "67.90 m³"}},
    {"resource_type": "load_chart", "slug": "reefer-40-hc-mixed-pallets", "title": "Reefer 40' HC - mixed pallet plan", "summary": "40-foot high-cube reefer plan for 20 standard pallets plus one Euro pallet.", "image": "load-charts/load-chart-11.png", "specifications": {"Load plan": "20 pallets of 100 × 120 cm + 1 Euro pallet", "Loose cargo": "229.4 cm × 19 cm", "Max load": "30,420 kg", "MGW": "35,000 kg", "Tare": "4,580 kg", "Volume": "67.90 m³"}},
    {"resource_type": "load_chart", "slug": "reefer-40-hc-23-euro-pallets", "title": "Reefer 40' HC - 23 Euro pallets", "summary": "40-foot high-cube reefer plan for 23 Euro pallets of 80 × 120 cm.", "image": "load-charts/load-chart-12.png", "specifications": {"Load plan": "23 Euro pallets, 80 × 120 cm", "Loose cargo": "Equivalent to 1 or 1.5 pallets", "Max load": "30,420 kg", "MGW": "35,000 kg", "Tare": "4,580 kg", "Volume": "67.90 m³"}},
]


class Command(BaseCommand):
    help = "Seed the database with front-end mock data and create default users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Clear existing data before seeding.",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== ESC Shipping Database Seeder ==="))

        if options["flush"]:
            self.stdout.write(self.style.WARNING("Flushing existing data..."))
            self._flush_data()

        with transaction.atomic():
            self._seed_users()
            self._seed_services()
            self._seed_branding()
            self._seed_maritime_campaigns()
            self._seed_associated_campaigns()
            self._seed_stats()
            self._seed_partners()
            self._seed_resources()

        self.stdout.write(self.style.SUCCESS("\n=== Seeding Complete ==="))
        self._print_summary()

    def _flush_data(self):
        """Delete all existing data."""
        ServiceStep.objects.all().delete()
        Service.objects.all().delete()
        SiteBranding.objects.all().delete()
        MaritimeCampaign.objects.all().delete()
        AssociatedCampaign.objects.all().delete()
        Stat.objects.all().delete()
        TrustedPartner.objects.all().delete()
        ResourceItem.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        self.stdout.write("  All existing data cleared.")

    def _seed_users(self):
        """Create default user accounts."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Users..."))
        for user_data in USERS:
            password = user_data.pop("password")
            user, created = User.objects.get_or_create(
                email=user_data["email"],
                defaults=user_data,
            )
            if created:
                user.set_password(password)
                user.save()
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f"  Created: {user.email} ({user.role})")
                )
            else:
                self.stdout.write(f"  Exists:  {user.email}")

    def _seed_services(self):
        """Create services with steps and copy images."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Services..."))
        frontend_assets = Path(settings.BASE_DIR).parent / "src" / "assets"

        for order, service_data in enumerate(SERVICES, start=1):
            image_filename = service_data.pop("image")
            steps = service_data.pop("steps")
            benefits = service_data.pop("benefits")
            why_us = service_data.pop("why_us")

            service, created = Service.objects.get_or_create(
                slug=service_data["slug"],
                defaults={
                    **service_data,
                    "benefits": "\n".join(benefits),
                    "why_us": "\n".join(why_us),
                    "order": order,
                },
            )

            if created:
                # Create steps
                for step_order, step in enumerate(steps, start=1):
                    ServiceStep.objects.create(
                        service=service,
                        title=step["title"],
                        text=step["text"],
                        order=step_order,
                    )

                # Copy image from front-end assets
                src_image = frontend_assets / image_filename
                if src_image.exists():
                    with open(src_image, "rb") as f:
                        service.image.save(
                            image_filename,
                            File(f),
                            save=True,
                        )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Created: {service.name} (with image)"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  Created: {service.name} (image not found: {image_filename})"
                        )
                    )
            else:
                self.stdout.write(f"  Exists:  {service.name}")

    def _seed_branding(self):
        """Create or update the admin-managed site logo."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Site Branding..."))
        frontend_assets = Path(settings.BASE_DIR).parent / "src" / "assets"
        src_image = frontend_assets / BRANDING_IMAGE
        if not src_image.exists():
            self.stdout.write(self.style.WARNING(f"  Logo not found: {src_image}"))
            return

        branding, created = SiteBranding.objects.get_or_create(pk=1)
        with open(src_image, "rb") as image_file:
            branding.logo.save(BRANDING_IMAGE, File(image_file), save=True)
        self.stdout.write(self.style.SUCCESS(f"  {'Created' if created else 'Updated'}: site logo"))

    def _seed_maritime_campaigns(self):
        """Create maritime campaigns."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Maritime Campaigns..."))
        for campaign_data in MARITIME_CAMPAIGNS:
            highlights = campaign_data.pop("highlights")
            campaign, created = MaritimeCampaign.objects.get_or_create(
                title=campaign_data["title"],
                defaults={
                    **campaign_data,
                    "highlights": "\n".join(highlights),
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  Created: {campaign.title}")
                )
            else:
                self.stdout.write(f"  Exists:  {campaign.title}")

    def _seed_associated_campaigns(self):
        """Create associated campaigns."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Associated Campaigns..."))
        for campaign_data in ASSOCIATED_CAMPAIGNS:
            campaign, created = AssociatedCampaign.objects.get_or_create(
                title=campaign_data["title"],
                defaults=campaign_data,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  Created: {campaign.title}")
                )
            else:
                self.stdout.write(f"  Exists:  {campaign.title}")

    def _seed_stats(self):
        """Create company statistics."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Statistics..."))
        for stat_data in STATS:
            stat, created = Stat.objects.get_or_create(
                label=stat_data["label"],
                defaults=stat_data,
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  Created: {stat.value}{stat.suffix} {stat.label}")
                )
            else:
                self.stdout.write(f"  Exists:  {stat.value}{stat.suffix} {stat.label}")

    def _seed_partners(self):
        """Create trusted partners."""
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Trusted Partners..."))
        TrustedPartner.objects.exclude(
            name__in=[partner["name"] for partner in TRUSTED_PARTNERS]
        ).delete()
        for partner_data in TRUSTED_PARTNERS:
            domain = partner_data.pop("domain")
            partner, created = TrustedPartner.objects.get_or_create(
                name=partner_data["name"],
                defaults=partner_data,
            )
            self._download_partner_logo(partner, domain)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"  Created: {partner.name} (logo fetched)")
                )
            else:
                self.stdout.write(f"  Exists:  {partner.name}")

    def _seed_resources(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreating Resources..."))
        frontend_assets = Path(settings.BASE_DIR).parent / "src" / "assets"
        for order, item_data in enumerate(RESOURCES + LOAD_CHARTS, start=1):
            item_data = item_data.copy()
            image_filename = item_data.pop("image")
            if item_data["resource_type"] == "container":
                container_image_names = {
                    "20-bulk": "20-granelero",
                    "20-open-top": "20-ot",
                    "20-tank": "20-cisterna",
                    "20-pallet-wide": "20-pw",
                    "20-pallet-wide-hc": "20-pw-hc",
                    "40-high-cube": "40-hc",
                    "40-open-top": "40-ot",
                    "40-pallet-wide": "40-pw",
                    "40-pallet-wide-hc": "40-pw-hc",
                    "45-pallet-wide-hc": "45-pw-hc",
                    "45-reefer-pallet-wide-hc": "45-reefer-pw-hc",
                }
                source_stem = container_image_names.get(item_data["slug"], item_data["slug"])
                image_filename = f"operplus-containers/{source_stem}.png"
            elif item_data["resource_type"] == "air_freight":
                image_filename = f"operplus-air/uld/{item_data['slug']}.png"
            elif item_data["resource_type"] == "aircraft":
                aircraft_image_names = {
                    "airbus-a320": "AIRBUSA320",
                    "airbus-a321": "AIRBUSA321",
                    "airbus-a330-200": "AIRBUSA330-200",
                    "airbus-a330-300": "AIRBUSA330-300",
                    "airbus-a350-900": "AIRBUSA350-900",
                    "airbus-a350-1000": "AIRBUSA350-1000",
                    "airbus-a380-800": "AIRBUSA380-800",
                    "boeing-787-8": "BOEING787-8",
                    "boeing-787-9": "BOEING787-9",
                    "boeing-787-10": "BOEING787-10",
                    "boeing-777-200": "BOEING777-200",
                    "boeing-777-300": "BOEING777-300",
                    "boeing-747-8f": "BOEING747-8F",
                }
                image_filename = f"operplus-air/aircraft/{aircraft_image_names[item_data['slug']]}.png"
            item, created = ResourceItem.objects.update_or_create(
                slug=item_data["slug"], defaults={**item_data, "order": order}
            )
            source = frontend_assets / image_filename
            existing_image = (item.image.name or "").replace("\\", "/")
            if source.exists() and (created or not existing_image.endswith(image_filename)):
                with open(source, "rb") as image_file:
                    item.image.save(image_filename, File(image_file), save=True)
            self.stdout.write(self.style.SUCCESS(f"  {'Created' if created else 'Updated'}: {item.title}"))

    def _download_partner_logo(self, partner, domain):
        """Fetch the carrier favicon from its official domain into media storage."""
        logo_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=512"
        try:
            request = Request(logo_url, headers={"User-Agent": "ESC Shipping seed command"})
            with urlopen(request, timeout=15) as response:
                logo_data = response.read()
            filename = f"{partner.name.lower().replace(' ', '-').replace('/', '-')}.png"
            with Image.open(BytesIO(logo_data)) as image:
                if image.width < 64 or image.height < 32:
                    self._restore_best_partner_logo(partner, filename)
                    return
            partner.logo.save(filename, ContentFile(logo_data), save=True)
        except Exception as error:
            self.stdout.write(
                self.style.WARNING(f"  Logo unavailable for {partner.name}: {error}")
            )

    def _restore_best_partner_logo(self, partner, filename):
        """Keep the largest existing local mark when a provider returns a tiny icon."""
        media_dir = Path(settings.MEDIA_ROOT) / "partners"
        stem = Path(filename).stem
        candidates = list(media_dir.glob(f"{stem}*.png"))
        if not candidates:
            return

        best = max(candidates, key=lambda path: path.stat().st_size)
        partner.logo.name = f"partners/{best.name}"
        partner.save(update_fields=["logo"])

    def _print_summary(self):
        """Print a summary of seeded data."""
        self.stdout.write(f"\n  Users:              {User.objects.count()}")
        self.stdout.write(f"  Services:           {Service.objects.count()}")
        self.stdout.write(f"  Service Steps:      {ServiceStep.objects.count()}")
        self.stdout.write(f"  Maritime Campaigns: {MaritimeCampaign.objects.count()}")
        self.stdout.write(f"  Associated Campaigns: {AssociatedCampaign.objects.count()}")
        self.stdout.write(f"  Statistics:         {Stat.objects.count()}")
        self.stdout.write(f"  Trusted Partners:   {TrustedPartner.objects.count()}")
        self.stdout.write(f"  Resource Items:     {ResourceItem.objects.count()}")
