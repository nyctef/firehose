realtime centralized rss/chat/twitter/notification/whatever tracking

- create python27 virtualenv at `env/`
- `pip install -r requirements.txt` to get dependencies
  - use http://www.lfd.uci.edu/~gohlke/pythonlibs/ for psycopg2/gevent on windows
- see `config.py` for config details
  - either create environment variables or write to `config_local.py`
  - make sure to set a SECRET_KEY for flask to use
- `. activate.sh` to activate
- `./tests.sh` to run tests
