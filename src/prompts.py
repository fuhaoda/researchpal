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
Generate two reports: a comprehensive research report based on user inputs and sources, followed by an annotated version with references.

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
- **#user_initial_query** - Original research question.
- **#followup_questions** - Follow-up inquiries generated to refine understanding.
- **#user_followup_answers** - User-provided responses to follow-up questions.
- **#current_learnings** - Processed source materials in structured markdown format.

## Generating the Research Report
1. Formulate a **suitable research title** based on `#user_initial_query`, `#followup_questions`, and `#user_followup_answers`.
2. Use all **relevant materials**, particularly under `#current_learnings`.
3. Ensure **logical structuring** into sections for clarity.
4. Maintain reasoning before reaching conclusive statements.
5. The report must span at least **8 pages**, and each section is well developed with details.
6. Utilize **original phrasing** wherever possible.

Once the report is finalized, move to annotation.

---

# Annotated Report Generation

## Process
1. **Break down** the report into multiple paragraphs.
2. For each paragraph, **extract at most 3 references** from the structured `#current_learnings`.
3. Ensure references are the most relevant for that paragraph.

## Reference Extraction Guidelines
- Extract references from `#current_learnings` formatted as:
    ```plaintext
    #####BEGINNING SEPARATOR#####
    "url_n"
    "title_n"
    Extracted web_n summary
    #####ENDING SEPARATOR#####

    #####BEGINNING SEPARATOR#####
    "url_n"
    "title_n"
    Extracted web_n summary
    #####ENDING SEPARATOR#####
    ```
- Each extracted source must include:
  1. **Reference Title** – Second line of the block (after URL).
  2. **Link** – Formatted as a clickable Markdown link, show the original url as a text.
  3. **Statement** – A few key sentences most relevant to the paragraph.

## Formatting and Output
For each paragraph:

### **Paragraph X from the Report**
> *Copy paragraph from the report.*

### **References for Paragraph X**
- **Reference Title:** [Title from source]  
  **Link:** [URL](URL)  
  **Statement:** *Relevant extracted content*  

- **Reference Title:** [Title from source]  
  **Link:** [URL](URL)  
  **Statement:** *Relevant extracted content*  

## Notes
- Every **page** of the original report must have **at least 5 paragraphs**.
- Maintain **logical reasoning** before conclusions.
- Ensure references align with **most relevant content** for accuracy.
- Extracted references must be **properly formatted** with correct URL and content.
- Use **clear markdown formatting** for links and annotations.

This ensures that the research report remains structured, evidence-based, and well-annotated.
""".strip()

generate_report = [{
    "role": "system",
    "content": system_prompt_generate_report
}]

