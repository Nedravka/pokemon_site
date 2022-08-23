import folium

from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    all_existing_pokemon_entities = PokemonEntity.objects.select_related(
        'pokemon'
    ).filter(
        disappeared_at__gt=localtime(),
        appeared_at__lte=localtime(),
    )
    pokemons_titles = set(pokemon_entity.pokemon for
                          pokemon_entity in all_existing_pokemon_entities)

    for pokemon_entity in all_existing_pokemon_entities:

        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []

    for pokemon in pokemons_titles:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': (
                request.build_absolute_uri(pokemon.image.url)
                if pokemon.image
                else None
            ),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemon_type = Pokemon.objects.select_related(
        'evolved_from'
    ).prefetch_related(
        Prefetch(
            'entities',
            queryset=PokemonEntity.objects.filter(
                disappeared_at__gt=localtime(),
                appeared_at__lte=localtime(),
            ),
            to_attr='pokemons'
        )
    ).get(
        id=int(pokemon_id),
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entity = {
        'pokemon_id': pokemon_type.id,
        'title_ru': pokemon_type.title,
        'title_en': pokemon_type.title_en,
        'title_jp': pokemon_type.title_jp,
        'description': pokemon_type.description,
        'img_url': request.build_absolute_uri(pokemon_type.image.url),
    }

    try:
        evolve_to = pokemon_type.evolve_to.get()
        next_evol = {"next_evolution": {
            "title_ru": evolve_to.title,
            "pokemon_id": evolve_to.id,
            "img_url": request.build_absolute_uri(evolve_to.image.url),
        }}
        pokemon_entity.update(next_evol)

    except ObjectDoesNotExist:
        pass

    try:
        prev_evol = {"previous_evolution": {
            "title_ru": pokemon_type.evolved_from.title,
            "pokemon_id": pokemon_type.evolved_from.id,
            "img_url": request.build_absolute_uri(
                pokemon_type.evolved_from.image.url
            ),
        }}
        pokemon_entity.update(prev_evol)

    except AttributeError:
        pass

    for pokemon in pokemon_type.pokemons:

        add_pokemon(
            folium_map,
            pokemon.latitude,
            pokemon.longitude,
            request.build_absolute_uri(pokemon_type.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_entity
    })
