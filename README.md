What it does:

MCP client acts as a bridge between an AI application  and Google Calendar MCP servers and make the below tools available to the LLM (model - o4-mini-2025-04-16).
LLM Will use these tools to act on the task given by user.

> Tool: list_calendars - List all calendars
> Tool: list_calendar_events - Get events from a calendar
> Tool: create_calendar_event - Create a calendar event  
> Tool: get_calendar_event - Get a calendar event        
> Tool: edit_calendar_event - Edit a calendar event      
> Tool: delete_calendar_event - Delete a calendar event  

How to run:

pip install -r requirements.txt
python mcpusinglanggraph.py

Output: Google calendar event will get created 
<img width="2843" height="766" alt="image" src="https://github.com/user-attachments/assets/c833f951-003b-44e2-8aff-c63e49ffb7b1" />

