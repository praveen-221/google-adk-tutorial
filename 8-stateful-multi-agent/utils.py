from datetime import datetime
from google.genai import types

async def add_interaction_history(session_service, app_name, session_id, user_id, record):
    """
        Add an entry to the interaction history in state.

        Args:
            session_service: The session service instance
            app_name: The application name
            user_id: The user ID
            session_id: The session ID
            entry: A dictionary containing the interaction data
                - requires 'action' key (e.g., 'user_query', 'agent_response')
                - other keys are flexible depending on the action type
    """
    try:
        session = await session_service.get_session(
            app_name = app_name, session_id = session_id, user_id = user_id
        )

        interaction_history = session.state.get("interaction_history", [])

        if "timestamp" not in record:
            record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        interaction_history.append(record)
        session.state["interaction_history"] = interaction_history
    except Exception as e:
        print(f"Error while adding interaction: {e}")

    return

async def add_agent_response(session_service, app_name, session_id, user_id, query):
    """Add a user query to the interaction history."""
    await add_interaction_history(
        session_service,
        app_name,
        session_id,
        user_id,
        {
            "action": "user_query",
            "query": query
        }
    )
    return

async def add_agent_response(session_service, app_name, session_id, user_id, agent_name, response):
    """Add an agent response to the interaction history."""
    await add_interaction_history(
        session_service,
        app_name,
        session_id,
        user_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response
        }
    )
    return

async def display_state(session_service, app_name, session_id, user_id, label = "CURRENT STATE"):
    """
        Displays the session state at the time of invocation
    """
    try:
        # get the session 
        session = await session_service.get_session(
            app_name = app_name, session_id = session_id, user_id = user_id
        )

        print(f"{'-'*10} {label} {'-'*10}")

        userName = session.state.get("user_name", "Unknown")
        print(f"User name: {userName}")

        purchased_courses = session.state.get("purchased_courses", [])
        if purchased_courses and any(purchased_courses):
            print(f"Purchased course list:")
            for idx, course in enumerate(purchased_courses, 1):
                if isinstance(course, dict):
                    course_id = course.get("id", "Unknown")
                    purchased_date = course.get("purchase_date", "Unknown Date")
                    print(f"\t{idx}) {course_id} purchased on {purchased_date}")
                elif course: 
                    print(f"\t{idx}) {course}")
        else:
            print(f"Purchased course list: None")

        interactions = session.state.get("interaction_history", [])
        if interactions and any(interactions):
            print(f"Session Interaction History:")
            for idx, interaction in enumerate(interactions, 1):
                if isinstance(interactions, dict):
                    action = interactions.get("action", "interaction")
                    timestamp = interactions.get("timestamp", "unknown timestamp")

                    if action == "user_query":
                        query = interaction.get("query", "")
                        print(f"\t{idx}) User query at {timestamp}: {query}")
                    elif action == "agent_response":
                        agent_name = interaction.get("agent_name", "")
                        agent_response = interaction.get("response", "")
                        # truncate respone 
                        if len(agent_response) > 100:
                            agent_response = agent_response[:97] + "..."
                        print(f"\t{idx}) {agent_name} response at {timestamp}: {agent_response}") 
                    else:
                        logs = "".join(
                            f"{k}: {v}"
                            for k, v in interaction.items()
                            if k not in ["action", "timestamp"]
                        )
                        print(
                            f"\t{idx}) {action} at {timestamp}"
                            + f"{logs}" if logs else ""
                        )
                else:
                    print(f"\t{idx}) {interaction}")
        else:
            print(f"Interaction history: None")
        print(f"{'-' * (22 + len(label))}")
        
    except Exception as e:
        print(f"Error while fetching ad displaying the session state: {e}")
        print(f"{'-' * (22 + len(label))}")
    return

async def process_agent_response(event):
    """
        Process agent response event
    """
    # Log event info
    print(f"Event id: {event.id} \t Author: {event.author}")

    # check for differnt parts in event response
    has_specific_parts = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"Debug: {part.text.strip()}")
                has_specific_parts = True
    
    # get final response of the event
    final_response = None
    if event.is_final_response():
        if(
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            # get the final response of the agent and remove trailing spaces
            final_response = event.content.parts[0].text.strip()
            print(f"Agent: {final_response}\n")
        else: 
            print(f"No text content present in the final response of the agent.")
    return final_response

async def call_agent_async(runner, message, session_id, user_id):
    """Call the agent asynchronously with the user's query."""
    final_response = None
    agent_name = None

    # display state of the session before event
    await display_state(runner.session_service, runner.app_name, session_id, user_id, label="INITIAL STATE")

    try:
        query = types.Content(
            role = "user", parts = [types.Part(text=message)]
        )
        async for event in runner.run_async(
            user_id = user_id,
            session_id = session_id,
            new_message = query
        ):
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response = response
    except Exception as e:
        print(f"Error during agent call: {e}")

    # Add the agent response to interaction history if we got a final response
    await add_agent_response(
        session_service = runner.session_service,
        app_name = runner.app_name,
        session_id = session_id,
        user_id = user_id,
        agent_name = agent_name,
        response = final_response
    )

    # display state of the session after event
    await display_state(runner.session_service, runner.app_name, session_id, user_id)
    return final_response