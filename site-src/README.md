# jackassmeshworks.com

`../site` is the live website, served by Cloudflare Pages (build output directory: `site`, no build command).

`build.py` writes the HTML pages into `../site`. Page text, plugins and links live at the top of that file.
To add a plugin, add an entry to `PLUGINS`, put its art in `site/assets/<slug>/`, and run:

    python site-src/build.py

Styles are in `site/css/site.css`.
