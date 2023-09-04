import os
import calendar
from collections import defaultdict

def generate_calendar(base_dir="./cs.CV"):
    years = os.listdir(base_dir)
    years.sort(reverse=True)

    all_markdown = "# Calendar of arXiv papers for cs.CV\n\n"
    
    for year in years:
        year_path = os.path.join(base_dir, year)
        if not os.path.isdir(year_path):
            continue

        all_markdown += f"### {year}\n\n"

        months = os.listdir(year_path)
        months.sort(reverse=True)
        
        # Create a defaultdict to hold all the days where articles are present
        days_with_articles = defaultdict(set)

        for month in months:
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path):
                continue

            articles = os.listdir(month_path)
            for article in articles:
                if article.endswith(".md"):
                    days_with_articles[int(month)].add(int(article[-5:-3]))
                    
            all_markdown += "##### " + calendar.month_name[int(month)] + "\n\n"

            all_markdown += "| Sun | Mon | Tue | Wed | Thu | Fri | Sat |\n"
            all_markdown += "|-----|-----|-----|-----|-----|-----|-----|\n"

            cal = calendar.monthcalendar(int(year), int(month))

            for week in cal:
                week_str = "| "
                for day in week:
                    if day == 0:
                        week_str += "  | "
                    elif day in days_with_articles[int(month)]:
                        week_str += f"[{day}]({base_dir}/{year}/{month.zfill(2)}/{year}{month.zfill(2)}{str(day).zfill(2)}.md) | "
                    else:
                        week_str += f"{day} | "
                all_markdown += week_str + "\n"
            all_markdown += "\n"

    with open("calendar.md", "w") as f:
        f.write(all_markdown)


if __name__ == "__main__":
    generate_calendar()
