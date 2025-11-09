import uuid
from datetime import datetime, timedelta

sessions = {}

# Session expires after 30 min of inactivity
SESSION_TIMEOUT = timedelta(minutes=30)


def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"messages": [], "last_used": datetime.now()}
    return session_id


def get_session_messages(session_id):
    if session_id not in sessions:
        return None

    session = sessions[session_id]
    session["last_used"] = datetime.now()

    return session["messages"]


def add_message(session_id, message):
    if session_id in sessions:
        sessions[session_id]["messages"].append(message)
        sessions[session_id]["last_used"] = datetime.now()


def cleanup_old_sessions():
    now = datetime.now()
    expired = []
    for sid, data in sessions.items():
        if now - data["last_used"] > SESSION_TIMEOUT:
            expired.append(sid)

    for sid in expired:
        del sessions[sid]
