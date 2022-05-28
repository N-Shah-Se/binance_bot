import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0002_alter_profile_account_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 23, 12, 45, 59, 289257)),
        ),
    ]
