from ml.train import Trainer

trainer = Trainer(

    train_dir="data/processed/Training",

    test_dir="data/processed/Testing",

    epochs=20,

    batch_size=32

)

history = trainer.train()