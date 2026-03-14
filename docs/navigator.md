# Navigator

Open Google Chrome or Firefox, search Google, and extract all web pages from the search results.

**Core functionality:** Opens the specified browser on the host machine, performs a search for the query, prints the extracted web links from the first page of Google, and saves the links to a local JSON file (`google_search_results.json`).

## Usage
```bash
python skills/navigator/scripts/navigate.py [--browser chrome|firefox] <QUERY>
```

## Example
```bash
python skills/navigator/scripts/navigate.py --browser firefox highest mountain in the world
```
