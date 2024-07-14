import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_openai import OpenAI, OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import HumanMessage, SystemMessage, AIMessage

load_dotenv()

app = Flask(__name__, 
            template_folder='frontend/build',
            static_folder='frontend/build/static')

app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app)


llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.7)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY")




pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY")
index_name = "product-index"


pinecone_index = pc.Index(index_name)

# initialize conversation memory
conversation_memory = [{"role": "system", "content": "You are a friendly and helpful assistant for the appliance e-commerce company PartSelect. You are client-facing, so all of your responses must be professional. You will be providing product information and assisting with customer transactions. If a client's questions does not relate to specific appliance parts or general appliance queries, strictly do not answer it."}]

def get_relevant_context(query, k=1):
    """Retrieve relevant context from Pinecone based on the query."""
    query_embedding = embeddings.embed_query(query)
    context_response = pinecone_index.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True
    )
    contexts = [match['metadata']['text'] for match in context_response['matches']]
    return " ".join(contexts)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-message', methods=['POST'])
def get_message():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        global conversation_memory
        data = request.json
        user_query = data.get('query', 'No query provided')
    
        relevant_context = get_relevant_context(user_query)
    
        # prepare the messages for the language model
        messages = [
            SystemMessage(content="""You are an expert sales representative for PartSelect, specializing in dishwasher and refrigerator parts. Your role is to:

1. Provide knowledgeable, friendly assistance on products and installations.
2. Demonstrate expertise in dishwasher and refrigerator parts and their functions.
3. Offer clear, concise explanations and step-by-step installation instructions.
4. Maintain a professional tone and prioritize customer needs.

Be concise and respond in bullet points wherever possible.  If a query is unrelated to dishwashers, refrigerators, or general appliance concerns, respond:

"I specialize in dishwasher and refrigerator parts. How can I assist you with these appliances today?"

Always aim to provide excellent customer service while effectively representing PartSelect. """),
            HumanMessage(content=f"Given the following context, please provide a helpful response to the user's query. Context: {relevant_context}\n\nUser query: {user_query}")
        ]
        
        # add the last 5 messages from conversation_memory
        for msg in conversation_memory[-5:]:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
    
        # generate response based on the messages
        response = llm(messages)
    
        # append to conversation memory
        response_content = response.content
        conversation_memory.append({"role": "assistant", "content": response_content})
    
        # limit conversation memory to last 10 messages (prevent token limit issues)
        if len(conversation_memory) > 10:
            conversation_memory = conversation_memory[-10:]
    
        response = {
            "role": "assistant",
            "content": response_content
        }
        return jsonify(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/clear-memory', methods=['GET', 'POST'])
def clear_memory():
    global conversation_memory
    conversation_memory = [{"role": "system", "content": """You are an expert sales representative for PartSelect, specializing in dishwasher and refrigerator parts. Your role is to:

1. Provide knowledgeable, friendly assistance on products and installations.
2. Demonstrate expertise in dishwasher and refrigerator parts and their functions.
3. Offer clear, concise explanations and step-by-step installation instructions.
4. Maintain a professional tone and prioritize customer needs.

Remember to be concise and respond in bullet points wherever possible. If a query is unrelated to dishwashers, refrigerators, or general appliance concerns, respond:

"I specialize in dishwasher and refrigerator parts. How can I assist you with these appliances today?"

Always aim to provide excellent customer service while effectively representing PartSelect. """}]
    return jsonify({"status": "Memory cleared"})

if __name__ == '__main__':
    app.run(debug=True)