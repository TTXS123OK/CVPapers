# ArXiv Paper Collector for cs.CV

## Introduction

This project is designed to fetch and catalog academic papers from the cs.CV domain on arXiv. Utilizing the arXiv API in compliance with its [Terms of Use](https://info.arxiv.org/help/api/tou.html), the project leverages the Python library [arxiv](https://github.com/lukasschwab/arxiv.py) for execution. The aim is to maintain a daily updated collection of paper abstracts from this particular field.

## Features

- **Automated Daily Updates**: This project is set to automatically fetch new paper abstracts from the cs.CV domain each day.
  
- **Comprehensive Catalog**: Attempts to collect all papers from the cs.CV domain that are available through the arXiv API.

- **Markdown Format**: The fetched paper details are saved in Markdown files, organized by publication date.

- **Interactive Calendar**: Navigate through an [interactive calendar](calendar.md) to easily find papers published on specific dates.

## Limitations

Due to restrictions on the arXiv API, the data from December 8, 2020, to March 5, 2021, is currently missing from the collection. If anyone has a workaround or solution for this, contributions are greatly appreciated.

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
