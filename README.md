# CRISIS Scrapers

This repository contains the web scraper utilities to scrape the data (course, major, minor, HASS, etc.) from various RPI webpages and compile it into a useful format.

## Scrapers

- [ ] Individual courses
- [ ] Major
- [ ] Minor
- [ ] HASS Pathways

## Infrastructure

- [ ] GitHub action or similar to run scrapers and commit to [the data repository](https://github.com/rpi-crisis/data).

## Getting set up

Make sure you have python and pip installed first before running the following.

```sh
git clone git@github.com:rpi-crisis/scraper.git
cd scraper/
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

To run the course scraper:

```sh
python src/course.py
```
