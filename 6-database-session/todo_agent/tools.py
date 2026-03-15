from google.adk.tools.tool_context import ToolContext

def addToDo(toDo: str, tool_context: ToolContext) -> dict:
    """Add a new ToDo to the user's ToDo list.

    Args:
        ToDo: The ToDo text to add
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    # Get current state 
    todo_list = tool_context.state.get("todo_list", [])

    todo_list.append(toDo)

    # update the state 
    tool_context.state["todo_list"] = todo_list

    return {
        "action": "Add ToDo item",
        "todo_item": toDo,
        "message": f"Added To Do item: {toDo}"
    }

def viewToDo(tool_context: ToolContext) -> dict:
    """View all current to-dos.

    Args:
        tool_context: Context for accessing session state

    Returns:
        The list of to-dos
    """
    todo_list = tool_context.state.get("todo_list", [])
    return {
        "action": "view ToDo list",
        "todo_list": todo_list,
        "count": len(todo_list)
    }

def updateToDo(index: int, update_text: str, tool_context: ToolContext) -> dict:
    """Update an existing to-do.

    Args:
        index: The 1-based index of the to-do to update
        updated_text: The new text for the to-do
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    todo_list = tool_context.state.get("todo_list", [])

    if not todo_list or index < 1 or index > len(todo_list):
        return {
            "action": "update ToDo item",
            "status": "error",
            "message": f"Could not find a to-do item at index {index}. Length of the list is: {len(todo_list)}"
        }
    
    old_todo = todo_list[index - 1]
    todo_list[index - 1] = update_text

    tool_context.state["todo_list"] = todo_list

    return {
        "action": "update To Do item",
        "index": index,
        "old_todo": old_todo,
        "updated_todo": update_text,
        "message": f"Updated To Do item at index {index} from {old_todo} to {update_text}"
    }

def deleteToDo(index: int, tool_context: ToolContext) -> dict:
    """Delete a to-do.

    Args:
        index: The 1-based index of the to-do to delete
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    todo_list = tool_context.state.get("todo_list", [])

    if not todo_list or index < 1 or index > len(todo_list):
        return {
            "action": "delete ToDo item",
            "status": "error",
            "message": f"Could not find a to-do item to delete at index {index}. Length of the list is: {len(todo_list)}"
        }
    
    deleted_item = todo_list.pop(index - 1)
    tool_context.state["todo_list"] = todo_list

    return {
        "action": "delete ToDo item",
        "index": index,
        "deleted_todo": deleted_item,
        "message": f"Deleted To Do item {deleted_item} at index {index} from th list"
    }

def update_username(userName: str, tool_context: ToolContext) -> dict:
    """Update the user's name.

    Args:
        name: The new name for the user
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message
    """
    old_name = tool_context.state.get("user_name", "")
    tool_context.state["user_name"] = userName

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": userName,
        "message": f"Updated your name to: {userName}",
    }