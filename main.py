from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from DB_operations import connect_to_mongo, insert_documents, load_json_file, cleanup_file, get_all_notes_by_pdf
from tab_Generation import convert_notes_to_tab
import tempfile

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
collection = connect_to_mongo()

# Fetch notes for a given song (source_pdf)
@app.get("/api/notes", response_model=List[Dict])
async def get_notes(song: str):
    """
    Returns all note objects for a given source_pdf (song name).
    """
    try:
        notes = get_all_notes_by_pdf(song, collection)
        if not notes:
            return []
        return notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notes: {str(e)}")


# Upload JSON and insert into MongoDB
@app.post("/api/upload-json")
async def upload_json(file: UploadFile, source_pdf: str = Form(...)) -> Dict[str, str]:
    """
    Upload a JSON file and insert data into MongoDB for the given source_pdf.
    """
    try:
        # Save temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(await file.read())
        temp_file.close()

        # Load and insert
        json_data = load_json_file(temp_file.name)
        inserted_count = insert_documents(json_data, collection, source_pdf)

        # Cleanup
        cleanup_file(temp_file.name)

        return {"message": f"{inserted_count} documents inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# Generate tab for a given song
@app.get("/api/tab", response_model=Dict[str, str])
async def get_tab(song: str):
    """
    Generate and return the tab text for the given song.
    """
    try:
        notes_data = get_all_notes_by_pdf(song, collection)
        if not notes_data:
            return {"tab": "No notes found for this song."}

        tab_text = convert_notes_to_tab(notes_data)
        return {"tab": tab_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
