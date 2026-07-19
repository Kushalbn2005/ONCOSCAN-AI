from ml.dataset import DatasetLoader
import matplotlib.pyplot as plt

# Load dataset
loader = DatasetLoader(
    train_dir="data/processed/Training",
    test_dir="data/processed/Testing",
    batch_size=32,
    image_size=(224, 224)
)

train_ds, val_ds, test_ds = loader.load()

# Get one batch
images, labels = next(iter(train_ds))

# Plot images
plt.figure(figsize=(10, 10))

for i in range(9):
    plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy())  # Convert TensorFlow tensor to NumPy
    plt.title(loader.class_names[labels[i].numpy()])
    plt.axis("off")

plt.tight_layout()
plt.show()