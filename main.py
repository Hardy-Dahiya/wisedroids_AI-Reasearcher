import os
import streamlit as st
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def set_openai_api_key(api_key):
    """Set the OpenAI API key as an environment variable."""
    os.environ["OPENAI_API_KEY"] = api_key
    # Also set it for the openai package
    openai.api_key = api_key

def validate_api_key(api_key):
    """Validate the OpenAI API key by making a simple API call."""
    try:
        # Set the API key
        set_openai_api_key(api_key)
        
        # Try to list models as a simple validation
        openai.models.list()
        return True
    except Exception as e:
        st.error(f"API key validation failed: {str(e)}")
        return False

def run_research(topic):
    """Run the research task with CrewAI."""
    try:
        # Define the agent
        researcher = Agent(
            role="Researcher",
            goal=f"Gather information on {topic} and summarize it",
            backstory="You are an expert researcher skilled at finding and condensing information.",
            verbose=True,
            allow_delegation=False
        )

        # Define the task
        research_task = Task(
            description=f"Research the topic '{topic}' and write a short summary.",
            expected_output=f"A concise summary of {topic}, about 100 words.",
            agent=researcher
        )

        # Create the crew and assign the task
        crew = Crew(
            agents=[researcher],
            tasks=[research_task],
            verbose=True
        )

        # Execute the crew's task
        with st.spinner(f"Researching '{topic}'... This may take a minute."):
            result = crew.kickoff()
        
        return result
    except Exception as e:
        st.error(f"An error occurred during research: {str(e)}")
        return None

# Set up the Streamlit app
st.title("AI Research Assistant")

# Sidebar for API key
st.sidebar.title("Authentication")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# Check if API key is provided
if api_key:
    if validate_api_key(api_key):
        st.sidebar.success("API key validated successfully!")
        
        # Main app content
        st.write("This app uses CrewAI to research topics and provide summaries.")
        
        # Input for research topic
        topic = st.text_input("Enter a research topic:", value="Artificial Intelligence Trends in 2025")
        
        if st.button("Research Topic"):
            if topic:
                result = run_research(topic)
                if result:
                    st.subheader("Research Summary:")
                    st.write(result)
            else:
                st.warning("Please enter a topic to research.")
    else:
        st.sidebar.error("Invalid API key. Please check and try again.")
else:
    st.info("Please enter your OpenAI API key in the sidebar to use this application.")
    st.write("This application requires an OpenAI API key to function. Your key is used only for the current session and is not stored.")
