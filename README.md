# ArXiv Paper Collector for cs.CV

## Introduction

This project is designed to fetch and catalog academic papers from the cs.CV domain on arXiv. Utilizing the arXiv API in compliance with its [Terms of Use](https://info.arxiv.org/help/api/tou.html), the project leverages the Python library [arxiv](https://github.com/lukasschwab/arxiv.py) for execution. The aim is to maintain a daily updated collection of paper abstracts from this particular field.

## Features

- **Automated Daily Updates**: This project is set to automatically fetch new paper abstracts from the cs.CV domain each day.
  
- **Comprehensive Catalog**: Attempts to collect all papers from the cs.CV domain that are available through the arXiv API.

- **Markdown Format**: The fetched paper details are saved in Markdown files, organized by publication date.

- **Interactive Calendar**: Navigate through an [interactive calendar](calendar.md) to easily find papers published on specific dates.

## Limitations

Please note that data is missing for two periods: from 2020-12-08 to 2021-03-05 (due to arXiv API restrictions) and from 2025-05-31 to 2025-06-18 (due to a repository crash). If you have any workarounds or solutions, contributions are highly welcome.

## Disclaimer

If there are any issues related to copyright infringement or improper behavior, please contact the repository owner promptly for immediate removal.

## Dependencies

- Python 3.x
- arxiv library

## Setup

1. Install the required Python library with `pip install arxiv`.

2. Run the Python script to begin fetching papers:
   ```bash
   python arxiv_collect.py --catalog cs.CV --start_date YYYY-MM-DD --end_date YYYY-MM-DD --order desending
