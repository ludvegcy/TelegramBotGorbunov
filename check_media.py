from pathlib import Path
from src.exercises_db import EXERCISES

media_dir = Path("media")
missing = []

for key, ex in EXERCISES.items():
    photo_path = media_dir / ex["photo"]
    if not photo_path.exists():
        missing.append(f"{key}: {ex['photo']}")

if missing:
    print("❌ Отсутствуют файлы:")
    for m in missing:
        print(f"  - {m}")
else:
    print("✅ Все файлы на месте")