from pathlib import Path

train_root = Path("data/processed/Training")
test_root = Path("data/processed/Testing")

print("=" * 50)
print("TRAINING DATASET")
print("=" * 50)

total_train = 0

for cls in sorted(train_root.iterdir()):
    if cls.is_dir():
        count = len(list(cls.glob("*.*")))
        total_train += count
        print(f"{cls.name:<15} : {count}")

print("-" * 50)
print(f"Total Images    : {total_train}")

print("\n")

print("=" * 50)
print("TEST DATASET")
print("=" * 50)

total_test = 0

for cls in sorted(test_root.iterdir()):
    if cls.is_dir():
        count = len(list(cls.glob("*.*")))
        total_test += count
        print(f"{cls.name:<15} : {count}")

print("-" * 50)
print(f"Total Images    : {total_test}")