from ml.dataset import DatasetLoader

loader = DatasetLoader(

    train_dir="data/processed/Training",

    test_dir="data/processed/Testing",

    batch_size=32,

    image_size=(224,224)

)

train_ds, val_ds, test_ds = loader.load()
