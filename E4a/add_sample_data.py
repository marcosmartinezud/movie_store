from movies.models import Director, Genre, Movie

# Limpieza opcional
Director.objects.all().delete()
Genre.objects.all().delete()
Movie.objects.all().delete()

# Géneros
genres = {
    "Acción": "Películas llenas de adrenalina y escenas de combate.",
    "Drama": "Historias centradas en el desarrollo emocional de los personajes.",
    "Ciencia Ficción": "Futuros imaginarios, tecnología avanzada y universos paralelos.",
    "Comedia": "Películas diseñadas para hacerte reír.",
    "Suspense": "Historias con tensión y giros inesperados.",
}
genre_objs = {name: Genre.objects.create(name=name, description=desc) for name, desc in genres.items()}

# Directores base
directors = [
    {
        "name": "Christopher Nolan",
        "biography": "Director británico conocido por películas complejas y visualmente impactantes.",
        "birth_date": "1970-07-30",
    },
    {
        "name": "Quentin Tarantino",
        "biography": "Director estadounidense famoso por su estilo narrativo no lineal y diálogos únicos.",
        "birth_date": "1963-03-27",
    },
    {
        "name": "Denis Villeneuve",
        "biography": "Director canadiense reconocido por su trabajo en ciencia ficción y thrillers psicológicos.",
        "birth_date": "1967-10-03",
    },
    {
        "name": "Greta Gerwig",
        "biography": "Directora y actriz estadounidense, conocida por su estilo naturalista y narrativas femeninas.",
        "birth_date": "1983-08-04",
    },
    {
        "name": "The Wachowskis",
        "biography": "Lana y Lilly Wachowski, directoras estadounidenses famosas por combinar acción, filosofía y ciencia ficción.",
        "birth_date": None,
    },
    {
        "name": "Edgar Wright",
        "biography": "Director británico con un estilo visual muy distintivo y ritmo de comedia dinámica.",
        "birth_date": "1974-04-18",
    },
    {
        "name": "Bong Joon-ho",
        "biography": "Director surcoreano conocido por mezclar géneros y crítica social en sus películas.",
        "birth_date": "1969-09-14",
    },
]

# Usar update_or_create para garantizar que se rellene la biografía/fecha
for d in directors:
    Director.objects.update_or_create(
        name=d["name"], defaults={"biography": d["biography"], "birth_date": d["birth_date"]}
    )

# Películas
movies = [
    {
        "title": "Inception",
        "release_year": 2010,
        "description": "Un ladrón que roba secretos corporativos mediante el uso de tecnología de sueños.",
        "poster": "https://m.media-amazon.com/images/I/81p+xe8cbnL._AC_SL1500_.jpg",
        "genre": genre_objs["Ciencia Ficción"],
        "directors": ["Christopher Nolan"],
    },
    {
        "title": "Interstellar",
        "release_year": 2014,
        "description": "Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en busca de un nuevo hogar para la humanidad.",
        "poster": "https://m.media-amazon.com/images/I/91obuWzA3XL.jpg",
        "genre": genre_objs["Ciencia Ficción"],
        "directors": ["Christopher Nolan"],
    },
    {
        "title": "Pulp Fiction",
        "release_year": 1994,
        "description": "Historias entrelazadas de crimen, redención y humor negro en Los Ángeles.",
        "poster": "https://m.media-amazon.com/images/I/71c05lTE03L._AC_SL1181_.jpg",
        "genre": genre_objs["Suspense"],
        "directors": ["Quentin Tarantino"],
    },
    {
        "title": "Arrival",
        "release_year": 2016,
        "description": "Una lingüista es reclutada para comunicarse con visitantes alienígenas.",
        "poster": "https://m.media-amazon.com/images/I/41oKKo0YZZL._AC_UF894,1000_QL80_.jpg",
        "genre": genre_objs["Ciencia Ficción"],
        "directors": ["Denis Villeneuve"],
    },
    {
        "title": "Little Women",
        "release_year": 2019,
        "description": "Adaptación del clásico de Louisa May Alcott sobre la vida de las hermanas March.",
        "poster": "https://m.media-amazon.com/images/I/71BrrTUCFPL._AC_UF894,1000_QL80_.jpg",
        "genre": genre_objs["Drama"],
        "directors": ["Greta Gerwig"],
    },
    {
        "title": "Parasite",
        "release_year": 2019,
        "description": "Una familia pobre se infiltra en la vida de una familia rica con consecuencias inesperadas.",
        "poster": "https://i.etsystatic.com/18242346/r/il/87bc12/2184703308/il_fullxfull.2184703308_jpnu.jpg",
        "genre": genre_objs["Drama"],
        "directors": ["Bong Joon-ho"],
    },
    {
        "title": "The Matrix",
        "release_year": 1999,
        "description": "Un hacker descubre la verdad sobre la realidad y lidera la rebelión contra las máquinas.",
        "poster": "https://www.tuposter.com/pub/media/catalog/product/cache/71d04d62b2100522587d43c930e8a36b/m/a/matrix_posters.png",
        "genre": genre_objs["Acción"],
        "directors": ["The Wachowskis"],
    },
    {
        "title": "John Wick",
        "release_year": 2014,
        "description": "Un exasesino a sueldo busca venganza tras el asesinato de su perro, regalo de su difunta esposa.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTU2NjA1ODgzMF5BMl5BanBnXkFtZTgwMTM2MTI4MjE@._V1_FMjpg_UX1000_.jpg",
        "genre": genre_objs["Acción"],
        "directors": ["Chad Stahelski", "David Leitch"],
    },
    {
        "title": "Baby Driver",
        "release_year": 2017,
        "description": "Un joven conductor experto en fugas busca escapar de la vida criminal con la ayuda de su amor.",
        "poster": "https://m.media-amazon.com/images/I/81cSHhNL7IL._AC_UF1000,1000_QL80_.jpg",
        "genre": genre_objs["Comedia"],
        "directors": ["Edgar Wright"],
    },
    {
        "title": "Knives Out",
        "release_year": 2019,
        "description": "Un detective investiga la muerte del patriarca de una excéntrica familia.",
        "poster": "https://m.media-amazon.com/images/M/MV5BZDU5ZTRkYmItZjg0Mi00ZTQwLThjMWItNWM3MTMxMzVjZmVjXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "genre": genre_objs["Suspense"],
        "directors": ["Rian Johnson"],
    },
]

