from django.db import models


class Pokemon(models.Model):

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='название покемона'
    )
    title_en = models.CharField(
        max_length=200,
        blank=True,
        default='-',
        verbose_name='название на английском'
    )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        default='-',
        verbose_name='название на японском'
    )
    description = models.TextField(
        default='no data',
        blank=True,
        verbose_name='описание'
    )

    evolved_from = models.ForeignKey(
        'pokemon_entities.Pokemon',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='evolve_to',
        default=None,
        verbose_name='предыдущая эволюция'
    )

    pokemon_image = models.ImageField(
        upload_to='pokemon_image',
        null=True, blank=True,
        verbose_name='изображение покемона'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):

    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name='покемон'
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='долгота'
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        verbose_name='широта'
    )

    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='появится'
    )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='пропадет'
    )

    level = models.IntegerField(default=1, verbose_name='уровень')
    health = models.IntegerField(default=1, verbose_name='здоровье')
    attack = models.IntegerField(default=1, verbose_name='атака')
    defence = models.IntegerField(default=1, verbose_name='защита')
    stamina = models.IntegerField(default=1, verbose_name='выносливость')

    class Meta:
        verbose_name = 'Pokemon entity'
        verbose_name_plural = 'Pokemon entities'
