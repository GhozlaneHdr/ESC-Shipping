from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cms", "0002_sitebranding"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitebranding",
            name="hero_video",
            field=models.FileField(
                blank=True,
                help_text="Optional looping video for the homepage hero background.",
                null=True,
                upload_to="branding/",
            ),
        ),
    ]