# Películas adicionales
movies.extend(
    [
        {
            "title": "Shrek",
            "release_year": 2001,
            "description": "Un ogro solitario emprende una aventura para rescatar a una princesa y recuperar la tranquilidad de su pantano.",
            "poster": "https://m.media-amazon.com/images/I/81Hw13F3nSL._AC_UF894,1000_QL80_.jpg",
            "genre": genre_objs["Comedia"],
            "directors": ["Andrew Adamson", "Vicky Jenson"],
        },
        {
            "title": "Fight Club",
            "release_year": 1999,
            "description": "Un oficinista insomne y un vendedor carismático forman un club de lucha clandestino que se sale de control.",
            "poster": "https://upload.wikimedia.org/wikipedia/en/f/fc/Fight_Club_poster.jpg",
            "genre": genre_objs["Drama"],
            "directors": ["David Fincher"],
        },
        {
            "title": "Inglourious Basterds",
            "release_year": 2009,
            "description": "Un grupo de soldados aliados planea acabar con altos mandos nazis mientras una joven busca venganza en la Francia ocupada.",
            "poster": "https://upload.wikimedia.org/wikipedia/en/c/c3/Inglourious_Basterds_poster.jpg",
            "genre": genre_objs["Suspense"],
            "directors": ["Quentin Tarantino"],
        },
        {
            "title": "Casablanca",
            "release_year": 1942,
            "description": "En la ciudad marroquí de Casablanca, un cínico propietario de un club nocturno se enfrenta a un dilema cuando su antiguo amor reaparece junto a su esposo, un líder de la resistencia.",
            "poster": "/static/movies/posters/casablanca.jpg",
            "genre": genre_objs["Drama"],
            "directors": ["Michael Curtiz"],
        },
    ]
)

# Directores adicionales (incluye los que faltaban con datos completos)
extra_directors = {
    "Chad Stahelski": {
        "name": "Chad Stahelski",
        "biography": "Director y doble de acción estadounidense, conocido por la saga John Wick.",
        "birth_date": "1968-09-20",
    },
    "David Leitch": {
        "name": "David Leitch",
        "biography": "Director, productor y actor especializado en cine de acción.",
        "birth_date": "1975-11-16",
    },
    "Rian Johnson": {
        "name": "Rian Johnson",
        "biography": "Director estadounidense conocido por su estilo original en películas de misterio y ciencia ficción.",
        "birth_date": "1973-12-17",
    },
    "David Fincher": {
        "name": "David Fincher",
        "biography": "Director estadounidense conocido por thrillers como Seven y Fight Club.",
        "birth_date": "1962-08-28",
    },
    "Andrew Adamson": {
        "name": "Andrew Adamson",
        "biography": "Director y guionista neozelandés, codirector de Shrek.",
        "birth_date": "1966-12-01",
    },
    "Vicky Jenson": {
        "name": "Vicky Jenson",
        "biography": "Directora y artista estadounidense, codirectora de Shrek.",
        "birth_date": "1960-03-04",
    },
    "Michael Curtiz": {
        "name": "Michael Curtiz",
        "biography": "Director estadounidense de origen húngaro, ganador del Óscar por Casablanca.",
        "birth_date": "1886-12-24",
    },
}

for d in extra_directors.values():
    Director.objects.update_or_create(
        name=d["name"], defaults={"biography": d["biography"], "birth_date": d["birth_date"]}
    )

# Crear películas
for m in movies:
    movie = Movie.objects.create(
        title=m["title"],
        release_year=m["release_year"],
        description=m["description"],
        poster=m["poster"],
        genre=m["genre"],
    )
    movie.directors.set(Director.objects.filter(name__in=m["directors"]))

print("Películas, géneros y directores cargados correctamente.")

