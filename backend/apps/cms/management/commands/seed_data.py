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
