In order to use this

    pip install jupyter_config

Which is then executed as

    jupyter config "your_search_term"

on the command line to search for "`your_search_term`".

If you pass just

    jupyter config

it will return the total list of configuration files that it found relative to
the directory that you are running the command from (not just the directories,
which you can find using `jupyter --paths` beneath `config:`).
