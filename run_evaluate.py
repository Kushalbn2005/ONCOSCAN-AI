from ml.evaluate import Evaluator

evaluator = Evaluator(

    model_path="artifacts/models/best_model.keras",

    train_dir="data/processed/Training",

    test_dir="data/processed/Testing",

    batch_size=32,

    image_size=(224, 224)

)

evaluator.run()