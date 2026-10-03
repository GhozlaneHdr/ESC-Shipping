import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("cms", "0003_sitebranding_hero_video")]
    operations = [migrations.CreateModel(name="ResourceItem", fields=[
        ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("resource_type", models.CharField(choices=[("container", "Container"), ("air_freight", "Air freight"), ("aircraft", "Aircraft"), ("incoterm", "Incoterm"), ("load_chart", "Load chart")], max_length=20)),
        ("slug", models.SlugField(unique=True)), ("title", models.CharField(max_length=160)), ("summary", models.TextField(blank=True)),
        ("image", models.ImageField(blank=True, null=True, upload_to="resources/")), ("specifications", models.JSONField(blank=True, default=dict)),
        ("responsibilities", models.JSONField(blank=True, default=dict)), ("is_published", models.BooleanField(default=True)), ("order", models.PositiveIntegerField(default=0)),
    ], options={"verbose_name": "Resource item", "verbose_name_plural": "Resource items", "ordering": ["resource_type", "order", "title"]})]
