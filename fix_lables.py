import os

# CHANGE THIS PATH if needed
LABELS_DIR = "PPE_DATASET/ppe_dataset/train/labels"

# OLD → NEW mapping
# OLD dataset:
# 0 = Person (REMOVE)
# 1 = boots
# 3 = goggles
# 4 = helmet
# 5 = vest

CLASS_MAP = {
    1: 2,  # boots -> boots
    3: 4,  # goggles -> goggles
    4: 0,  # helmet -> helmet
    5: 1   # vest -> vest
}

for file in os.listdir(LABELS_DIR):
    if not file.endswith(".txt"):
        continue

    path = os.path.join(LABELS_DIR, file)
    new_lines = []

    with open(path, "r") as f:
        for line in f.readlines():
            parts = line.strip().split()
            cls = int(parts[0])

            # Skip PERSON class completely
            if cls == 0:
                continue

            if cls in CLASS_MAP:
                parts[0] = str(CLASS_MAP[cls])
                new_lines.append(" ".join(parts))

    with open(path, "w") as f:
        f.write("\n".join(new_lines))

print("✅ Labels fixed successfully")
