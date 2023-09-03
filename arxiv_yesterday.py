import arxiv
import datetime
import os

# Initialize the arxiv client
client = arxiv.Client(
    page_size=100,
    delay_seconds=3,
    num_retries=5
)

# Initialize the search query
search = arxiv.Search(
    query="cat:cs.CV",
    max_results=float('inf'),
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

# Get yesterday's date
yest = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday = datetime.datetime(yest.year, yest.month, yest.day)

# Initialize paper list for the day
papers_for_the_day = []

# Loop through the search results
for result in client.results(search):

    published_date = result.published.replace(tzinfo=None)

    # Stop if we have passed the target date
    if published_date.date() < yesterday.date():
        break

    # Continue to next iteration if paper is not from yesterday
    if published_date.date() != yesterday.date():
        continue
    
    # Add this paper's information to papers list
    paper_info = {
        'title': result.title,
        'entry_id': result.entry_id,
        'doi': result.doi,
        'categories': result.categories,
        'primary_category': result.primary_category,
        'pdf_url': result.pdf_url,
        'published': result.published,
        'updated': result.updated,
        'authors': ", ".join(author.name for author in result.authors),
        'comment': result.comment,
        'journal_ref': result.journal_ref,
        'summary': result.summary.replace("\n", " ")
    }
    papers_for_the_day.append(paper_info)

# Sort papers_for_the_day based on the published time
papers_for_the_day.sort(key=lambda x: x['published'])

# Directory and Markdown file naming
dir_name = os.path.join("CVPapers", str(yesterday.year), str(yesterday.month).zfill(2))
os.makedirs(dir_name, exist_ok=True)
md_file_name = "{}.md".format(yesterday.strftime("%Y%m%d"))
md_file_path = os.path.join(dir_name, md_file_name)

# Initialize Markdown content
md_content = "# Arxiv Papers in cs.CV on {}\n".format(yesterday.date())

# Add papers to Markdown content
for paper in papers_for_the_day:
    md_content += "### {}\n".format(paper['title'])
    md_content += "- **Arxiv ID**: {}\n".format(paper['entry_id'])
    md_content += "- **DOI**: {}\n".format(paper['doi'])
    md_content += "- **Categories**: "
    
    for cat in paper['categories']:
        if cat == paper['primary_category']:
            md_content += "**{}**".format(cat)
        else:
            md_content += cat
        md_content += ", "
    
    md_content = md_content.rstrip(", ")
    md_content += "\n"
    md_content += "- **Links**: [PDF]({})\n".format(paper['pdf_url'])
    md_content += "- **Published**: {}\n".format(paper['published'])
    md_content += "- **Updated**: {}\n".format(paper['updated'])
    md_content += "- **Authors**: {}\n".format(paper['authors'])
    md_content += "- **Comment**: {}\n".format(paper['comment'])
    md_content += "- **Journal**: {}\n".format(paper['journal_ref'])
    md_content += "- **Summary**: {}\n".format(paper['summary'])
    md_content += "\n\n\n"

# Save the markdown content to a file
with open(md_file_path, "w") as f:
    f.write(md_content)

print("Markdown files have been generated.")
