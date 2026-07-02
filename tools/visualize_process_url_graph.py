from dotenv import load_dotenv

load_dotenv()

from graph.ingestion_graph.process_url_graph import process_url_graph

png = process_url_graph.get_graph().draw_mermaid_png()

with open("process_url_graph.png", "wb") as f:
    f.write(png)

print("Graph generated!")