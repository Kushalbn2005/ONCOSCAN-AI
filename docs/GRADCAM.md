# Grad-CAM and heatmaps

Explainability lives in `ml/gradcam.py`. The classifier wraps EfficientNetB0 as a nested Functional model, so Grad-CAM cannot call `self.model.get_layer("top_conv")` on the outer graph.

## Why the nested graph matters

Outer layers typically look like:

```
input_layer_*
efficientnetb0          # nested Model — last conv is top_conv here
global_average_pooling2d
batch_normalization
dropout
dense
dropout_1
dense_1
```

Correct construction:

1. Take the nested backbone (`_get_backbone()`).
2. Build a model: `backbone.input` → `[top_conv.output, backbone.output]`.
3. Run the **outer head** (`model.layers[2:]`) on `backbone.output` so the class score stays connected to the conv maps.
4. `GradientTape` differentiates `predictions[:, class_index]` w.r.t. `top_conv` activations.
5. Channel-wise mean of gradients weights the maps; ReLU + normalize → heatmap.
6. Resize, JET colormap, blend with the original BGR MRI.

`keras.Model(inputs=outer.inputs, outputs=inner_conv.output)` raises `Output with path 0 is not connected to inputs`.

## CLI

`GradCAM` now takes a loaded `Predictor`, not a raw path:

```python
from ml.predict import Predictor
from ml.gradcam import GradCAM

predictor = Predictor("artifacts/models/best_model.keras")
gradcam = GradCAM(predictor)
result = gradcam.run("data/raw/Testing/notumor/Te-no_25.jpg")
```

```bash
python run_gradcam.py
python run_predict.py
```

`run()` saves a three-panel image (original | heatmap | overlay) under `artifacts/gradcam/`.

## API modes

`backend/routes/predict.py` chooses a generator from `get_heatmap_mode()`:

| Mode | Method | Use |
|------|--------|-----|
| `full` | `GradCAM.generate` | True Grad-CAM. Higher RAM. Default on a local machine. |
| `light` | `GradCAM.generate_light` | Mean last-conv activation (no `GradientTape`). Default on Render free tier. |
| `off` | skipped | Class probabilities only. |

Both generators return a filename; the API exposes `/static/gradcam/<filename>`.

Light mode is **not** class-specific Grad-CAM. It shows where the last conv layer fires strongly, which is usually enough for a UI overlay when memory is tight.

## Reading the overlay

Warm colors (red/yellow) are regions that most increased the predicted class score (full mode). Use overlay / split / raw / heatmap views in the Scan Studio. Treat heatmaps as a debugging aid, not proof of tumor location.
