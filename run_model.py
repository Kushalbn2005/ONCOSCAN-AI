from ml.model import BrainTumorClassifier

builder = BrainTumorClassifier()

model = builder.build()

model.summary()