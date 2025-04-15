import json
import os
import sys
import asyncio  # Added to enable async execution

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.ai import get_ai_responses
from src.utils import ModelType


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


async def main():
    filepath = "output/saved_messages.json"
    messages = load_messages(filepath)
    print("Loaded messages for generating report:")

    updated_messages = generate_report_research + messages

    report = await get_ai_responses(messages=updated_messages, model=ModelType.SUMMARIZING)

    short_desc = "test_prompt"
    output_filename = os.path.join("output", f"research_result_{short_desc}.md")
    os.makedirs("output", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Final report saved to {output_filename}\n")


if __name__ == "__main__":
    asyncio.run(main())