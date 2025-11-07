import os
import sys
import json
import urllib.request
import urllib.parse


def post_nu_validator(html: str):
    url = "https://validator.w3.org/nu/?out=json"
    data = html.encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "User-Agent": "movie-store-validator/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        payload = resp.read().decode("utf-8")
    return json.loads(payload)


def validate_css_text(css_text: str):
    # W3C CSS validator endpoint
    base = "https://jigsaw.w3.org/css-validator/validator"
    # Try POST first
    try:
        url = base + "?output=json&warning=0&profile=css3svg"
        data = urllib.parse.urlencode({"text": css_text}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8")
        return json.loads(payload)
    except Exception:
        # Fallback to GET
        params = urllib.parse.urlencode({
            "output": "json",
            "warning": "0",
            "profile": "css3svg",
            "text": css_text,
        })
        with urllib.request.urlopen(base + "?" + params) as resp:
            payload = resp.read().decode("utf-8")
        return json.loads(payload)


def setup_django():
    # Ensure project root is on sys.path (parent of this file's directory)
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

    # Add details for first of each type if available
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
        pages[u] = resp.content.decode("utf-8")
    return pages


def main():
    setup_django()

    # Validate HTML pages
    pages = collect_pages()
    html_report = {}
    had_html_errors = False
    for path, html in pages.items():
        result = post_nu_validator(html)
        messages = result.get("messages", [])
        errors = [m for m in messages if m.get("type") == "error"]
        warnings = [m for m in messages if m.get("type") == "info" and m.get("subType") == "warning"]
        html_report[path] = {"errors": errors, "warnings": warnings}
        if errors:
            had_html_errors = True

    # Validate CSS
    css_path = os.path.join("movies", "static", "movies", "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css_text = f.read()
    css_errors = []
    css_warnings = []
    try:
        css_result = validate_css_text(css_text)
        css_val = css_result.get("cssvalidation", {})
        css_errors = css_val.get("errors", [])
        css_warnings = css_val.get("warnings", [])
    except Exception as e:
        print("CSS validator request failed:", e)
        print("Continuing without CSS errors; please retry if needed.")

    # Print summary
    print("HTML Validation Summary:")
    for path, rep in html_report.items():
        print(f"- {path}: {len(rep['errors'])} errors, {len(rep['warnings'])} warnings")
        for e in rep["errors"]:
            msg = e.get("message")
            extract = e.get("extract")
            lastLine = e.get("lastLine")
            print(f"  error L{lastLine}: {msg}")
            if extract:
                print(f"    > {extract}")
    print()

    print("CSS Validation Summary:")
    print(f"- styles.css: {len(css_errors)} errors, {len(css_warnings)} warnings")
    for e in css_errors:
        line = e.get("line")
        msg = e.get("message")
        print(f"  error L{line}: {msg}")
    for w in css_warnings or []:
        line = w.get("line")
        msg = w.get("message")
        level = w.get("level")
        print(f"  warn  L{line}: [{level}] {msg}")

    # Exit non-zero if errors found to signal CI or script usage
    if had_html_errors or css_errors:
        sys.exit(2)


if __name__ == "__main__":
    main()
