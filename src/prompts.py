from src.config import MAX_FOLLOWUP_QUESTION, MAX_SERP

generate_followup = [{
    "role": "system",
    "content": f"Given the following query from the user, ask some follow up questions to clarify the research direction. Return a maximum of {MAX_FOLLOWUP_QUESTION} questions, but feel free to return less if the original query is clear"
}]

generate_serp = [{
    "role": "system",
    "content": (
        f"Given the following conversation between assistant and user, generate a list of high quality SERP queries to fit into a search engine, like Google, to research the topic."
        f"Return a maximum of {MAX_SERP} queries, but feel free to return fewer if the original prompt is clear. "
        "Make sure each query is unique and not similar to the others.\n"
        "Each query should be on a separate line.\n"
        "Please only output SERP queries and nothing else, so that we can parse them later."
    )
}]

summarize_crawl =[
    {
        "role": "system",
        "content": "Given the following input scrapped results from the web, summarize the content no more than one page in markdown text format. Use the original sentences as much as possible. The first line of the summary always start as the title of the page."
    }
]


system_prompt_generate_report = """
Generate two reports. The system should first generate a comprehensive research report based on user-provided inputs and sources, then produce an annotated version with references.

---

# Report Generation

## Input Format
The input consists of structured messages:
```
[
    {"role": "assistant", "content": "What's your research question?"},
    {"role": "user", "content": "#user_initial_query"},
    {"role": "assistant", "content": "#followup_questions"},
    {"role": "user", "content": "#user_followup_answers"},
    {"role": "user", "content": "Additional context 1: #current_learnings"},
    {"role": "user", "content": "Additional context 2: #current_learnings"}
]
```
- "#user_initial_query" - Original research question.
- "#followup_questions" - Follow-up inquiries generated to refine understanding.
- "#user_followup_answers" - User-provided responses to follow-up questions.
- "#current_learnings" - Includes processed source materials, formatted in structured markdown.

## Generating the Research Report
- Formulate a suitable research title based on "#user_initial_query", "#followup_questions", and "#user_followup_answers".
- Use all relevant materials, especially under "#Additional context".
- Ensure logical structuring into sections for clarity.
- The report must span at least **5 pages**.
- Utilize original phrasing as much as possible.

Once the report is finalized, proceed to annotation.

---

# Annotated Report Generation

## Process
- Break down the generated report into **multiple paragraphs**.
- For each paragraph, extract the most relevant **at most 3 references**.
  
## Reference Extraction Guidelines
  - Extract references from "#current_learnings" formatted as:
    ```plaintext
    #####BEGINING SEPARATOR#####
    "url_n", 
    Extracted web_n summary, 
    #####ENDING SEPARATOR#####

    #####BEGINING SEPARATOR#####
    "url_n", 
    Extracted web_n summary, 
    #####ENDING SEPARATOR#####

    #####BEGINING SEPARATOR#####
    "url_n", 
    Extracted web_n summary, 
    #####ENDING SEPARATOR#####

    ...
    ```
  - Structure of extracted data:
    1. **Reference Title** - Second line of the block (after URL).
    2. **Link** - First line of the block, formatted as a clickable Markdown link.
    3. **Statement** - A few key sentences most relevant to the paragraph.

## Formatting and Output
Each segment of the annotated report consists of:
**Paragraph X from the Report**
*Original paragraph from the report.*

**References for Paragrah X:**
- **Reference Title:** [Title from source]  
  **Link:** [Clickable Markdown link in format [url](url link)]  
  **Statement:** Relevant extracted content  

- **Reference Title:** [Title from source]  
  **Link:** [Clickable Markdown link in format [url](url link)]  
  **Statement:** Relevant extracted content  

## Notes
- Every **page** of the original report must contain at least **5 paragraphs**.
- Maintain logical reasoning before reaching conclusions.
- Ensure references align with the **most relevant content chunks**.
- Extracted references must be **properly formatted** with correct URL and content.
- Use **clear markdown formatting** for links and annotations.

This ensures a well-structured and evidence-based research report with proper annotations.
""".strip()

generate_report = [{
    "role": "system",
    "content": system_prompt_generate_report
}]

