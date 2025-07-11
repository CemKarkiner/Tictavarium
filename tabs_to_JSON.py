import os
import subprocess
import xml.etree.ElementTree as ET
import json
import zipfile
import glob

INPUT_PDF = r"C:\Users\ASUS\Downloads\GuitarLick.pdf"
PROJECT_DIR = os.path.abspath(os.getcwd())
OUTPUT_DIR = os.path.join(PROJECT_DIR, "audiveris_output")
AUDIVERIS_JAR = r"C:\Users\ASUS\audiveris\app\build\libs\audiveris-all-5.6.1-all.jar"
JAVA_21_PATH = r"C:\Program Files\Java\jdk-21\bin\java.exe"
MUSICXML_PATH = r"C:\Users\ASUS\audiveris\output\extracted_mxl\GuitarLick.xml"


def run_omr_batch(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = [
        JAVA_21_PATH,
        "-jar",
        AUDIVERIS_JAR,
        "-batch",
        pdf_path,
        "-output=" + output_dir
    ]

    print("OMR batch processing started...")
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(AUDIVERIS_JAR))
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print(f"OMR batch işlem hatası: {result.returncode}")
        exit(1)
    print("OMR batch processing done.")


def run_export(omr_path):
    command = [
        JAVA_21_PATH,
        "-jar",
        AUDIVERIS_JAR,
        "-export",
        omr_path
    ]

    print("Exporting MusicXML from OMR...")
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.path.dirname(AUDIVERIS_JAR))
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    if result.returncode != 0:
        print(f"Export hata ile sonlandı: {result.returncode}")
        exit(1)
    print("Export Done.")


def extract_mxl(mxl_path, extract_dir):
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    with zipfile.ZipFile(mxl_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Extracted all files to {extract_dir}")

    for file in os.listdir(extract_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(extract_dir, file)
            print(f"Found XML file: {xml_path}")
            return xml_path

    print("XML dosyası .mxl içinden çıkarılamadı.")
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
    # 1. PDF → OMR
    run_omr_batch(INPUT_PDF, OUTPUT_DIR)

    # 2. OMR dosyasını bul
    omr_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.omr"), recursive=True)
    if not omr_files:
        print("OMR dosyası bulunamadı.")
        exit(1)

    # 3. OMR → .mxl export
    for omr_file in omr_files:
        run_export(omr_file)

    # 4. .mxl dosyasını bul
    mxl_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.mxl"), recursive=True)
    if not mxl_files:
        print("MXL dosyası bulunamadı.")
        exit(1)
    mxl_path = mxl_files[0]

    # 5. .mxl içinden XML çıkar
    extracted_dir = os.path.join(OUTPUT_DIR, "extracted_mxl")
    xml_path = extract_mxl(mxl_path, extracted_dir)
    if not xml_path:
        print("XML dosyası bulunamadı.")
        exit(1)

    # 6. XML → JSON
    json_data = parse_musicxml_to_json(xml_path)
    json_output_path = os.path.join(PROJECT_DIR, "output.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"JSON çıktı dosyası oluşturuldu: {json_output_path}")
