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
    import logging

    # Load environment variables
    load_dotenv()

    # Initialize the scraper
    scraper = LLMsWebScraper(model_type="gemini", model_name="gemini-2.0-flash-exp", api_key=os.getenv("Gemini_API_KEY"))
    # scraper = LLMsWebScraper(model_type="groq", model_name="llama3-8b-8192", api_key=os.getenv("Groq_API_KEY"))
    # scraper = LLMsWebScraper(model_type="openai", model_name="gpt-4o-mini", api_key=os.getenv("OpenAI_API_KEY"))
    # scraper = LLMsWebScraper(model_type="ollama", model_name="llama3.2", base_url="http://localhost:11434", api_key="")


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