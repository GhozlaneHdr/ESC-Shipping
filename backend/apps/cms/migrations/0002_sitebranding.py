from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteBranding",
            fields=[
                (
                    "id",
                    models.PositiveSmallIntegerField(
                        default=1, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("logo", models.ImageField(upload_to="branding/")),
            ],
            options={
                "verbose_name": "Site branding",
                "verbose_name_plural": "Site branding",
            },
        ),
    ]
