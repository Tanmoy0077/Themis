from typing import List
from util.schemas import ClauseDetail


def format_clauses_to_markdown(clauses: List[ClauseDetail]) -> str:
    markdown_parts = []

    if not clauses:
        return "No clauses were extracted or provided."

    for i, clause in enumerate(clauses):
        # Add Clause Title as Heading
        markdown_parts.append(f"### {i + 1}. {clause.title.strip()}")
        markdown_parts.append("\n")  # Add a newline for spacing

        # Add Clause Text
        # Using blockquote for the text might improve readability
        text_lines = clause.text.strip().split("\n")
        blockquote_text = "\n".join([f"> {line}" for line in text_lines])
        markdown_parts.append(blockquote_text)
        markdown_parts.append("\n")

        # Add annotations based on flags
        annotations = []
        if clause.is_termination_clause:
            annotations.append("**Note:** This appears to be a termination clause.")

        if clause.is_ambiguous:
            reason = (
                f" Reason: {clause.ambiguity_reason}" if clause.ambiguity_reason else ""
            )
            annotations.append(f"**Warning:** This clause may be ambiguous.{reason}")

        if annotations:
            markdown_parts.append("\n".join(annotations))
            markdown_parts.append("\n")

        # Add a separator between clauses, except for the last one
        if i < len(clauses) - 1:
            markdown_parts.append("---")
            markdown_parts.append("\n")  # Add spacing after separator

    return "\n".join(markdown_parts)
