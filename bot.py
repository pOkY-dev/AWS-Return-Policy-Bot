from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from model import custom_graph, rag_chain  

async def start(update: Update, context):
    await update.message.reply_text('Hi! I am the Amazon Return Policy Bot. Ask me anything about returns!')

async def handle_message(update: Update, context):
    user_question = update.message.text
    response = custom_graph.invoke({"question": user_question, "steps": []})

    # Check and log the relevant parts of the response
    retrieved_docs = response["documents"]
    for doc in retrieved_docs:
        print("Doc content:", doc.page_content)

    # Use the adjusted prompt template
    formatted_prompt = rag_chain.steps[0].format(question=user_question, documents=retrieved_docs)
    print("Full Prompt:", formatted_prompt)

    print("Generated Response:", response["generation"])

    await update.message.reply_text(response["generation"])

# Initialize the Telegram bot 
application = ApplicationBuilder().token("7490941592:AAG2YWJeJbblZPBv3-M6zuOYPHLVWF0R2ZY").build()

# Add the command and message handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Start polling for messages
application.run_polling()



