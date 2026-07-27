# from tools.content_scraper_tool import search_urls
import json

from agents.content_scraper_agent import get_content_scraper_agent
from graph.event_bus import Event, event_bus
from graph.events.ingestion_events import IngestionEventType
from graph.ingestion_graph.state import GraphState
from helper.json_parser import parse_agent_json
from helper.retry import retry_async
from telemetry.instrumentation import tracer


async def search_node(state: GraphState):
    with tracer.start_as_current_span("Scraping URLs"):

        with tracer.start_as_current_span("Scraping"):
            # scraped_urls = await retry_async(
            #     lambda: search_urls(state["rewritten_query"])
            # )

            content_scraper_agent = await get_content_scraper_agent()

            result = await retry_async(
                lambda: content_scraper_agent.ainvoke({"messages": [{"role": "user", "content": json.dumps({"query": state["rewritten_query"]})}]})
            )

            print(result)

            data = parse_agent_json(result["messages"][-1].content)

        print(data["pages"])

        await event_bus.publish(
            Event(
                conversation_id=state["conversation_id"],
                type=IngestionEventType.SEARCH_COMPLETED,
                data={
                    "urls_found": len(data["pages"]),
                },
            )
        )

        return {
            "url_list": data["pages"],
        }