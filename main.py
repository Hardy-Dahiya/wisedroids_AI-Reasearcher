import os
import streamlit as st
from crewai import Agent, Task, Crew
import openai

# Set page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Function to set OpenAI API key
def set_openai_api_key(api_key):
    """Set the OpenAI API key as an environment variable."""
    os.environ["OPENAI_API_KEY"] = api_key
    return api_key

# Sidebar for API key input
st.sidebar.title("Authentication")
st.sidebar.markdown("Please enter your OpenAI API key to use this application.")

api_key = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key. Your key is not stored and only used for the current session.",
    placeholder="sk-..."
)

if api_key:
    try:
        # Set the API key
        set_openai_api_key(api_key)
        st.sidebar.success("API key set successfully!")
        authenticated = True
    except Exception as e:
        st.sidebar.error(f"Error setting API key: {str(e)}")
        authenticated = False
else:
    authenticated = False
    st.sidebar.warning("Please enter your OpenAI API key to proceed.")

# Main application
st.title("AI Research Assistant")
st.markdown("This application uses CrewAI to research topics and provide summaries.")

if authenticated:
    # Input for research topic
    research_topic = st.text_input(
        "Research Topic",
        value="Artificial Intelligence Trends in 2025",
        help="Enter the topic you want to research"
    )
    
    # Run button
    if st.button("Run Research", type="primary"):
        with st.spinner("Researching... This may take a minute or two."):
            try:
                # Define the agent
                researcher = Agent(
                    role="Researcher",
                    goal="Gather information on a given topic and summarize it",
                    backstory="You are an expert researcher skilled at finding and condensing information.",
                    verbose=True,
                    allow_delegation=False
                )

                # Define the task
                research_task = Task(
                    description=f"Research the topic '{research_topic}' and write a short summary.",
                    expected_output="A concise summary of the topic, about 100 words.",
                    agent=researcher
                )

                # Create the crew and assign the task
                crew = Crew(
                    agents=[researcher],
                    tasks=[research_task],
                    verbose=True
                )

                # Execute the crew's task
                result = crew.kickoff()
                
                # Display the result
                st.success("Research completed!")
                st.subheader("Research Summary:")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"An error occurred during research: {str(e)}")
                st.info("This could be due to an invalid API key or a connection issue. Please check your API key and try again.")
    
    # Additional information
    with st.expander("How it works"):
        st.markdown("""
        This application uses CrewAI to:
        1. Create a researcher agent with specific goals and backstory
        2. Assign a research task to the agent
        3. Execute the task to generate a summary of the requested topic
        
        The agent uses your OpenAI API key to access language models for generating the research summary.
        """)
else:
    # Show instructions when not authenticated
    st.info("Please enter your OpenAI API key in the sidebar to use this application.")
    
    st.markdown("""
    ### How to get an OpenAI API key:
    1. Go to [OpenAI's platform](https://platform.openai.com/signup)
    2. Create an account or sign in
    3. Navigate to the API section
    4. Generate a new API key
    5. Copy and paste it into the sidebar
    
    Your API key is only used for the current session and is not stored permanently.
    """)
