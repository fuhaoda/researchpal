from src.config import MAX_FOLLOWUP_QUESTION, MAX_SERP_RESEARCH, MAX_SERP_EVIDENCE
from src.utils import section_separator_begin, section_separator_end

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


# ### Generate Report ###
# system_prompt_generate_report_research = """
# # **Comprehensive Research Report Generation**

# This task requires generating a **detailed, well-structured, and analytically rigorous** research report based on user queries, follow-up dialogues, and supplementary materials. The content must integrate user-provided context and external references while maintaining logical coherence and depth.

# ## **Input Format and Research Scope**

# The report is guided by structured dialogue inputs, typically formatted in a Python list as follows:

# ```python
# [
#     {"role": "assistant", "content": "What is your research question?"},
#     {"role": "user", "content": "#user_initial_query"},
#     {"role": "assistant", "content": "#followup_questions"},
#     {"role": "user", "content": "#user_followup_answers"},
#     {"role": "user", "content": "Additional context 1: #current_learnings"},
#     {"role": "user", "content": "Additional context 2: #current_learnings"}
# ]
# ```

# ### **Key Input Components:**  
# - **#user_initial_query**: The primary research question or problem statement provided by the user.  
# - **#followup_questions**: Clarifying and refining questions to better define the research scope.  
# - **#user_followup_answers**: User responses that help shape the focus of the report.  
# - **#current_learnings**: User-supplied insights from external materials, structured data, research sources, or expert opinions.  

# The final report must consolidate these components into a **cohesive and in-depth analysis** that adheres to research standards.

# ---

# ## **Report Structure and Guidelines**

# The comprehensive research report should follow a **logical, well-organized structure** that facilitates readability and academic rigor.

# ### **1. Establish a Strong Research Foundation**  
# - **Title**: A concise and precise title that captures the essence of the research question and objectives.  
# - **Table of Contents**: List section titles only (no subsections).  
# - **Introduction** (~1000 words):  
#   - Clearly define the research context, objectives, and significance.  
#   - Align the research problem with relevant theoretical or practical implications.  
#   - Articulate specific research questions or hypotheses that guide the study.  

# ---

# ### **2. Integration and Synthesis of Source Materials**  
# All analysis must be built upon a solid foundation of reasoning before reaching conclusions:  
# - Incorporate all **additional context (#current_learnings) and user-generated insights** into the analysis.  
# - Establish **cause-effect relationships** with proper theoretical grounding before making claims.  
# - Perform **critical evaluations** of cited materials rather than merely summarizing facts.  
# - Analyze alternative viewpoints to enhance depth and rigor—arguments should be developed fully before presenting conclusions.  
# - Ensure that reasoning flows **logically** from evidence to findings in a progressive, structured manner.  

# ---

# ### **3. Logical Organization and Depth**  
# Each section should be **comprehensive and detailed**, ensuring analytical depth by maintaining a **minimum of two pages** per core section:  

# #### **Main Sections and Minimum Length Requirements**  
# - **Introduction**: Defines purpose, research significance, and key objectives (~1000 words).  
# - **Literature Review**:  
#   - Summarizes relevant existing research findings.  
#   - Reviews key theories and conceptual models.  
#   - Discusses practical applications and case studies.  
#   - Presents gaps in the current research landscape with alternative perspectives.  
#   - **Minimum of 5000 words.**  
# - **Findings and Discussion**:  
#   - Develops insights through logical reasoning and analytical rigor **before stating conclusions**.  
#   - Presents supported arguments, competing perspectives, and critical debates.  
#   - Evaluates challenges, limitations, biases, and possible counterarguments.  
#   - Explores emerging trends and future research directions.  
#   - **Minimum 1000 words.**  
# - **Conclusion**:  
#   - Summarizes findings concisely **while strictly deriving conclusions from previous reasoning**.  
#   - Provides key takeaways, implications, and recommendations.  
# - **Learning Recommendation**:  
#   - Structures the most logical order of presentation for a non-expert audience.  
#   - Connects research insights to actionable learning pathways.  

