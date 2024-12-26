# LLMs Web Scraper

LLM Web Scraper is a Python library that uses a generative AI model to extract structured data from web pages.

## Features
- Fetch HTML content from web pages.
- Extract structured data using instructions and an LLM.
- Save extracted data to a JSON file.

## How to Use

1. **Install the pip Library**: Use the `pip install` command.

    ```cmd
    pip install LLMsWebScraper
    ```

2. **Test the Installed Library**
    After the library is installed, you can import and use it in your Python projects just like any other library.

    Create a Python File to Test It: Create a new Python file or open a Python REPL to use your library.

    For example:

    ```python
    from LLMsWebScraper import LLMsWebScraper  
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Initialize the scraper
    scraper = LLMsWebScraper(api_key=os.getenv("Gemini_API_KEY"))

    # Define instructions
    instructions = """
    Extract the following information:
    1. Titles of all blog posts on the page.
    2. Author names for each blog post.
    3. Publication dates of each blog post.

    Please provide the extracted information in a structured JSON format.
    Expecting property name enclosed in double quotes and values in string format.
    Example:
    {
    "blog_posts": [
            {
                "title": "Blog Post 1",
                "author": "Author 1",
                "publication_date": "2022-01-01"
            },
            {
                "title": "Blog Post 2",
                "author": "Author 2",
                "publication_date": "2022-01-02"
            }
        ]
    }
    """

    # URL of the webpage to scrape
    url = "https://chirpy.cotes.page/"

    # Extract data
    blog_data = scraper.toJSON(url, instructions)

    # Print the data
    print(blog_data)

    # If need to save like as json file
    if blog_data:
        scraper.toFile(blog_data, "output/data.json")
    else:
        logging.warning("No blog data to save.")
    ```