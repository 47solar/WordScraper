# WordScraper

<b>The idea is taken from Hack The Box Academy, an "Introduction to Python 3" module for learning</b>

This script is designed to scrape words from a given webpage and its internal links, analyze them, and generate potential password mutations based on configurable options. The user can customize the depth of the crawl, the types of mutations to apply to words, and filter words based on their length. The script outputs the results in a convenient format, with options to save the output to a file. Additionally, it includes a progress bar for a better user experience, especially when processing large numbers of words or pages.
User-Accessible Functionality:

The script provides the following features, which can be controlled through command-line options:

    URL Input (--url / -u):
        Purpose: The user provides the URL of a webpage to scrape words from.
        Usage: --url https://example.com

    Crawl Depth (--depth / -d):
        Purpose: This option controls how deep the script will crawl through internal links of the provided URL. Higher depth values allow for a more extensive crawl, exploring more pages.
        Usage: --depth 2 (crawls the provided URL and links on pages within two levels of depth)

    Minimum Word Length (--length / -l):
        Purpose: The user can specify a minimum word length. Only words with lengths greater than or equal to this threshold will be considered in the output.
        Usage: --length 5 (only words with 5 or more characters will be counted)

    Fixed Word Length (--fixed-length / -f):
        Purpose: This option allows the user to specify an exact word length. Only words with the exact length provided will be included.
        Usage: --fixed-length 6 (only words with exactly 6 characters will be included)

    Top Words Count (--count / -c):
        Purpose: The user specifies how many of the most frequent words they want to see in the output.
        Usage: --count 10 (displays the 10 most frequent words)

    Word Mutation Options:
        Purpose: Users can choose whether to apply various password mutation strategies to the words found during scraping. The following mutation types can be controlled:
            Base Mutation (--apply-mutation / -am): Applies common password transformations like capitalizing or converting the word to uppercase.
            Leetspeak Mutation (--apply-leet / -al): Applies leetspeak transformations to words (e.g., replacing 'a' with '4').
            Character-Based Mutation (--apply-chars / -ac): Appends numbers and symbols to the words (e.g., adding '1', '!', etc.).
        Usage:
            --apply-mutation (applies base transformations like capitalization).
            --apply-leet (applies leetspeak transformations).
            --apply-chars (appends characters like numbers and symbols).
    Search through the extracted words:
        Purpose: Option allows users to pass multiple words to search for.
        Usage: --search "admin" "password" (without specifying the length or quantity)
    Output File (--output / -o):
        Purpose: Allows the user to save the results of the script to a file for further use.
        Usage: --output result.txt (saves the results in a file named result.txt)

    Progress Bar:
        Purpose: To provide feedback on the script’s progress as it scrapes pages and processes words. A progress bar will be shown while crawling through internal links and processing the words for mutations.

Example Command:

    python WordScraper.py --url https://example.com --depth 2 --length 5 --count 10 --apply-mutation --apply-leet --apply-chars --output result.txt

What the Script Does:

* Scrapes words from the given URL and all internal links up to the specified crawl depth.
* Filters out words that don’t meet the length criteria (either minimum or fixed).
* Optionally applies mutations to words, such as capitalization, leetspeak, and appending numbers/symbols, based on user preferences.
* Displays the most frequent words found (up to a specified count).
* Shows the total number of unique words discovered.
* Saves the results in the specified file, if chosen.

The user can easily configure the script to customize the output to their needs, such as when searching for potential password candidates or analyzing a webpage’s text content. The progress bar improves the user experience, especially for large websites.
