from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_currency',
            field=djmoney.models.fields.CurrencyField(
                choices=[('USD', '$'), ('EUR', '€'), ('₽', '₽')], default='₽',
                editable=False, max_length=3),
        ),
    ]
