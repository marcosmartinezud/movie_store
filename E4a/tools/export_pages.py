import os
import sys


def setup_django():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(this_dir, os.pardir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_store.settings")
    import django

    django.setup()


def collect_pages():
    from django.test import Client
    from movies.models import Movie, Genre, Director

    client = Client()
    urls = ["/"]
    urls += ["/movies/", "/genres/", "/directors/"]

    m = Movie.objects.order_by("pk").first()
    if m:
        urls.append(f"/movies/{m.pk}/")
    g = Genre.objects.order_by("pk").first()
    if g:
        urls.append(f"/genres/{g.pk}/")
    d = Director.objects.order_by("pk").first()
    if d:
        urls.append(f"/directors/{d.pk}/")

    pages = {}
    for u in urls:
        resp = client.get(u)
        if resp.status_code != 200:
            raise SystemExit(f"GET {u} -> {resp.status_code}")
        pages[u] = resp.content.decode("utf-8")
    return pages


def safe_name(path: str) -> str:
    if path == "/":
        return "index.html"
    return path.strip("/").replace("/", "-") + ".html"


def main():
    setup_django()
    pages = collect_pages()

    out_dir = os.path.join(os.getcwd(), "build")
    os.makedirs(out_dir, exist_ok=True)

    for url, html in pages.items():
        name = safe_name(url)
        out_path = os.path.join(out_dir, name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
