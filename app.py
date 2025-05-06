import os
from typing import Optional, TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import START, END, StateGraph
from tools.search_paddy_info import paddy_info_tool, search_rice_varieties
from tools.get_detection_info import disease_detection_tool
from tools.search_disease_treatment import disease_treatment_tool
from core.prompt import SYSTEM
from langchain_core.runnables import RunnableLambda
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid
import base64
# from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Setup LLM and history
# Get API key from environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

llm = ChatOpenAI(
    temperature=0,
    max_tokens=2000,
    model="gpt-4-turbo",
    api_key=openai_api_key)

HISTORY_FILE = "history.txt"
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as file:
        file.write("")

# History management functions


def read_previous_history():
    """Read the previous_response_id from the history file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return file.read().strip()
    return None


def write_previous_history(messages):
    """Append the messages to the history file."""
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        # Handle both string and list content
        if isinstance(messages, list):
            # If it's a list of content items, convert to a string representation
            message_str = str(messages)
        else:
            # If it's already a string, use it directly
            message_str = str(messages)

        file.write(message_str + "\n")


# Define the prompt template for the main agent interaction
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM.format(context="")),
        ("placeholder", "{messages}"),
    ]
)

# Document chain setup
document_chain_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM),
        ("human", "{input}"),
    ]
)
question_answering_chain = create_stuff_documents_chain(
    llm, document_chain_prompt)

# Tools - now including image classification
tools = [paddy_info_tool, disease_detection_tool, disease_treatment_tool]

# Bind tools to the LLM
llm_with_tools = llm.bind_tools(tools)
agent_chain = agent_prompt | llm_with_tools

# Define the agent state


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    # You can add more state fields here if needed


def assistant(state: AgentState):
    response = agent_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}


# Build the graph
builder = StateGraph(AgentState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)
builder.add_edge("tools", "assistant")
alfred = builder.compile()


def get_final_response(messages):
    """Extract the final response from the list of messages."""
    previous_messages = read_previous_history()
    if previous_messages:
        messages = [HumanMessage(content=previous_messages)] + messages
    write_previous_history(messages[-1].content)
    response = alfred.invoke({"messages": messages})
    final_response = next(m for m in reversed(
        response['messages']) if isinstance(m, AIMessage) and not m.tool_calls)
    print("🎩 Alfred's Response:", final_response)
    return final_response.content


@app.route("/", methods=["POST"])
def handle_request():
    # Check if a message is provided
    message = request.form.get("message", None)

    # Check if a file is provided
    file = request.files.get("file", None)

    if not message and not file:
        return jsonify({"error": "No message or file provided"}), 400

    response_data = {}

    # Process the file if provided
    image_path = None
    if file:
        # Save the image with a unique filename
        filename = f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)
        print(f"File saved at: {image_path}")

    # Construct the appropriate message
    if message and image_path:
        # Both text and image
        human_message = HumanMessage(
            content=[
                {"type": "text", "text": message},
                {
                    "type": "text",
                    "text": f"I've uploaded an image. Please analyze it using the disease_detection_tool. The image path is: {image_path}"
                }
            ]
        )
    elif image_path:
        # Image only
        human_message = HumanMessage(
            content=f"I've uploaded an image. Please analyze it using the disease_detection_tool. The image path is: {image_path}"
        )
    else:
        # Text only
        human_message = HumanMessage(content=message)

    # Get the response from the agent
    response_data["message"] = get_final_response([human_message])

    write_previous_history(response_data["message"])

    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True)
