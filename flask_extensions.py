import flask
from app import app

import markdown
import os

# See http://flask.pocoo.org/snippets/40/ (static cache buster)
## TODO: Caching should occur on the file time as otherwise os.stat is called every request
@app.context_processor
def _context_hash_url_for():
  return dict(dated_url_for=dated_url_for)

@app.context_processor
def _context_inject_models():
  import models
  return dict(models=models)

def dated_url_for(endpoint, **values):
  if endpoint == "static":
    filename = values.get("filename", None)
    if filename:
      file_path = os.path.join(app.root_path, endpoint, filename)
      values["q"] = int(os.stat(file_path).st_mtime)
    return flask.url_for(endpoint, **values)

## Markdown filter and render

md = markdown.Markdown()
@app.template_filter("markdown")
def render_markdown(content):
  return flask.Markup(md.convert(content))
