import os
import subprocess
import xml.etree.ElementTree as ET
import zipfile
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json
import shutil
from DB_operations import connect_to_mongo, insert_documents, cleanup_file


audiveris_jar = r"C:\Users\ASUS\audiveris\app\build\libs\audiveris-all-5.6.1-all.jar"
java_path = r"C:\Program Files\Java\jdk-21\bin\java.exe"

def ask_user_inputs():
    root = tk.Tk()
    root.withdraw()

    pdf_path = filedialog.askopenfilename(
        title="Select Sheet Music PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not pdf_path:
        messagebox.showerror("Input Error", "No PDF file selected.")
        exit(1)

    return pdf_path

def run_omr_batch(pdf_path, output_dir, java_path, audiveris_jar):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [
        java_path,
        "-cp",
        f"{audiveris_jar};C:\\Users\\ASUS\\audiveris\\lib\\*",
        "Audiveris",
        "-batch",
        pdf_path,
        f"-output={output_dir}"
    ]

    print("OMR batch processing started...")
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(audiveris_jar))
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print(f"OMR batch error: {result.returncode}")
        exit(1)
    print("OMR batch processing done.")

def run_export(omr_path, java_path, audiveris_jar):
    command = [
        java_path,
        "-jar",
        audiveris_jar,
        "-export",
        omr_path
    ]

    print("Exporting MusicXML from OMR...")
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(audiveris_jar))
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print(f"Export error: {result.returncode}")
        exit(1)
    print("Export Done.")

def extract_mxl(mxl_path, extract_dir):
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(mxl_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    for file in os.listdir(extract_dir):
        if file.endswith(".xml"):
            return os.path.join(extract_dir, file)
    return None

def parse_musicxml_to_json(musicxml_path):
    tree = ET.parse(musicxml_path)
    root = tree.getroot()

    ns = {'': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}
    data = []

    for part in root.findall("part", ns):
        part_id = part.attrib.get("id", "unknown")
        for measure in part.findall("measure", ns):
            measure_data = {
                "part": part_id,
                "measure": measure.attrib.get("number", "0"),
                "notes": []
            }
            for note in measure.findall("note", ns):
                note_info = {}
                pitch = note.find("pitch", ns)
                duration = note.find("duration", ns)

                if pitch is not None:
                    step = pitch.find("step", ns)
                    octave = pitch.find("octave", ns)
                    note_info["note"] = f"{step.text}{octave.text}" if step is not None and octave is not None else "unknown"
                elif note.find("rest", ns) is not None:
                    note_info["note"] = "rest"
                else:
                    note_info["note"] = "unknown"

                note_info["duration"] = duration.text if duration is not None else "unknown"
                measure_data["notes"].append(note_info)

            data.append(measure_data)
    return data

if __name__ == "__main__":
    pdf_path = ask_user_inputs()
    pdf_name = os.path.basename(pdf_path)
    project_dir = os.getcwd()
    output_dir = os.path.join(project_dir, "audiveris_output")

    # 1. PDF → OMR
    run_omr_batch(pdf_path, output_dir, java_path, audiveris_jar)

    # 2. Find OMR file
    omr_files = glob.glob(os.path.join(output_dir, "**", "*.omr"), recursive=True)
    if not omr_files:
        print("No OMR file found.")
        exit(1)

    # 3. OMR → MXL Export
    for omr_file in omr_files:
        run_export(omr_file, java_path, audiveris_jar)

    # 4. Find MXL
    mxl_files = glob.glob(os.path.join(output_dir, "**", "*.mxl"), recursive=True)
    if not mxl_files:
        print("No MXL file found.")
        exit(1)
    mxl_path = mxl_files[0]

    # 5. MXL → XML
    extract_dir = os.path.join(output_dir, "extracted_mxl")
    xml_path = extract_mxl(mxl_path, extract_dir)
    if not xml_path:
        print("No XML file extracted.")
        exit(1)

    # 6. XML → JSON
    json_data = parse_musicxml_to_json(xml_path)
    pdf_name = os.path.basename(pdf_path)
    pdf_name = re.sub(r"\.pdf$", "", pdf_name, flags=re.IGNORECASE)
    for doc in json_data:
        doc["source_pdf"] = pdf_name

    json_path = os.path.join(project_dir, "output.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # 7. Geçici klasörü sil
    try:
        shutil.rmtree(output_dir)
    except Exception as e:
        print(e)

    # 8. JSON → MongoDB
    try:
        collection = connect_to_mongo()
        count = insert_documents(json_data, collection, pdf_name)
        print(f"MongoDB'ye {count} belge yüklendi.")

        # JSON dosyasını sil
        cleanup_file(json_path)

    except Exception as e:
        print("MongoDB yükleme hatası:", e)