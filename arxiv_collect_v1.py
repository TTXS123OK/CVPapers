import arxiv
import datetime
import os

# Initialize the arxiv client
client = arxiv.Client(
    page_size=100,
    delay_seconds=5,
    num_retries=5
)

# Initialize the search query
search = arxiv.Search(
    query="cat:cs.CV",
    max_results=float('inf'),
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Ascending
)

# Define the start and end dates you're interested in
start_date = datetime.datetime(2020, 12, 8)
end_date = datetime.datetime(2023, 9, 1)  # Change this to your desired end date

# Initialize counter
counter = 0

# Loop through the search results
for result in client.results(search):
    
    # Increment counter
    counter += 1

    published_date = result.published.replace(tzinfo=None)
    
    # Print progress after every 1000 papers
    if counter % 100 == 0:
        print("Processed {} papers. Last processed paper published on {}".format(counter, published_date.date()), flush=True)

    # Check end date
    if published_date.date() > end_date.date():
        break

    # Filter papers by date (starting from start_date)
    if published_date.date() < start_date.date():
        continue

    # Directory name based on the year and month
    dir_name = os.path.join("CVPapers", str(published_date.year), str(published_date.month).zfill(2))
    
    # Create the directory if it doesn't exist
    os.makedirs(dir_name, exist_ok=True)
    
    # Markdown file name based on the date
    md_file_name = "{}.md".format(published_date.strftime("%Y%m%d"))
    md_file_path = os.path.join(dir_name, md_file_name)
    
    # Initialize or read existing Markdown content
    if os.path.exists(md_file_path):
        with open(md_file_path, "r") as f:
            md_content = f.read()
    else:
        md_content = "# Arxiv Papers in cs.CV on {}\n".format(published_date.date())
    
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
    md_content += "- **Authors**: {}\n".format(", ".join(author.name for author in result.authors))
    md_content += "- **Comment**: {}\n".format(result.comment)
    md_content += "- **Journal**: {}\n".format(result.journal_ref)
    md_content += "- **Summary**: {}\n".format(result.summary.replace("\n", " "))
    md_content += "\n\n\n"
    
    # Save the markdown content to a file
    with open(md_file_path, "w") as f:
        f.write(md_content)

print("Markdown files have been generated.")
