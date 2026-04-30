import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from config.settings import settings
from src.nlp.utils import safe_json_loads

# Use the API key from our centralized config
os.environ["OPENAI_API_KEY"] = settings.NVIDIA_API_KEY
os.environ["OPENAI_API_BASE"] = settings.OPENAI_API_BASE

# Initialize the LLM using the native CrewAI LLM class wrapper for Litellm
llm = LLM(
    model="openai/meta/llama-3.1-405b-instruct",
    base_url=settings.OPENAI_API_BASE,
    api_key=settings.NVIDIA_API_KEY,
    temperature=0.1
)

# -------------------------
# 1. DEFINE THE AGENTS
# -------------------------
extractor_agent = Agent(
    role="Senior Data Extraction Specialist",
    goal="Accurately extract structured disaster task data from messy, unstructured NGO reports.",
    backstory="You are a highly analytical AI trained by the Red Cross to rapidly scan through chaotic field reports, emails, and PDFs to extract the exact 'Task Description' and 'People Count' so ground forces can deploy immediately.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

translator_agent = Agent(
    role="Multilingual Communications Officer",
    goal="Translate crucial disaster response reports into multiple languages for international volunteers.",
    backstory="You are an expert translator working at the UN. Given an English task description, your job is to translate the core actionable sentence into Spanish and French so international NGOs can understand the need.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# -------------------------
# 2. RUN THE PIPELINE
# -------------------------
def process_ngo_report(unstructured_report: str, temperature=0.1):
    print(f"Starting CrewAI Processing Pipeline with temp={temperature}...")
    
    # Update LLM temperature for this specific run if needed
    # Note: In a production app, you might want to create a new LLM instance
    llm.temperature = temperature
    
    extract_task = Task(
        description=f"Read the following chaotic NGO field report and extract 1 clean, actionable 'Task Description' and the 'People Count'.\n\nReport:\n'{unstructured_report}'\n\nReturn ONLY a valid JSON format exact format: {{\"description\": \"...\", \"people_count\": 5}}",
        expected_output="A JSON object containing 'description' and 'people_count'.",
        agent=extractor_agent
    )
    
    translate_task = Task(
        description="Take the extracted JSON and add two new fields: 'description_es' (Spanish translation of the description) and 'description_fr' (French translation). Output the final JSON.",
        expected_output="A complete JSON object with the original 'description', 'people_count', and both translated descriptions.",
        agent=translator_agent
    )
    
    ngo_crew = Crew(
        agents=[extractor_agent, translator_agent],
        tasks=[extract_task, translate_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the crew
    result = ngo_crew.kickoff()
    
    # Use robust JSON parsing utility
    return safe_json_loads(str(result.raw), fallback={"description": str(result.raw), "people_count": 1})


# -------------------------
# 3. TEST SCRIPT
# -------------------------
if __name__ == "__main__":
    # We mock an unstructured report that would normally be uploaded as a PDF
    mock_pdf_transcript = """
    Field Report #884A - 04/17/2026:
    It's chaos down near Sector 4 (City Square). The river broke the banks and flooded the main roads. 
    We currently have a group of around thirty-five people stranded on the roof of the old library. 
    They are out of food and the water is rising. We urgently need a supply drop of rations and fresh 
    drinking water transported to them via heavy truck or boat if possible. Over and out.
    """
    
    final_output = process_ngo_report(mock_pdf_transcript)
    print("\n\n=== FINAL CREW AI TASK OUTPUT ===")
    print(final_output)
    
    # Notice how this cleanly maps to our data/sample_tasks.json database!
