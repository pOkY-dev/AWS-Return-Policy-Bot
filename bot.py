from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from model import custom_graph, rag_chain  

# Dictionary to store default responses
default_responses = {
    "hello":"Hello! I am the Amazon Return Policy Bot. Ask me anything about returns!",
    "how do you work?": "I use advanced language models and Amazon's return policy to answer your questions about returns.",
    "what can you do?": "I can provide information about Amazon's return policy, including timelines, eligible items, and the return process.",
    "can you help me with a return?": "Yes, I can guide you through the return process. Just tell me what you want to return and I'll help you find the relevant information.",
    "what is Amazon's return policy?": "Amazon's return policy allows you to return most new, unopened items within 30 days of delivery for a full refund. However, some items may have different return windows or conditions. You can ask me for specifics about a particular product.",
    "how do I initiate a return?": "You can initiate a return by going to 'Your Orders' on Amazon.com, selecting the order containing the item you wish to return, and then clicking on the 'Return or Replace Items' button. Follow the on-screen instructions to complete the return process.",
}

async def start(update: Update, context):
    await update.message.reply_text('Hi! I am the Amazon Return Policy Bot. Ask me anything about returns!')



async def handle_message(update: Update, context):
    user_question = update.message.text

    # Check for default questions first
    if user_question.lower() in default_responses:
        response = default_responses[user_question.lower()]
    else:
        # If not a default question, use the RAG chain
        response = custom_graph.invoke({"question": user_question, "steps": []})

        # Check and log the relevant parts of the response
        retrieved_docs = response["documents"]
        for doc in retrieved_docs:
            print("Doc content:", doc.page_content)

        formatted_prompt = rag_chain.steps[0].format(question=user_question, documents=retrieved_docs)
        print("Full Prompt:", formatted_prompt)
        print("Generated Response:", response["generation"])

        # Extract text from the Document objects
        extracted_text = [doc.page_content for doc in retrieved_docs]

        # Use the adjusted prompt template with extracted text
        formatted_prompt = rag_chain.steps[0].format(question=user_question, documents=extracted_text)

        # Get the generated response (which is a string)
        response = response["generation"]

    # Now send only the generated response
    await update.message.reply_text(response) 
# Initialize the Telegram bot 
application = ApplicationBuilder().token("7490941592:AAG2YWJeJbblZPBv3-M6zuOYPHLVWF0R2ZY").build()

# Add the command and message handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start polling for messages
application.run_polling()



