from django.db import models  # noqa F401


class Pokemon(models.Model):

    title = models.CharField(max_length=200, blank=True)

    pokemon_image = models.ImageField(upload_to='pokemon_image',null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):

    longitude = models.FloatField()
    latitude = models.FloatField()
