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
Generate two sequential reports based on user input and supplementary materials. One is a *Comprehensive Research Report*, and then an *Annotated Report*.

---

# 1. Comprehensive Research Report  

A detailed, logically structured, and analytically rigorous research report based on user queries, follow-up dialogues, and supplementary materials.  

## **Input Format**  
Research scope is guided by structured dialogue inputs:  

```
[
    {"role": "assistant", "content": "What is your research question?"},
    {"role": "user", "content": "#user_initial_query"},
    {"role": "assistant", "content": "#followup_questions"},
    {"role": "user", "content": "#user_followup_answers"},
    {"role": "user", "content": "Additional context 1: #current_learnings"},
    {"role": "user", "content": "Additional context 2: #current_learnings"}
]
```
- **#user_initial_query**: The user's primary research question.  
- **#followup_questions**: Clarifying questions to refine research direction.  
- **#user_followup_answers**: Responses shaping the report’s focus.  
- **#current_learnings**: User-provided structured insights and external sources.  

## **Report Structure and Guidelines**  

### 1. Establish Clear Research Foundation  
- **Title**: Concise title reflecting combined insights from user queries and dialogue.  
- **Introduction** (~300 words): Clearly present research context, objectives, significance, and research questions or hypotheses.  

### 2. Integration of Source Materials  
- Utilize **all additional context**, incorporating **critical analysis**, key facts, and summaries.  
- Establish **cause-effect relationships** with citations for credibility.  

### 3. Logical Structure and Depth  
The research must be **structured into logical sections**, each a minimum of **2 pages**:  
- **Introduction**: Research context, significance, objectives.  
- **Literature Review**: Based on **#current_learnings**, discuss existing research, key theories, practical applications, and case studies. **Minimum of 5 pages (~3000 words).**  
- **Findings and Discussion**: Provide a detailed analysis, supported arguments, current debates and controversies, challenges and limitations, and emerging trends and future directions. **Minimum 1000 words.**  
- **Conclusion**: Summarized insights, implications, and recommendations.  
- **Learning Recommendation**: Based on conversations and literature, propose the most logical order to present this research topic to non-experts.  

### 4. Analytical Rigor and Originality  
- Prioritize **cause-effect reasoning** and **synthesis** over isolated facts.  
- Arguments must **progress logically** with explicit supporting details.  
- Ensure **original formulation**, though **direct incorporation of provided materials** in a structured manner is acceptable.  

### 5. Formatting Requirements  
- Minimum length: **5000 words**.  
- **Section headings** and **citations** required.  

---

# 2. Annotated Report  

Once the Comprehensive Research Report is finalized, generate an **Annotated Report** linking each paragraph to relevant external references.

## **Annotation Process**  
1. **Divide** the original report into paragraphs.  
2. **Identify up to 3 highly relevant references** from the structured external sources (`#current_learnings`) for each paragraph.  
   - Prioritize **high-quality and most relevant references**.  

## **Reference Extraction Format**  

Each reference annotation should be clearly structured:  

```
#####BEGINNING SEPARATOR#####
**Source URL:** "https://example.com/article1"  
"Title of Source 1"  
Extracted web summary 1  
#####ENDING SEPARATOR#####
```

Each reference must contain:  
- **Reference Title**: Extracted title from provided structured sources.  
- **Link**: Correct markdown-formatted hyperlink (e.g., [https://example.com/article1](https://example.com/article1)).  
- **Statement**: Selected key statements closely relevant to the paragraph.  

---

# **Output Format for Annotated Report**  

For each paragraph:  

### **Paragraph X from the Report**  
> *Copy the exact paragraph from the comprehensive report.*  

### **References for Paragraph X**  
- **Reference Title:** *Title from provided sources.*  
  **Link:** [URL](URL)  
  **Statement:** *Selected relevant statement(s).*  

---

# **Example Output**  

### **Paragraph 1 from the Report**  
> *In recent years, electric vehicles (EVs) have become increasingly popular as sustainable alternatives to traditional gasoline vehicles. Enhanced battery technology and favorable government policies have significantly contributed to their rapid adoption.*  

### **References for Paragraph 1**  
- **Reference Title:** *The Rise of Electric Vehicles*  
  **Link:** [https://example.com/ev-growth](https://example.com/ev-growth)  
  **Statement:** *Recent improvements in lithium-ion battery efficiency and reduced manufacturing costs have accelerated EV adoption globally.*  

- **Reference Title:** *Government Incentives and EV Adoption*  
  **Link:** [https://example.com/ev-incentives](https://example.com/ev-incentives)  
  **Statement:** *Governments worldwide offer incentives such as subsidies and tax breaks, significantly boosting consumer interest in electric vehicles.*  

---

# **Additional Notes**  
- Ensure each paragraph has a corresponding annotated version.  
- **Ensure correctly formatted, clickable URLs** in annotations.  
- All references must be formatted in **markdown for clarity**.  
- **Logical coherence and analytical depth** must be upheld throughout **both reports**.
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
   **Link**: [URL](URL) (for example, [https://example.com](https://example.com))
   ```

   Ensure that the link is fully visible and clickable.

# Example

### Input:
```
Original Statement: Climate change accelerates extreme weather events.

Supporting Evidence:
#####BEGINNING SEPARATOR#####
**Source URL:**  "https://example.com/article1"
"Rising Temperatures Increase Storm Frequency"
Recent studies indicate that climate change is causing more frequent and intense hurricanes.
#####ENDING SEPARATOR#####

#####BEGINNING SEPARATOR#####
**Source URL:**  "https://example.com/article2"
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