# ---

# ### **4. Ensuring Analytical Rigor and Originality**  
# - Emphasize **cause-and-effect reasoning** rather than presenting isolated data points.  
# - Ensure **each argument is well-supported** with logical justifications **before drawing conclusions**.  
# - Explore **alternative theories, limitations, and counterpoints** actively to preemptively address counterarguments.  
# - **Avoid overly descriptive writing**—critical engagement with concepts and arguments is necessary.  
# - Structure arguments so that **conclusions come only after sufficient analytical buildup**.  
# - Ensure the report demonstrates **original thought**, even when directly integrating provided source materials.  
# - Derive insights primarily from **#current_learnings**, ensuring usage of facts, data, and concrete evidence.

# ---

# ### **5. Formatting and Length Requirements**  
# - **Minimum word count**: 10000 words (preferably 12000 words).  
# - Use **clear section headings** to enhance readability.  
# - **Citations and references** are required for sourced content.  
# - Follow an **academic citation standard** (such as APA, MLA, or Chicago format).  
# - Structure paragraphs with well-defined topic sentences and smooth transitions.

# ---

# ## **Deliverables and Evaluation Criteria**  
# The final report should be:  
# ✔ **Comprehensive**: Detailed exploration of the research subject, addressing all key elements.  
# ✔ **Logically structured**: Coherent progression of ideas with well-defined sections.  
# ✔ **Well-supported**: Uses citations, research findings, and logical arguments.  
# ✔ **Critically engaged**: Actively synthesizes findings rather than restating facts.  
# ✔ **Readability-focused**: Balances in-depth analysis with accessibility for a broader audience.  

# Ensure all sections maintain **strong analytical depth**, and avoid summarizing information without deeper engagement. **Each section should logically lead to the next, culminating in properly justified conclusions.**
# """.strip()

# generate_report_research = [{
#     "role": "system",
#     "content": system_prompt_generate_report_research
# }]


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



system_prompt_extract_title_n_one_sentence = """
Based on the **Report Block**, extract key information from the **Reference Summary** to generate a two-line output.

# Input Format

The input consists of:
- **Report Block**: Starts with "**Report Block**:"
- **Reference Summary**: Follows the Report Block and starts with "**Reference Summary:**"

The **Reference Summary** follows this structure:
# [Title]
**Executive Summary**  
*A detailed summary of the key points using simple language.*

**Detailed Summary**  
*A more detailed exposition, no longer than one page.*

# Task

1. **Extract the Title**  
   - Identify the title from the Reference Summary, which is usually the first line.

2. **Select the Most Relevant Statement**  
   - Find a single sentence most relevant to the **Report Block** from either:
     - The **Detailed Summary**, or  
     - The **Executive Summary**  
   - This sentence should best support the **Report Block**.

# Output Format

The response should be in the following format:

**Reference Title**: [Extracted title]
**Statement**: [Most relevant extracted sentence]

# Notes

- The extracted statement should be concise and directly support the **Report Block**.
- Prioritize sentences that clearly relate to the **Report Block**'s content.
- Ensure the title is correctly extracted without modification.


# Example  

### **Input:**  
```
**Report Block**: 
The impact of climate change on agriculture has intensified over the past decade.  

**Reference Summary**:  
# Climate Change and Agriculture  
**Executive Summary**  
Climate change is affecting crop yields worldwide.  

**Detailed Summary**  
Studies indicate that rising temperatures and irregular rainfall patterns are major challenges for farmers. Sustainable farming practices are being promoted as a solution to mitigate risks.  Climate change has led to unpredictable weather patterns, affecting crop yields worldwide.  
```  

### **Output:**  
**Reference Title**: Climate Change and Agriculture  
**Statement**: Climate change has led to unpredictable weather patterns, affecting crop yields worldwide.  
""".strip()

