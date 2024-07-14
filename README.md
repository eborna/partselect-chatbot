# PartSelect E-commerce Chat Agent
implemented by Eugenia Bornacini

This project implements a specialized chat agent for the PartSelect e-commerce website, focusing on Refrigerator and Dishwasher parts. The agent provides product information and assists with customer transactions.

## Features

- React-based frontend for a seamless chat interface
- Flask backend for handling requests and integrating with AI services
- Integration with OpenAI's language models for natural language processing
- Pinecone vector database for efficient storage and retrieval of product information
- Web scraping functionality to keep product data up-to-date

## Setup

1. Clone the repository:
     git clone https://github.com/your-username/partselect-chat-agent.git
     cd partselect-chat-agent
2. Install backend dependencies:
     pip install -r requirements.txt
3. Set up environment variables:
     Get an OpenAI API Key (https://platform.openai.com/account/api-keys)
     Get a Pinecone API Key (https://docs.pinecone.io/guides/get-started/quickstart)
     Create a `.env` file in the root directory and add the following:
       OPENAI_API_KEY=your_openai_api_key
       PINECONE_API_KEY=your_pinecone_api_key
       FLASK_SECRET_KEY=your_flask_secret_key
5. Install frontend dependencies:
    cd frontend
    npm install
6. In a new terminal, folow the instructions in the /frontend ReadMe to build the React frontend:
    cd frontend
    npm install
    npm run build
    load the "build" directory as a [chrome extension](https://bashvlas.com/blog/install-chrome-extension-in-developer-mode) to view the chat interface from your Chrome browser's side panel.

## Building a Vector Database

1. In `scraper_db_populator.py`, set the `category_base_url` variables. Acceptable URLs include any of the links found on the Products page from PartSelect, such as (for dishwasher and fridge parts, respectively):
- https://www.partselect.com/Dishwasher-Parts.htm
- https://www.partselect.com/Refrigerator-Parts.htm

2. Run the script:
   python scraper_db_populator.py
   
3. Wait for confirmation that the Pinecone database has been successfully populated.

**Note on database size:** The default web scraping depth is 0, retrieving the first set of products listed (38 for each kind of product). This allows for quick setup and testing. Increasing the depth will retrieve more products (by a factor of the depth) but will subsequently take longer.

**Note on runtime:** The process relies on the OpenAI API for converting raw text data into natural language, which is time-consuming but enhances query accuracy.

## Testing Scope

Due to the limited scrape depth, the bot's knowledge is based on the first set of products from the chosen category URLs. For testing, visit these URLs, click on any "Featured Products", and quiz the bot. Increasing scrape depth will expand the knowledge base but will increase build time.

## Running the App

1. Start the Flask backend:
   Certainly! I'll incorporate these concepts into the README, adjusting them to fit your specific project. Here's an updated version of the README:
markdownCopy# PartSelect E-commerce Chat Agent

This project implements a specialized chat agent for the PartSelect e-commerce website, focusing on Refrigerator and Dishwasher parts. The agent provides product information and assists with customer transactions.

## Features

- Chrome extension frontend for a seamless chat interface in the browser's side panel
- Flask backend for handling requests and integrating with AI services
- Integration with OpenAI's language models for natural language processing
- Pinecone vector database for efficient storage and retrieval of product information
- Web scraping functionality to keep product data up-to-date

## Frontend Setup

1. Load the "build" directory as a [chrome extension](https://bashvlas.com/blog/install-chrome-extension-in-developer-mode) to view the chat interface right from your Chrome browser's side panel.

## Backend Setup

1. Clone the repository:
git clone https://github.com/your-username/partselect-chat-agent.git
cd partselect-chat-agent
Copy
2. Get an OpenAI [API Key](https://platform.openai.com/account/api-keys)

3. Copy `.env.template` to `.env`, then set `OPENAI_API_KEY` and `FLASK_SECRET_KEY`

4. Install backend dependencies:
pip install -r requirements.txt
Copy
## Building a Vector Database

1. In `scraper_db_populator.py`, set the `category_base_url` variables. Acceptable URLs include any of the links found on the Products page from PartSelect, such as:
- https://www.partselect.com/Dishwasher-Parts.htm
- https://www.partselect.com/Refrigerator-Parts.htm

2. Run the script:
python scraper_db_populator.py
Copy
3. Wait for confirmation that the Pinecone database has been successfully populated.

**Note on database size:** The default web scraping depth is 0, retrieving the first set of products listed. This allows for quick setup and testing. Increasing the depth will retrieve more products but will take longer.

**Note on runtime:** The process relies on the OpenAI API for converting raw text data into natural language, which is time-consuming but enhances query accuracy. This solution prioritizes response quality over range.

## Testing Scope

Due to the limited scrape depth, the bot's knowledge is based on the first set of products from your chosen category URLs. For testing, visit these URLs, click on any "Featured Prodcuts", and quiz the bot. Increasing scrape depth will expand the knowledge base but may increase build time. 
In development testing, the bot did well (>90% accuracy) in responding accurately and not interacting outside of its knowledge scope.

## Running the App

1. Start the Flask backend:
   python flask_app.py

2. Launch the Chrome extension in your browser.

3. Enjoy interacting with the appliance chat agent!
   
## Project Structure

- `flask_app.py`: Main backend application
- `scraper_db_populator.py`: Web scraping and database population script
- `test.py`: Connection tester for debugging flask application
- `frontend/`: React frontend application

## Future Enhancements

- Implement routing for query classification for more precise database selection and navigation between topics
- Expand product coverage beyond refrigerators and dishwashers
- Enhance web-scraping to refresh for an up-to-date product catalog 




