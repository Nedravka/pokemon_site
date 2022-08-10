from django.db import models


class Pokemon(models.Model):

    title = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True, default='-')
    title_jp = models.CharField(max_length=200, blank=True, default='-')
    description = models.TextField(default='no data', blank=True)

    evolved_from = models.ForeignKey(
        'pokemon_entities.Pokemon',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='evolve_to',
        default=None
    )

    pokemon_image = models.ImageField(upload_to='pokemon_image', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    longitude = models.FloatField()
    latitude = models.FloatField()

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    attack = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Pokemon entity'
        verbose_name_plural = 'Pokemon entities'