extract_title_n_one_sentence = [{
    "role": "system",
    "content": system_prompt_extract_title_n_one_sentence
}]


system_prompt_research_toc = f"""
Generate a detailed and logically structured Table of Contents for a research report based on preceding multi-turn user-assistant dialogues and user-provided contextual materials.

Your task is to analyze the full structured input, including the initial research question, clarifying questions and responses, and any supplemental context provided by the user. From this, formulate a coherent Table of Contents (ToC) that reflects the user's research intent and interprets the depth and direction of the inquiry. Ensure coherence across sections, integrating user-supplied topics and relevant categories.

# Constraints
- The Table of Contents must include a maximum of **8 main sections**
- The ToC must begin with the **Research Title**, followed by:
   1. Introduction
   2. Literature Review
   3. 3–5 topic-specific body sections derived from user input
   4. Final section: Discussion / Future Considerations
- Each section must include a **section title** and **up to 3 bullet points** describing key content to be covered in that section.
- Use the following separators to bound each section explicitly:
  - Start each section with a line: {section_separator_begin}
  - End each section with: {section_separator_end}

# Input Format
Input will be provided as a list of structured dialogue messages in the following format:

```python
[
    {{"role": "assistant", "content": "What is your research question?"}},
    {{"role": "user", "content": "#user_initial_query"}},
    {{"role": "assistant", "content": "#followup_questions"}},
    {{"role": "user", "content": "#user_followup_answers"}},
    {{"role": "user", "content": "Additional context 1: #current_learnings"}},
    {{"role": "user", "content": "Additional context 2: #current_learnings"}}
]
```

Pay special attention to:
- The user’s core research question or topic
- Clarifications that refine scope or objectives
- External insights, references, or theories that shape the research framing

# Output Format

Your output must follow this structure:
- First line: `Title: [Determined Research Title]`
- Then, for each main section (1–8), wrap the section with:
  - A header {section_separator_begin}
  - Between the separators:
     - A numeric section heading and title (e.g., `1. Introduction`)
     - 3-5 bullet points explaining what will be covered in that section
  - End with {section_separator_end}

# Example

Title: The Impact of Climate Change on Marine Biodiversity  
{section_separator_begin}
1. Introduction  
- Provide background on climate change and its relevance to marine ecosystems  
- Explain the objective of studying biodiversity in changing ocean environments  
- Clearly state the central research questions guiding this report  
{section_separator_end}

{section_separator_begin}
2. Literature Review  
- Summarize key findings from prior studies on marine biodiversity  
- Review evidence supporting links between specific climate variables and biodiversity loss  
- Integrate findings from user-provided sources and benchmarks  
{section_separator_end}

(...additional sections...)

# Notes
- Ensure the structure is usable for generating full sections later.
- Do not include more than 8 main sections total.
- Start with analysis of user inputs before generating the ToC.
- Bullets should be conceptually rich and informative, without full paragraph narration.
- Output everything in raw markdown/plaintext (no code blocks).
""".strip()

messages_research_report_toc = [{
    "role": "system",
    "content": system_prompt_research_toc
}]


def section_generation_messages(section_summary, accumulated_content):
    section_prompt = (
            f"Generate detailed content for at least 3000 words based on the materials in '{section_summary}'. "
            "Do not generate a section title or any subheadings. Focus on writing long, cohesive paragraphs that flow naturally from the prior content, maintaining a consistent narrative and argumentative trajectory."
            "Use the following materials as your primary sources: - A list of assistant and user messages (including research questions and follow-ups). - The `Additional context` (online research provided by the user). Extract key ideas, arguments, and factual evidence from these materials. Ideally including relevant quotations, paraphrases, or citations where appropriate."
            "Here is what has been generated so far:\n\n" + accumulated_content
        )
    
    messages_section_generation = [{"role": "system", "content": section_prompt}]
    return messages_section_generation 