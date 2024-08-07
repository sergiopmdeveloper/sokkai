# Generated by Django 5.0.7 on 2024-08-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('league', models.CharField(max_length=50)),
                ('team1', models.CharField(max_length=50)),
                ('team2', models.CharField(max_length=50)),
                ('spi1', models.FloatField()),
                ('spi2', models.FloatField()),
                ('prob1', models.FloatField()),
                ('prob2', models.FloatField()),
                ('probtie', models.FloatField()),
                ('proj_score1', models.FloatField()),
                ('proj_score2', models.FloatField()),
                ('score1', models.FloatField(blank=True, null=True)),
                ('score2', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
    ]