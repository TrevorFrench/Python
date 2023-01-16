from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from keras import layers
from keras.models import Sequential

import os
from os.path import join


# helicopter_dir = '../selected/helicopter'

# helicopter_paths = [join(helicopter_dir,filename) for filename in 
#                             ['helicopter1.jpg',
#                              'helicopter2.jpg']]

# jet_plane_dir = '../selected/jet_plane'
# jet_plane_paths = [join(jet_plane_dir, filename) for filename in
#                             ['jet_plane1.jpg',
#                              'jet_plane2.jpg']]

# img_paths = helicopter_paths + jet_plane_paths

# import pathlib
data_dir = "selected"
#data_dir = tf.keras.utils.get_file('hotdog', origin=dataset_url, untar=True)
#data_dir = pathlib.Path(data_dir)

import glob
image_list = []
for filename in glob.glob("selected/*/*.jpg"):
        im=PIL.Image.open(filename)
        image_list.append(im)

image_count= len(image_list)
print(image_count)

# helicopter = []
# for filename in glob.glob("selected/helicopter/*.jpg"):
#     im=PIL.Image.open(filename)
#     helicopter.append(im)

# jet_plane = []
# for filename in glob.glob("selected/jet_plane/*.jpg"):
#     im=PIL.Image.open(filename)
#     jet_plane.append(im)

batch_size = 32
img_height = 180
img_width = 180
# FIRST SEED 123
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=0,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=0,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

num_classes = len(class_names)

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs=13
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

# %%
plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
# %%

url_list = [
    "https://storage.googleapis.com/kagglesdsdata/datasets/8552/57440/test/hot_dog/146834.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20220417%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220417T232130Z&X-Goog-Expires=345599&X-Goog-SignedHeaders=host&X-Goog-Signature=4337ab84d4495402f773fc9225ed2a289b2973edccbccdf88711a049ccea6e10d507b435be59bdcbc009cb07661fccdafd4a898acfba1cf770373135293d966369ef82e3fe3f7849317ba373d8f295b47234cd8e456ad4b264986c6a28adffa2dca03252a63b06974c11de391bdf6d1612facadb2b3083ded332035e06d03a2b0d0fd2b628f97a782566c7211ed1fb72e419d5cecfe4205ff2ce2ce7a8817a3a8cf4cea19a9751a0100a006cad17fa6ff48eaa4c75e819b5787878b8d9c0be0d8cfc33b5bee95be948d4c8d32ccd1bbd9da9508d0540dbfc2b6903a1479ab4610e2094100cf8305912c2255e27095448d0466c59b6b28e45c06a125df5816db5"
    , "https://storage.googleapis.com/kagglesdsdata/datasets/8552/57440/test/hot_dog/165005.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20220417%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220417T232131Z&X-Goog-Expires=345599&X-Goog-SignedHeaders=host&X-Goog-Signature=98f2f92437e6e689f694d6a75f1e8beb43514df028e64174f9b3306e638dedefc00b8295ca1afae400397ea834df67d959b3030cad5d58609d1e784461419b5bd98d8f56a052431d76a81fa3b16de6a9cfbc6912c6785d57e61f5d211048911b3ccce41199a717103c388196cb2e8ea67a20115b23c91127816ae48fc2c4dbc023f205caa923330fddceac65fa06f6e9c29ffe9ba5dac434efcb7a9be51ea1933e430d935efad9a3d49ab53452d9683a00ff0558efef4567c1d3490db08ea8f62f6fba4dbf74fa00799c47b4a945b744e7e51125aa95ab670475e6471bf1ec5e118402d6fd627f63ff30f4b8882e3d671cbf0a5477adbe163c27559fa8f99ac5"
    , "https://storage.googleapis.com/kagglesdsdata/datasets/8552/57440/test/not_hot_dog/13023.jpg?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20220418%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20220418T000129Z&X-Goog-Expires=345599&X-Goog-SignedHeaders=host&X-Goog-Signature=698a08260c34061f2853f598d1c38693bb768c03d339446db4f705122d61d32267ce92b36627cca4bbf427752b7751ed7d13773eb3d21526e0b99c702cf9f59da2362074960d0183fefa1ce65677fee298c6840b4c92afeb71796b71d04e30ecf0f8b95605ad2781797078f91790226a4c5e120429aa758bb3961d4f30f7f19911e20238c7fb9c32d60144080d3bcc5ad6dd6887a3eedf93022dce44b8d866222f28aec099dff5cd2873c59d13f4d3e1b82b8f0ca77c15049ca151d4368fa6cede3ccbdb72ccb145f0fee8967d77954abe65a55f09b5d52d0b2c74dac7b5b81781e942f8fc6c9a27eee40400f1cae8f88b681ee363ec5095f7a30ebdf3c1917a"
    , "https://imageio.forbes.com/specials-images/imageserve/5f47d4de7637290765bce495/0x0.jpg?format=jpg&crop=2146,2145,x1699,y559,safe&height=416&width=416&fit=bounds"
]

url_list_2 =["https://www.tacobueno.com/assets/food/tacos/Taco_Crispy_Beef_990x725.jpg"]
import webbrowser

# i = 0
for image in url_list_2:
    print(image)
    path = tf.keras.utils.get_file(origin=image)

    webbrowser.open(image)

    img = tf.keras.utils.load_img(
        path, target_size=(img_height, img_width)
    )

    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

    print(class_names[np.argmax(score)])
    # i+=1
    sleep(5)
