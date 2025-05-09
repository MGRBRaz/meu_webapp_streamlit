import streamlit as st
import pandas as pd

def display_event_log(process):
    """Display the event log for a process"""
    st.subheader("Histórico de Eventos")
    
    events = process.get("events", [])
    
    if not events:
        st.info("Nenhum evento registrado para este processo.")
        return
    
    # Convert events to dataframe for display
    events_df = pd.DataFrame(events)
    
    # Make sure columns exist
    if "date" not in events_df.columns:
        events_df["date"] = ""
    if "description" not in events_df.columns:
        events_df["description"] = ""
    if "user" not in events_df.columns:
        events_df["user"] = ""
    
    # Sort events by date (most recent first)
    events_df = events_df.sort_values(by="date", ascending=False)
    
    # Display events in a timeline format
    for i, event in events_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"**{event['date']}**")
                st.caption(f"Usuário: {event['user']}")
            
            with col2:
                st.markdown(f"{event['description']}")
            
        st.divider()
