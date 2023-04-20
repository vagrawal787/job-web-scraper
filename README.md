# Indeed Job Searcher 

## an open-source recruiting project

this tool lets you type in a preferred job position and filter out roles for entry level positions on Indeed.com using Playwright, BeautifulSoup, Pandas . 

<br/>

## How to use:

1. Clone the repository and open it in your code editor. 
2. Set up a paid api account with OpenAI (https://platform.openai.com/account/org-settings)
3. Copy your API Key and paste it in the 'api_key' variable (you can also create an environment variable and use it from there)
4. In your terminal, navigate to the project directory and create a virtual environment e.g. `python3 -m venv playwrightplayround`
5. open the virtual environment using this command: `source playwrightplayground/bin/activate`
6. Install all required dependencies by running `pip install -r requirements.txt`
7. Run this command and follow the prompts: `python3 web-scraper.py`
8. To deactivate the virtual environment, run `deactivate` 

Note: If the script errors with 'Module Not Found', use `pip install ___` to install the missing packages. 

All the job results will be located in csv files in the same project directory! 




