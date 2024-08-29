Amazon Return Policy Bot

This project implements a Telegram bot that assists users with questions related to Amazon's return policies. The bot uses a language model to retrieve and process relevant information from an Amazon return policy document, providing concise and accurate responses to user queries.

Bot's link
https://t.me/AWS_Return_Policy_bot

Features
Natural Language Processing: The bot understands and processes user questions related to Amazon's return policy.
Document Retrieval: The bot retrieves relevant information from a pre-loaded Amazon return policy document.
Language Model Integration: The bot uses a language model (Llama2) to generate responses based on retrieved documents.
Telegram Integration: The bot interacts with users through Telegram, handling both commands and text messages.

Libs
pip install python-telegram-bot
pip install langchain
pip install langchain_community
pip install langchain_nomic
pip install langchain_core
pip install langchain_ollama
pip install langgraph

Usage
Start the Bot:

Users can start interacting with the bot by sending the /start command in Telegram. The bot will greet the user and invite them to ask questions about Amazon's return policy.

Ask Questions:

Users can type any question related to Amazon's return policy, and the bot will respond with relevant information extracted from the provided document.

Code Overview
bot.py
start Function: Handles the /start command and sends a greeting message to the user.
handle_message Function: Processes incoming text messages, retrieves relevant information from the Amazon return policy document, and generates a response using the language model.
Application Setup: Initializes the Telegram bot, sets up command and message handlers, and starts polling for messages.
model.py
Document Preparation: Loads and splits the Amazon return policy text into manageable chunks for retrieval.
Vector Store: Uses SKLearnVectorStore and NomicEmbeddings to create a searchable vector store of the document chunks.
Prompt Template: Defines a template for the language model to follow when generating responses.
Workflow Graph: Builds a state graph to manage the retrieval and response generation steps, and compiles the workflow for use in the bot.
