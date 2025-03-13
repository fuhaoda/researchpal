from src.config import MAX_FOLLOWUP_QUESTION, MAX_SERP_RESEARCH, MAX_SERP_EVIDENCE

generate_followup = [{
    "role": "system",
    "content": f"Given the following query from the user, ask some follow up questions to clarify the research direction. Return a maximum of {MAX_FOLLOWUP_QUESTION} questions with a purpose to generate a research report for the topic, but feel free to return less if the original query is clear"
}]


generate_serp_research = [{
    "role": "system",
    "content": (
        f"Given the following conversation between assistant and user, generate a list of high quality SERP queries. These queries should be designed for effective research using a search engine like Google."
        f"Return a maximum of {MAX_SERP_RESEARCH} queries, but feel free to return fewer if the original prompt is clear. "
        "Prioritize sources of high-quality information, such as Published papers in top academic journals.\n"
        "Make sure each query is unique and not similar to the others.\n"
        "Each query should exist on its own line to ensure easy parsing.\n"
        "Output only the SERP queries, without any additional text."
    )
}]

generate_serp_evidence = [{
    "role": "system",
    "content": (
        f"Generate a list of high-quality SERP (Search Engine Results Page) queries based on the text provided by the user."
        "These queries should be optimized for effective research using search engines like Google."
        "The queries should specifically aim to find supporting evidence for the user's provided material."
        f"Return a maximum of {MAX_SERP_EVIDENCE} queries, ensuring at least one query is always provided. If the provided text is clear and does not require many queries, returning fewer is acceptable."
        "Prioritize sources of high-quality information, such as Published papers in top academic journals.\n"
        "Make sure each query is unique and not similar to the others.\n"
        "Each query should exist on its own line to ensure easy parsing.\n"
        "Output only the SERP queries, without any additional text."
    )
}]


### Summarize Crawl ###
system_prompt_summarize_crawl = """
Given the following input scraped results from the web, summarize the content in no more than one page using Markdown format. Use the original sentences as much as possible.

The summary should follow this structure:

1. Start with the title of the page as the first line.
2. Provide an executive summary in no more than 3 sentences.
3. Follow with a detailed summary with the length about one page.

# Output Format

The output should be formatted as follows:

# [Title]
**Executive Summary**  
[No more than 3 sentences summarizing the key points. Use simple language, avoiding jargon.]

**Detailed Summary**  
[More in-depth summary of the content with the length less or equal to one page.]

Ensure the summary remains concise while preserving the original meaning.
""".strip()

summarize_crawl =[
    {
        "role": "system",
        "content": system_prompt_summarize_crawl
    }
]


### Generate Report ###
system_prompt_generate_report_research = """
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

generate_report_research = [{
    "role": "system",
    "content": system_prompt_generate_report_research
}]


system_prompt_find_supporting_evidence = """
Extract the most related supporting evidence from multiple summaries to match the given **Original Statement** and generate a report.

# Instructions

1. **Input Format**  
   The user input includes:
   - **Original Statement**: Specified as `"Original Statement:" + block`
   - **Supporting Evidence**: Multiple summary entries formatted as:

     ```
     #####BEGINNING SEPARATOR#####
     "url_n"
     "title_n"
     Extracted web_n summary
     #####ENDING SEPARATOR#####
     ```

   - Each learning instance consists of multiple summaries, enclosed within separators.

2. **Processing Steps**  
   - Identify the most relevant summaries that directly support the **Original Statement**.
   - Select **at most 5** supporting summaries that best reinforce the claim.
   - Extract the **most related sentence** (or brief two-sentence summary) from each selected supporting summary.
   - Collect the corresponding **Title** and **URL** from the same summary.

3. **Output Format**  
   Generate a structured markdown report in the format:

   ```
   **Statement**: [Most related extracted sentence or brief two-sentence summary]  
   **Reference Title**: [Title extracted from the corresponding summary]  
   **Link**: [URL](URL)
   ```

   Ensure that the link is fully visible and clickable.

# Example

### Input:
```
Original Statement: Climate change accelerates extreme weather events.

Supporting Evidence:
#####BEGINNING SEPARATOR#####
"https://example.com/article1"
"Rising Temperatures Increase Storm Frequency"
Recent studies indicate that climate change is causing more frequent and intense hurricanes.
#####ENDING SEPARATOR#####

#####BEGINNING SEPARATOR#####
"https://example.com/article2"
"Record Heat Waves Globally"
Data from NOAA shows that global temperatures have reached unprecedented highs in the last decade.
#####ENDING SEPARATOR#####
```

### Output:
**Statement**: Recent studies indicate that climate change is causing more frequent and intense hurricanes.  
**Reference Title**: Rising Temperatures Increase Storm Frequency  
**Link**: [https://example.com/article1](https://example.com/article1)


# Notes
- Output should **not exceed 5 entries**.
- If multiple summaries strongly support the statement, **prioritize the most specific and directly relevant** ones.
- Ensure text is clean and formatted correctly in Markdown.
- Avoid redundancy in selected supporting evidence.
"""
### Find Supporting Evidence ###
find_evidence = [{
    "role": "system",
    "content": system_prompt_find_supporting_evidence
}]