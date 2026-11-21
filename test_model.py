import tensorflow as tf

MODEL_PATH = "ai/models/isl_alphabet.keras"
CLASS_NAMES_PATH = "ai/models/class_names.txt"

print("Loading model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]

print("Model loaded successfully")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)
print("Classes:", class_names)
print("Number of classes:", len(class_names))