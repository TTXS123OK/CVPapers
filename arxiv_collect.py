import arxiv
from datetime import datetime, timedelta
import os
import argparse


def main(start_date, end_date, catalog, order):
    client = arxiv.Client(
        page_size=100,  # or any other number less than or equal to 1000
        delay_seconds=3,
        num_retries=5,
    )

    sort_order = (
        arxiv.SortOrder.Ascending
        if order == "ascending"
        else arxiv.SortOrder.Descending
    )

    search = arxiv.Search(
        query="cat:{}".format(catalog),
        max_results=float("inf"),
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=sort_order,
    )

    buffer = []
    count = 0
    success_offset = 0
    current_date = None

    retry_count = 0

    # Loop through the search results
    while True:
        count = success_offset
        buffer.clear()
        current_date = None

        try:
            for result in client.results(search, offset=success_offset):
                count += 1
                published_date = result.published.replace(tzinfo=None)
                if current_date is None:
                    current_date = published_date
                    
                if published_date.date() != current_date.date() and len(buffer) > 0:
                    write_to_md(buffer)
                    print(
                        f"Processed {count-1} papers. Last processed paper published on {current_date.date()}",
                        flush=True,
                    )
                    success_offset = count
                    current_date = published_date

                if (
                    order == "ascending" and published_date.date() > end_date.date()
                ) or (
                    order != "ascending" and published_date.date() < start_date.date()
                ):
                    print("All Markdown files have been generated.")
                    exit(0)

                if (
                    order == "ascending" and published_date.date() < start_date.date()
                ) or (order != "ascending" and published_date.date() > end_date.date()):
                    continue

                buffer.append(result)
                retry_count = 0

        except Exception as e:
            print(f"An exception occurred: {e}. Retrying...")
            retry_count += 1
            if retry_count >= 5:
                print("Reached maximum number of retries. Exiting.")
                exit(1)

            continue


def write_to_md(buffer):
    date = buffer[0].published
    dir_name = os.path.join(
        catalog,
        str(date.year),
        str(date.month).zfill(2),
    )
    os.makedirs(dir_name, exist_ok=True)
    md_file_name = f"{date.strftime('%Y%m%d')}.md"
    md_file_path = os.path.join(dir_name, md_file_name)

    if os.path.exists(md_file_path):
        os.remove(md_file_path)

    buffer.sort(key=lambda x: x.published)

    for result in buffer:
        if os.path.exists(md_file_path):
            with open(md_file_path, "r") as f:
                md_content = f.read()
        else:
            md_content = f"# Arxiv Papers in cs.CV on {result.published.date()}\n"

        # Append this paper's information to Markdown content
        md_content += "### {}\n".format(result.title)
        md_content += "- **Arxiv ID**: {}\n".format(result.entry_id)
        md_content += "- **DOI**: {}\n".format(result.doi)
        md_content += "- **Categories**: "

        # Highlight the primary category
        for cat in result.categories:
            if cat == result.primary_category:
                md_content += "**{}**".format(cat)
            else:
                md_content += cat
            md_content += ", "
        md_content = md_content.rstrip(", ")  # Remove trailing comma and space
        md_content += "\n"

        md_content += "- **Links**: [PDF]({})\n".format(result.pdf_url)
        md_content += "- **Published**: {}\n".format(result.published)
        md_content += "- **Updated**: {}\n".format(result.updated)
        md_content += "- **Authors**: {}\n".format(
            ", ".join(author.name for author in result.authors)
        )
        md_content += "- **Comment**: {}\n".format(result.comment)
        md_content += "- **Journal**: {}\n".format(result.journal_ref)
        md_content += "- **Summary**: {}\n".format(result.summary.replace("\n", " "))
        md_content += "\n\n\n"

        with open(md_file_path, "w") as f:
            f.write(md_content)

    # Clear Buffer
    buffer.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch arXiv papers.")
    parser.add_argument(
        "--start_date",
        default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        type=str,
        help="Start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end_date",
        default=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        type=str,
        help="End date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--catalog",
        default="cs.CV",
        type=str,
        help="Specify arXiv catalog",
    )
    parser.add_argument(
        "--order",
        default="descending",
        type=str,
        choices=["ascending", "descending"],
        help="Order to sort papers",
    )
    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    catalog = args.catalog
    order = args.order

    main(start_date, end_date, catalog, order)
