import json
import os
import sys
import asyncio  # Added to enable async execution

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.ai import get_ai_responses
from src.utils import ModelType
from src.utils import section_separator_begin, section_separator_end
from src.progress import ProgressManager

def save_messages(messages, filepath):
    """
    Save a list of messages to a JSON file.

    Parameters:
      messages (list): The list of message dictionaries to save.
      filepath (str): The path to the file where the messages will be saved.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)


def load_messages(filepath):
    """
    Load messages from a JSON file.

    Parameters:
      filepath (str): The path to the JSON file.

    Returns:
      list: The list of messages loaded from the file.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        messages = json.load(f)
    return messages


### Generate Report ###
system_prompt_generate_report_research = """
# **Comprehensive Research Report Generation**

This task requires generating a **detailed, well-structured, and analytically rigorous** research report based on user queries, follow-up dialogues, and supplementary materials. The content must integrate user-provided context and external references while maintaining logical coherence and depth.

## **Input Format and Research Scope**

The report is guided by structured dialogue inputs, typically formatted in a Python list as follows:

```python
[
    {"role": "assistant", "content": "What is your research question?"},
    {"role": "user", "content": "#user_initial_query"},
    {"role": "assistant", "content": "#followup_questions"},
    {"role": "user", "content": "#user_followup_answers"},
    {"role": "user", "content": "Additional context 1: #current_learnings"},
    {"role": "user", "content": "Additional context 2: #current_learnings"}
]
```

### **Key Input Components:**  
- **#user_initial_query**: The primary research question or problem statement provided by the user.  
- **#followup_questions**: Clarifying and refining questions to better define the research scope.  
- **#user_followup_answers**: User responses that help shape the focus of the report.  
- **#current_learnings**: User-supplied insights from external materials, structured data, research sources, or expert opinions.  

The final report must consolidate these components into a **cohesive and in-depth analysis** that adheres to research standards.

---

## **Report Structure and Guidelines**

The comprehensive research report should follow a **logical, well-organized structure** that facilitates readability and academic rigor.

### **1. Establish a Strong Research Foundation**  
- **Title**: A concise and precise title that captures the essence of the research question and objectives.  
- **Table of Contents**: List section titles only (no subsections).  
- **Introduction** (~1000 words):  
  - Clearly define the research context, objectives, and significance.  
  - Align the research problem with relevant theoretical or practical implications.  
  - Articulate specific research questions or hypotheses that guide the study.  

---

### **2. Integration and Synthesis of Source Materials**  
All analysis must be built upon a solid foundation of reasoning before reaching conclusions:  
- Incorporate all **additional context (#current_learnings) and user-generated insights** into the analysis.  
- Establish **cause-effect relationships** with proper theoretical grounding before making claims.  
- Perform **critical evaluations** of cited materials rather than merely summarizing facts.  
- Analyze alternative viewpoints to enhance depth and rigor—arguments should be developed fully before presenting conclusions.  
- Ensure that reasoning flows **logically** from evidence to findings in a progressive, structured manner.  

---

### **3. Logical Organization and Depth**  
Each section should be **comprehensive and detailed**, ensuring analytical depth by maintaining a **minimum of two pages** per core section:  

#### **Main Sections and Minimum Length Requirements**  
- **Introduction**: Defines purpose, research significance, and key objectives (~1000 words).  
- **Literature Review**:  
  - Summarizes relevant existing research findings.  
  - Reviews key theories and conceptual models.  
  - Discusses practical applications and case studies.  
  - Presents gaps in the current research landscape with alternative perspectives.  
  - **Minimum of 5000 words.**  
- **Findings and Discussion**:  
  - Develops insights through logical reasoning and analytical rigor **before stating conclusions**.  
  - Presents supported arguments, competing perspectives, and critical debates.  
  - Evaluates challenges, limitations, biases, and possible counterarguments.  
  - Explores emerging trends and future research directions.  
  - **Minimum 1000 words.**  
- **Conclusion**:  
  - Summarizes findings concisely **while strictly deriving conclusions from previous reasoning**.  
  - Provides key takeaways, implications, and recommendations.  
- **Learning Recommendation**:  
  - Structures the most logical order of presentation for a non-expert audience.  
  - Connects research insights to actionable learning pathways.  

---

### **4. Ensuring Analytical Rigor and Originality**  
- Emphasize **cause-and-effect reasoning** rather than presenting isolated data points.  
- Ensure **each argument is well-supported** with logical justifications **before drawing conclusions**.  
- Explore **alternative theories, limitations, and counterpoints** actively to preemptively address counterarguments.  
- **Avoid overly descriptive writing**—critical engagement with concepts and arguments is necessary.  
- Structure arguments so that **conclusions come only after sufficient analytical buildup**.  
- Ensure the report demonstrates **original thought**, even when directly integrating provided source materials.  
- Derive insights primarily from **#current_learnings**, ensuring usage of facts, data, and concrete evidence.

---

### **5. Formatting and Length Requirements**  
- **Minimum word count**: 10000 words (preferably 12000 words).  
- Use **clear section headings** to enhance readability.  
- **Citations and references** are required for sourced content.  
- Follow an **academic citation standard** (such as APA, MLA, or Chicago format).  
- Structure paragraphs with well-defined topic sentences and smooth transitions.

---

## **Deliverables and Evaluation Criteria**  
The final report should be:  
✔ **Comprehensive**: Detailed exploration of the research subject, addressing all key elements.  
✔ **Logically structured**: Coherent progression of ideas with well-defined sections.  
✔ **Well-supported**: Uses citations, research findings, and logical arguments.  
✔ **Critically engaged**: Actively synthesizes findings rather than restating facts.  
✔ **Readability-focused**: Balances in-depth analysis with accessibility for a broader audience.  

Ensure all sections maintain **strong analytical depth**, and avoid summarizing information without deeper engagement. **Each section should logically lead to the next, culminating in properly justified conclusions.**
""".strip()

