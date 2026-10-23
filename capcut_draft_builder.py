import os
import json
import uuid
import time
import shutil

DRAFTS_ROOT = r"C:\Users\magom\AppData\Local\CapCut Drafts"
PROJECT_NAME = "Price_Glitch_Promo_Viral"
PROJECT_DIR = os.path.join(DRAFTS_ROOT, PROJECT_NAME)
ROOT_META_FILE = r"C:\Users\magom\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\root_meta_info.json"

ASSETS_DIR = r"C:\Users\magom\Downloads\twitchst\price_glitch_bot\shorts_output"

def create_capcut_draft():
    os.makedirs(PROJECT_DIR, exist_ok=True)

    # Asset paths
    s1_img = os.path.join(ASSETS_DIR, "scene1.png")
    s2_img = os.path.join(ASSETS_DIR, "scene2.png")
    s3_img = os.path.join(ASSETS_DIR, "scene3.png")
    voice_file = os.path.join(ASSETS_DIR, "ad_voiceover.mp3")
    beat_file = os.path.join(ASSETS_DIR, "bg_beat.wav")
    chime_file = os.path.join(ASSETS_DIR, "chime.wav")
    cover_file = os.path.join(PROJECT_DIR, "draft_cover.jpg")

    # Generate draft cover from scene1
    if os.path.exists(s1_img):
        from PIL import Image
        im = Image.open(s1_img)
        im.resize((540, 960)).save(cover_file, "JPEG")

    # Timing in microseconds (1 sec = 1,000,000 us)
    d1 = 3200000   # 3.2s
    d2 = 4200000   # 4.2s
    d3 = 4100000   # 4.1s
    total_duration = d1 + d2 + d3

    # Generate Unique IDs
    draft_id = str(uuid.uuid4()).upper()
    v_track_id = str(uuid.uuid4()).upper()
    a1_track_id = str(uuid.uuid4()).upper()
    a2_track_id = str(uuid.uuid4()).upper()
    a3_track_id = str(uuid.uuid4()).upper()

    mat_s1_id = str(uuid.uuid4()).upper()
    mat_s2_id = str(uuid.uuid4()).upper()
    mat_s3_id = str(uuid.uuid4()).upper()
    mat_voice_id = str(uuid.uuid4()).upper()
    mat_beat_id = str(uuid.uuid4()).upper()
    mat_chime_id = str(uuid.uuid4()).upper()

    # Materials
    materials = {
        "videos": [
            {
                "id": mat_s1_id,
                "type": "photo",
                "duration": d1,
                "path": s1_img.replace(os.sep, "/"),
                "width": 1080,
                "height": 1920
            },
            {
                "id": mat_s2_id,
                "type": "photo",
                "duration": d2,
                "path": s2_img.replace(os.sep, "/"),
                "width": 1080,
                "height": 1920
            },
            {
                "id": mat_s3_id,
                "type": "photo",
                "duration": d3,
                "path": s3_img.replace(os.sep, "/"),
                "width": 1080,
                "height": 1920
            }
        ],
        "audios": [
            {
                "id": mat_voice_id,
                "category_id": "local",
                "category_name": "local_music",
                "duration": total_duration,
                "path": voice_file.replace(os.sep, "/")
            },
            {
                "id": mat_beat_id,
                "category_id": "local",
                "category_name": "local_music",
                "duration": total_duration,
                "path": beat_file.replace(os.sep, "/")
            },
            {
                "id": mat_chime_id,
                "category_id": "local",
                "category_name": "local_music",
                "duration": 500000,
                "path": chime_file.replace(os.sep, "/")
            }
        ],
        "texts": [],
        "transitions": [],
        "speeds": [],
        "canvases": []
    }

    # Video Track Segments
    v_segments = [
        {
            "id": str(uuid.uuid4()).upper(),
            "material_id": mat_s1_id,
            "source_timerange": {"start": 0, "duration": d1},
            "target_timerange": {"start": 0, "duration": d1},
            "speed": 1.0,
            "volume": 1.0
        },
        {
            "id": str(uuid.uuid4()).upper(),
            "material_id": mat_s2_id,
            "source_timerange": {"start": 0, "duration": d2},
            "target_timerange": {"start": d1, "duration": d2},
            "speed": 1.0,
            "volume": 1.0
        },
        {
            "id": str(uuid.uuid4()).upper(),
            "material_id": mat_s3_id,
            "source_timerange": {"start": 0, "duration": d3},
            "target_timerange": {"start": d1 + d2, "duration": d3},
            "speed": 1.0,
            "volume": 1.0
        }
    ]

    # Audio Tracks
    tracks = [
        {
            "id": v_track_id,
            "type": "video",
            "segments": v_segments
        },
        {
            "id": a1_track_id,
            "type": "audio",
            "segments": [
                {
                    "id": str(uuid.uuid4()).upper(),
                    "material_id": mat_voice_id,
                    "source_timerange": {"start": 0, "duration": total_duration},
                    "target_timerange": {"start": 200000, "duration": total_duration - 200000},
                    "volume": 1.0
                }
            ]
        },
        {
            "id": a2_track_id,
            "type": "audio",
            "segments": [
                {
                    "id": str(uuid.uuid4()).upper(),
                    "material_id": mat_beat_id,
                    "source_timerange": {"start": 0, "duration": total_duration},
                    "target_timerange": {"start": 0, "duration": total_duration},
                    "volume": 0.25
                }
            ]
        },
        {
            "id": a3_track_id,
            "type": "audio",
            "segments": [
                {
                    "id": str(uuid.uuid4()).upper(),
                    "material_id": mat_chime_id,
                    "source_timerange": {"start": 0, "duration": 500000},
                    "target_timerange": {"start": 650000, "duration": 500000},
                    "volume": 0.85
                }
            ]
        }
    ]

    # Full draft_content.json
    now_us = int(time.time() * 1000000)
    draft_content = {
        "id": draft_id,
        "version": 2,
        "new_version": "164.0.0",
        "name": PROJECT_NAME,
        "duration": total_duration,
        "fps": 60.0,
        "canvas_config": {
            "ratio": "9:16",
            "width": 1080,
            "height": 1920
        },
        "tracks": tracks,
        "materials": materials,
        "create_time": now_us,
        "update_time": now_us
    }

    # Write draft_content.json
    draft_content_file = os.path.join(PROJECT_DIR, "draft_content.json")
    with open(draft_content_file, "w", encoding="utf-8") as f:
        json.dump(draft_content, f, indent=2, ensure_ascii=False)

    # Register in root_meta_info.json so CapCut displays it instantly
    if os.path.exists(ROOT_META_FILE):
        with open(ROOT_META_FILE, "r", encoding="utf-8") as f:
            root_meta = json.load(f)

        # Remove existing if already present
        root_meta["all_draft_store"] = [
            d for d in root_meta.get("all_draft_store", [])
            if d.get("draft_name") != PROJECT_NAME
        ]

        # Insert new draft at top of the list
        new_entry = {
            "draft_name": PROJECT_NAME,
            "draft_fold_path": PROJECT_DIR.replace(os.sep, "/"),
            "draft_json_file": draft_content_file.replace(os.sep, "/"),
            "draft_cover": cover_file.replace(os.sep, "/"),
            "draft_id": draft_id,
            "draft_is_ai_shorts": False,
            "draft_is_cloud_temp_draft": False,
            "draft_is_infinite_canvas_draft": False,
            "draft_is_invisible": False,
            "draft_root_path": DRAFTS_ROOT,
            "streaming_edit_draft_ready": True,
            "tm_draft_create": now_us,
            "tm_draft_modified": now_us,
            "tm_duration": total_duration
        }
        root_meta["all_draft_store"].insert(0, new_entry)

        with open(ROOT_META_FILE, "w", encoding="utf-8") as f:
            json.dump(root_meta, f, indent=2, ensure_ascii=False)

    print(f"[✔] CapCut Project Built & Registered Successfully!")
    print(f"    Project Folder: {PROJECT_DIR}")
    print(f"    You can now open CapCut to view and edit the project natively.")

if __name__ == "__main__":
    create_capcut_draft()
