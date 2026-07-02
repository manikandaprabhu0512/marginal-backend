from dotenv import load_dotenv

load_dotenv()

from graph.ingestion_graph.ingestion_graph import graph

png = graph.get_graph().draw_mermaid_png()

with open("ingestion_graph.png", "wb") as f:
    f.write(png)

print("Graph generated!")