from langgraph.graph import StateGraph, START, END

from agent.head_agent.state.head_state import HeadState
from agent.head_agent.state.graph_input import GraphInput

from agent.head_agent.nodes.head_node import head_node
from agent.head_agent.nodes.file_node import file_node
from agent.head_agent.nodes.verification_node import verification_node
from agent.head_agent.nodes.cost_estimation_node import cost_estimation_node
from agent.head_agent.nodes.organization_node import organization_node

from agent.head_agent.router.router import route_after_head


builder = StateGraph(
    HeadState,
    input_schema=GraphInput,
)


builder.add_node(
    "head",
    head_node,
)

builder.add_node(
    "file",
    file_node,
)

builder.add_node(
    "verification",
    verification_node,
)

builder.add_node(
    "cost",
    cost_estimation_node,
)

builder.add_node(
    "organization",
    organization_node,
)


builder.add_edge(
    START,
    "head",
)


builder.add_conditional_edges(
    "head",
    route_after_head,
    {
        "file": "file",
        "verification": "verification",
        "cost": "cost",
        "organization": "organization",
        "end": END,
    },
)


builder.add_edge(
    "file",
    "head",
)

builder.add_edge(
    "verification",
    "head",
)

builder.add_edge(
    "cost",
    "head",
)

builder.add_edge(
    "organization",
    "head",
)


claim_graph = builder.compile()


# The PNG export only runs when this file is executed directly
# (python claim_graph.py). It must NOT run on import, because writing
# a file inside the project triggers the dev server's auto-reload.
if __name__ == "__main__":
    from pathlib import Path

    out = Path(__file__).resolve().parent / "claim_graph.png"

    try:
        claim_graph.get_graph().draw_mermaid_png(
            output_file_path=str(out)
        )
        print(f"Graph image saved to: {out}")

    except Exception as e:
        print(f"Could not generate PNG: {e}")