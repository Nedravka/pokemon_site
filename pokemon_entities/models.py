from django.db import models


class Pokemon(models.Model):

    title = models.CharField(max_length=200, blank=True)

    pokemon_image = models.ImageField(upload_to='pokemon_image', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    longitude = models.FloatField()
    latitude = models.FloatField()

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
