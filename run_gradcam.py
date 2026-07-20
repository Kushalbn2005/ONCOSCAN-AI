from ml.gradcam import GradCAM

gradcam = GradCAM(

    model_path="artifacts/models/best_model.keras"

)

original, image = gradcam.load_image(

    "data/processed/Testing/pituitary/Te-pi_4.jpg"          # replace with an MRI image

)

class_index, class_name, confidence = gradcam.predict(

    image

)

last_conv = gradcam.get_last_conv_layer()

heatmap = gradcam.make_heatmap(

    image,

    class_index,

    last_conv

)

print()

print("Heatmap Shape :", heatmap.shape)

print("Minimum Value :", heatmap.min())

print("Maximum Value :", heatmap.max())