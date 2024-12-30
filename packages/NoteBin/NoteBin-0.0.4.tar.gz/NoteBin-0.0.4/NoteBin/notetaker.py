import requests
import re
import os

def fetch_paper_info(title):
    """
    Fetch paper information from the Semantic Scholar API based on the title.

    Args:
        title (str): The title of the paper to search.

    Returns:
        dict: A dictionary containing the paper's title, year, citations, abstract,
              first author, author's affiliation, corresponding author, contact info,
              and the paper's link. Returns None if no information is found.
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={title}&fields=title,year,citationCount,abstract,authors,url"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            # Extract the first matched paper's information
            paper = data["data"][0]
            authors = paper.get("authors", [])
            
            # First Author info
            first_author = authors[0].get("name", "N/A") if authors else "N/A"
            first_author_affiliation = authors[0].get("affiliation", "N/A") if authors else "N/A"
            
            # Corresponding Author info (not always available)
            corresponding_author = None
            contact_info = None
            if len(authors) > 1:  # Assuming the second author is the corresponding author
                corresponding_author = authors[1].get("name", "N/A")
                contact_info = authors[1].get("contact", "N/A")  # Some papers may include contact info

            # Get the full abstract
            abstract = paper.get("abstract", "N/A")
            
            return {
                "Title": paper.get("title", "N/A"),
                "Year": paper.get("year", "N/A"),
                "Citations": paper.get("citationCount", "N/A"),
                "Abstract": abstract,
                "First Author": first_author,
                "First Author Affiliation": first_author_affiliation,
                "Corresponding Author": corresponding_author,
                "Contact Info": contact_info,
                "Paper Link": paper.get("url", "N/A")
            }
    return None

def process_md_file(md_file_path):
    """
    Process a Markdown file, extract 'PaperTitle', and append related information to the file.

    Args:
        md_file_path (str): The path to the Markdown file.
    """
    print(f"Processing file: {md_file_path}")
    
    # Read the content of the MD file
    with open(md_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    updated_lines = []
    paper_title_pattern = r"PaperTitle\s*:\s*(.+)"
    failure_message = "No relevant information found"

    # Keep track of PaperTitles we've processed and the line numbers
    processed_titles = set()

    i = 0  # Iterate through each line in the file
    while i < len(lines):
        line = lines[i]
        updated_lines.append(line)

        match = re.search(paper_title_pattern, line)
        if match:
            paper_title = match.group(1).strip()
            print(f"Searching for: {paper_title}")

            # Check if this PaperTitle has been processed before
            if paper_title in processed_titles:
                i += 1
                continue  # Skip if already processed

            # Look for the table that would follow this PaperTitle (if it already exists)
            has_info = False
            info_line_index = None
            for j in range(i + 1, len(lines)):
                # Look ahead for a table-like structure that contains the paper's info
                if re.match(r"^\| Year \| Citations \| Abstract \| First Author \|", lines[j]):
                    has_info = True
                    break
                if lines[j].startswith("PaperTitle:"):
                    break  # Encountered the next PaperTitle, stop looking
                if lines[j].strip() == failure_message:
                    info_line_index = j  # Store the index where the failure message was found

            if info_line_index is not None:
                # Remove the line with "No relevant information found"
                lines.pop(info_line_index)
                print(f"Removed previous failure message for: {paper_title}")

            if not has_info:
                # Fetch paper info only if not already present
                paper_info = fetch_paper_info(paper_title)

                if paper_info:
                    # Add a blank line before the table
                    updated_lines.append("\n")

                    # Create the table with the paper information in Markdown format
                    table = (
                        f"| Year | Citations | Abstract | First Author | Affiliation | Corresponding Author | Contact Info | Paper Link |\n"
                        f"|------|-----------|----------|--------------|-------------|----------------------|--------------|------------|\n"
                        f"| {paper_info['Year']} | {paper_info['Citations']} | <details><summary>Click to expand</summary>{paper_info['Abstract']} </details> | {paper_info['First Author']} | {paper_info['First Author Affiliation']} | {paper_info['Corresponding Author']} | {paper_info['Contact Info']} | [Link]({paper_info['Paper Link']}) |\n"
                    )
                    updated_lines.append(table + "\n")
                    processed_titles.add(paper_title)  # Mark this title as processed
                else:
                    # If information is not found, add failure message below the PaperTitle
                    updated_lines.append(f"{failure_message}\n")
        i += 1

    # Write the updated content back to the file
    with open(md_file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

    print(f"File processing completed. Updates written to: {md_file_path}")

def process_all_md_files(directory):
    """
    Traverse a directory and process all Markdown (.md) files.

    Args:
        directory (str): The directory to search for Markdown files.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                process_md_file(md_file_path)

def run(lac='./'):
    print(f"Processing files in directory: {lac}")
    process_all_md_files(lac)
