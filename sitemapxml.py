from urllib.parse import urlparse
from os.path import isfile
import bs4, traceback

robots = open("robots.txt", "r").read()
out = open("sitemap.xml", "w")
out.write(
    """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">"""
)
input = open("sitemap.txt", "r").read()
robolist = robots.split("\n")
for i in range(3):
    print(robolist)
    robostat = robolist.copy()
    for r in robostat:
        if "user-agent" in r.lower() or "sitemap" in r.lower() or len(r) < 1:
            try:
                robolist.remove(r)
            except ValueError:
                pass
        else:
            try:
                robolist[robolist.index(r)] = r.replace("Disallow: ", "")
            except ValueError:
                pass
print("Parsed robolist:")
print(robolist)
for url in input.split("\n"):
    url = url.replace("/schoology/", "/schoology.css")
    print("Parsing url " + urlparse(url).path)
    allowed = True
    for rob in robolist:
        if rob in urlparse(url).path:
            print("Nope says", rob)
            allowed = False
    if "https://ktibow.github.io/" in url and (
        allowed or url == "https://ktibow.github.io/"
    ):
        out.write(
            """<url>
<loc>"""
            + url
            + """</loc>
"""
        )
        try:
            imgs = []
            the_path = urlparse(url).path.replace("/", "", 1) + "index.html"
            print("Path:", the_path)
            if the_path in [
                "schoology/index.html",
                "schoologyindex.html",
                "schoology.cssindex.html",
            ]:
                the_path = "schoology.css.html"
            soup = bs4.BeautifulSoup(
                open(the_path).read(),
                "html.parser",
            )
            for img in soup.find_all("img"):
                if urlparse(img["src"]).netloc in ["ktibow.github.io", ""] and isfile(
                    urlparse(img["src"]).path.replace("/", "", 1)
                ):
                    imgs.append("https://ktibow.github.io" + urlparse(img["src"]).path)
                    print(
                        "Image:", "https://ktibow.github.io" + urlparse(img["src"]).path
                    )
            for img in imgs:
                out.write(
                    """<image:image>
<image:loc>"""
                    + img
                    + """</image:loc>
</image:image>
"""
                )
        except Exception:
            print(traceback.format_exc())
        out.write("<priority>")
        priority = 0.5
        if url in ["https://ktibow.github.io/"]:
            priority = 0.9
        if url.count("/") == 4:
            priority = 0.7
        if "blog" in url and url.count("/") < 7 and url.count("/") > 4:
            priority = 0.3
        print("Priority:", priority)
        out.write(
            "0."
            + str(round(priority * 100))
            + """</priority>
</url>
"""
        )
out.write("</urlset>")
out.close()
