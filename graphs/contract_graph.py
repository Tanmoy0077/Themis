from langgraph.graph import StateGraph, START, END
from states import ContractState
from nodes import (
    document_loader,
    classify_contract,
    extract_clauses,
    create_review_plan,
    summarize_contract,
    review_contract,
)

graph_builder = StateGraph(ContractState)

graph_builder.add_node("load_document", document_loader)
graph_builder.add_node("classify_contract", classify_contract)
graph_builder.add_node("extract_clauses", extract_clauses)
graph_builder.add_node("create_review_plan", create_review_plan)
graph_builder.add_node("review_contract", review_contract)
graph_builder.add_node("summarize_contract", summarize_contract)

graph_builder.add_edge(START, "load_document")
graph_builder.add_edge("load_document", "classify_contract")
graph_builder.add_edge("load_document", "extract_clauses")
graph_builder.add_edge("load_document", "summarize_contract")
graph_builder.add_edge("classify_contract", "create_review_plan")
graph_builder.add_edge("create_review_plan", "review_contract")

graph_builder.add_edge("extract_clauses", END)
graph_builder.add_edge("summarize_contract", END)
graph_builder.add_edge("review_contract", END)

contract_graph = graph_builder.compile()


# Uncomment the following lines to draw the contract graph
# try:
#     contract_graph.get_graph().draw_mermaid_png(output_file_path="contract_graph.png")
# except Exception as e:
#     print("Could not draw contract graph: ", e)
    
