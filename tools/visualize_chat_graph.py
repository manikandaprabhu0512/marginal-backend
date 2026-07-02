from dotenv import load_dotenv

load_dotenv()

from graph.chat_graph.chat_graph import chat_graph

png = chat_graph.get_graph().draw_mermaid_png()

with open("chat_graph.png", "wb") as f:
    f.write(png)

print("Graph generated!")