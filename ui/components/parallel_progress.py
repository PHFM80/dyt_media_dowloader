#ui\components\parallel_progress.py
import streamlit as st
from models.download_task import DownloadTask

def render_parallel_progress(tasks: list[DownloadTask], total: int):
    """Muestra el progreso global y el estado individual de cada tarea."""
    completed = sum(1 for t in tasks if t.status == "completed")
    failed = sum(1 for t in tasks if t.status == "failed")
    downloading = sum(1 for t in tasks if t.status == "downloading")
    
    st.progress(completed / total if total > 0 else 0)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Completados", completed)
    col2.metric("En progreso", downloading)
    col3.metric("Fallidos", failed)
    
    st.markdown("---")
    
    with st.container(height=300):
        for task in tasks:
            icon = "⏳" if task.status == "pending" else "🔄" if task.status == "downloading" else "✅" if task.status == "completed" else "❌"
            
            title = task.video_info.get("title", "Desconocido") if task.video_info else "Obteniendo info..."
            status_text = task.error_message if task.status == "failed" else f"{task.progress:.0f}%" if task.status == "downloading" else "Listo"
            
            st.markdown(f"**{icon} {title}**")
            st.caption(f"Calidad: {task.quality} | Estado: {status_text}")
            st.divider()