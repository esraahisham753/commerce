# Generated by Django 5.1.4 on 2025-01-02 17:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bid_id_alter_comment_id_alter_listing_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist_user',
            field=models.ManyToManyField(related_name='watchlist_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
