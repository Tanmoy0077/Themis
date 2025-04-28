
from langgraph.graph import StateGraph, START, END
from states import CourtCaseState
from nodes import (
    document_loader,
    summarize_case,
    case_facts
)

graph_builder = StateGraph(CourtCaseState)

graph_builder.add_node("load_document", document_loader)
graph_builder.add_node("case_summary", summarize_case)
graph_builder.add_node("case_facts", case_facts)


graph_builder.add_edge(START, "load_document")
graph_builder.add_edge("load_document", "case_summary")
graph_builder.add_edge("load_document", "case_facts")

graph_builder.add_edge("case_summary", END)
graph_builder.add_edge("case_facts", END)


court_case_graph = graph_builder.compile()


try:
    court_case_graph.get_graph().draw_mermaid_png(output_file_path="court_case_graph.png")
except Exception as e:
    print("Could not draw contract graph: ", e)
    
