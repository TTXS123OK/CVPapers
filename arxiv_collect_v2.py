import arxiv
import datetime
import os
import argparse
import shutil

def main(start_date, end_date, order):
    # Initialize the arxiv client
    client = arxiv.Client(
        page_size=1000,
        delay_seconds=3,
        num_retries=5
    )
    
    # Determine the sort order
    sort_order = arxiv.SortOrder.Ascending if order == "ascending" else arxiv.SortOrder.Descending
    
    # Initialize the search query
    search = arxiv.Search(
        query="cat:cs.CV",
        max_results=float('inf'),
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=sort_order
    )
    
    # Initialize counter
    counter = 0
    
    # Buffer to store all articles for sorting
    buffer = []
    
    # Loop through the search results
    for result in client.results(search):
        
        # Increment counter
        counter += 1
    
        published_date = result.published.replace(tzinfo=None)
        
        # Print progress after every 100 papers
        if counter % 100 == 0:
            print(f"Processed {counter} papers. Last processed paper published on {published_date.date()}", flush=True)
    
        # Check end date
        if order == "ascending" and published_date.date() > end_date.date():
            break

        elif order != "ascending" and published_date.date() < start_date.date():
            break
    
        # Filter papers by date (starting from start_date)
        if order == "ascending" and published_date.date() < start_date.date():
            continue

        elif order != "ascending" and published_date.date() > end_date.date():
            continue
    
        # Directory name based on the year and month
        dir_name = os.path.join("CVPapers", str(published_date.year), str(published_date.month).zfill(2))
        
        # Create the directory if it doesn't exist
        os.makedirs(dir_name, exist_ok=True)
        
        # Markdown file name based on the date
        md_file_name = f"{published_date.strftime('%Y%m%d')}.md"
        md_file_path = os.path.join(dir_name, md_file_name)
        
        # Remove file if already exists
        if os.path.exists(md_file_path):
            os.remove(md_file_path)
        
        # Append this paper's information to buffer
        buffer.append((md_file_path, result))
        
    # Sort buffer by date if needed
    if sort_order == arxiv.SortOrder.Descending:
        buffer.sort(key=lambda x: x[1].published)
        
    # Write sorted results to markdown files
    for md_file_path, result in buffer:
        
        if os.path.exists(md_file_path):
            with open(md_file_path, "r") as f:
                md_content = f.read()
        else:
            md_content = f"# Arxiv Papers in cs.CV on {result.published.date()}\n"
        
        # Rest of your markdown file writing logic here...
        
        with open(md_file_path, "w") as f:
            f.write(md_content)
    
    print("Markdown files have been generated.")

if __name__ == "__main__":
    
    # Argument parser for command-line options
    parser = argparse.ArgumentParser(description="Fetch arXiv papers.")
    parser.add_argument("--start", type=str, required=True, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", type=str, required=True, help="End date in YYYY-MM-DD format")
    parser.add_argument("--order", type=str, required=True, choices=["ascending", "descending"], help="Order to sort papers")
    
    args = parser.parse_args()
    
    start_date = datetime.datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(args.end, "%Y-%m-%d")
    order = args.order
    
    # Handle exceptions and rerun the program if needed
    while True:
        try:
            main(start_date, end_date, order)
            break
        except Exception as e:
            print(f"An exception occurred: {e}. Retrying...")
