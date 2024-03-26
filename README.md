# Patterns of lymphatic spread in hypopharyngeal and laryngeal squamous cell carcinoma

In this repository, we store the code and pipeline to create the figures for a poster we present at [ESTRO 2024].

[ESTRO 2024]: https://www.estro.org/Congresses/ESTRO-2024


## How to Reproduce the Figures

Follow the steps below to recreate the figures for yourself. This is not strictly necessary, because all the figures are already present in the repository. But just in case you want to make sure they are correct, or you want to create them for new data, here's how to recreate them:


### Requirements

First, make sure you have Python 3.10 or higher by typing the following command in your terminal:

```
python --version
```

If printed version is less than 3.10, head over to the [Python downloads page] and install the latest version.

With that out of the way, go ahead and clone this repository by running these four commands:

```
git clone https://github.com/rmnldwg/2024-estro-data-poster
cd 2024-estro-data-poster
python -m venv .venv
source .venv/bin/activate
```

With them, you clone (i.e., download) the repository, change your working directory to be inside of it, create a virtual Python environment and lastly activate that environment. If everything went well you should see a `(.venv)` at the start of the current line in your terminal.

Now, install the Python packages necessary to run the pipeline by running the two commands below one after the other. There will be quite some output after each one.

```
pip install -U pip
pip install -r requirements.txt
```

Now you're ready to reproduce the figures by simply executing this command:

```
dvc repro
```

When this is finished, you should find the generated figures inside the `figures` folder.


[Python downloads page]: https://www.python.org/downloads/
