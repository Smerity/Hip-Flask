Hip-Flask: Take a swig
======================

Hip-Flask integrates many standard Flask extensions to provide a solid basis for starting a new project.

Features
--------

- Implemented OpenID through `Flask-OpenID <http://packages.python.org/Flask-OpenID/>`_
- Protected Admin section
- Secure Sessions via `ItsDangerous <http://packages.python.org/itsdangerous/>`_
- Integration of Flask components into `Twitter Bootstrap <http://twitter.github.com/bootstrap/>`_
- Useful extensions including `Markdown <http://daringfireball.net/projects/markdown/syntax>`_ integration for simpler HTML and transparent asset versioning through last-modified timestamps

Before Use
----------

- Create an appropriately strong secret key for use by the application (see: *config.py*)
- (Optional) Set the appropriate options for Flask-SQLAlchemy and Flask-Mail (see: *config.py*)
- Persist the user (see: *oid.py*)
- Make the Admin section more presentable by removing the haxxor access ;) (see: *views.py*)
- Create something useful and prosper!
