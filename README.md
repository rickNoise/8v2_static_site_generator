# 8v2_static_site_generator
A static site generator project for boot.dev.

Place markdown files in the `content/` folder.
Each markdown file will become an html webpage.
The directory hierarchy will be reflected in the html output files generated in the `docs/` folder.

The generator should respect all "Basic Syntax" for markdown.
Note that nested inline elements (e.g. `_this is **bold** inside italics_`) are not supported.
Note that nested block-level elements (e.g. a block quote within a blockquote) are not supported.

Any images referenced in the markdown files can be store in static.

Run `main.sh` to generate html files locally and serve website on local port 8888.