generate_report_research = [{
    "role": "system",
    "content": system_prompt_generate_report_research
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

async def main():
    filepath = "output/saved_messages.json"
    messages = load_messages(filepath)
    progress = ProgressManager()
    progress.update(f"Loaded messages for generating report:")  
    

    toc_messages = messages_research_report_toc + messages
    progress.update(f"Generating Table of Contents...")  
    table_of_contents = await get_ai_responses(messages=toc_messages, model=ModelType.REASONING)
    
    

    # Split the table of contents into individual section titles (assuming each non-empty line represents a section).
    lines = table_of_contents.splitlines()
    # Extract the first non-empty line as the title
    title = lines[0].strip() if lines else ""
    sections = []
    collecting = False
    current_section_str = ""
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line == section_separator_begin:
            collecting = True
            current_section_str = ""
            continue
        if cleaned_line == section_separator_end and collecting:
            collecting = False
            sections.append(current_section_str.strip())
            continue
        if collecting:
            current_section_str += cleaned_line + "\n"

    # Define an async recursive function to generate each report section, including previously generated content for continuity.
    progress.update(f"Generating Sections ...")  

   

    async def generate_sections(sections, idx=0, accumulated_content=""):
        if idx >= len(sections):
            return ""
        section_summary = sections[idx]
        # Create a prompt that includes the accumulated content to ensure smooth flow.
        progress.update(f"Generating section {idx + 1}/{len(sections)}: {section_summary}")
        # Extract the title from the first line of the section summary
        section_title = section_summary.split("\n")[0].strip()  
        section_messages = section_generation_messages(section_summary, accumulated_content) + messages

        section_content = "## "+ section_title +"\n\n" + await get_ai_responses(messages=section_messages, model=ModelType.SUMMARIZING)
        # Append current section to the accumulated content.
       
        new_accumulated_content = accumulated_content +  section_content + "\n\n"
        # Recursively generate the remaining sections with the updated context.
        remaining_content = await generate_sections(sections, idx + 1, new_accumulated_content)
        return section_content + "\n\n" + remaining_content

    # Generate the report body by recursively processing all sections.
    report_body = await generate_sections(sections)
    report = "# "+ title + "\n\n" + report_body

    short_desc = "report_test"
    output_filename = os.path.join("output", f"research_result_{short_desc}.md")
    os.makedirs("output", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Final report saved to {output_filename}\n")


if __name__ == "__main__":
    asyncio.run(main())