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
    help="Enter your OpenAI API key. Your key is not stored and is only used for the current session.",
    placeholder="sk-..."
)

# Main app
st.title("AI Research Assistant")
st.markdown("This app uses CrewAI to research topics and provide summaries.")

# Check if API key is provided
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
else:
    # Set the API key
    set_openai_api_key(api_key)
    
    try:
        # Main functionality
        st.subheader("Research Topic")
        
        # Input for research topic
        research_topic = st.text_input(
            "Enter a topic to research:",
            value="Artificial Intelligence Trends in 2025",
            help="Specify the topic you want to research"
        )
        
        # Input for summary length
        summary_length = st.slider(
            "Summary length (words):",
            min_value=50,
            max_value=500,
            value=100,
            step=50,
            help="Specify how long the summary should be"
        )
        
        # Button to start research
        if st.button("Start Research"):
            with st.spinner("Researching... This may take a minute or two."):
                try:
                    # Define the agent
                    researcher = Agent(
                        role="Researcher",
                        goal=f"Gather information on {research_topic} and summarize it",
                        backstory="You are an expert researcher skilled at finding and condensing information.",
                        verbose=True,
                        allow_delegation=False
                    )
                    
                    # Define the task
                    research_task = Task(
                        description=f"Research the topic '{research_topic}' and write a short summary.",
                        expected_output=f"A concise summary of {research_topic}, about {summary_length} words.",
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
                    
                except openai.error.AuthenticationError:
                    st.error("Authentication Error: The OpenAI API key you provided is invalid.")
                except openai.error.RateLimitError:
                    st.error("Rate Limit Error: You've exceeded your OpenAI API rate limit.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
    
    except Exception as e:
        st.error(f"Error setting up the application: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown(
    "This application uses CrewAI and OpenAI to research topics and generate summaries. "
    "Your API key is only used for the current session and is not stored."
)
