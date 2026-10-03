from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("cms", "0004_resourceitem")]

    operations = [
        migrations.AlterField(
            model_name="resourceitem",
            name="resource_type",
            field=models.CharField(
                choices=[
                    ("container", "Container"),
                    ("air_freight", "Air freight"),
                    ("aircraft", "Aircraft"),
                    ("incoterm", "Incoterm"),
                    ("load_chart", "Load chart"),
                ],
                max_length=20,
            ),
        ),
    ]
