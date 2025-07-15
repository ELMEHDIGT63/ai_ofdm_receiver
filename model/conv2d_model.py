# Conv2D Model Placeholder

def build_model(input_shape, num_bits):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Flatten, Dense

    model = Sequential([
        Conv2D(32, (3, 2), activation='relu', input_shape=input_shape),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_bits, activation='sigmoid')
    ])

    return model