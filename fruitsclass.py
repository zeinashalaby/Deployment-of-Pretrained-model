{"metadata":{"kernelspec":{"language":"python","display_name":"Python 3","name":"python3"},"language_info":{"name":"python","version":"3.10.14","mimetype":"text/x-python","codemirror_mode":{"name":"ipython","version":3},"pygments_lexer":"ipython3","nbconvert_exporter":"python","file_extension":".py"},"kaggle":{"accelerator":"gpu","dataSources":[{"sourceId":928052,"sourceType":"datasetVersion","datasetId":500992},{"sourceId":103420,"sourceType":"modelInstanceVersion","isSourceIdPinned":true,"modelInstanceId":86686,"modelId":110937}],"isInternetEnabled":true,"language":"python","sourceType":"script","isGpuEnabled":true}},"nbformat_minor":4,"nbformat":4,"cells":[{"cell_type":"code","source":"# %% [markdown]\n# # Classify 15 Fruits with TensorFlow (acc: 99,6%)\n\n# %% [markdown]\n# <img src=\"https://i.imgur.com/GCj678V.pnghttps://i.imgur.com/GCj678V.png\" align = \"left\">\n\n# %% [markdown]\n# # Table of contents\n# \n# [<h3>1. Load and visualize the dataset</h3>](#1)\n# \n# [<h3>2. Train the neural network from scratch with Keras and w/o generator</h3>](#2)\n# \n# [<h3>3. Competition 27 pre-trained architectures - May the best win</h3>](#3)\n# \n# [<h3>4. Train the architecture with the best results</h3>](#4)\n# \n# [<h3>5. Example of predictions</h3>](#5)\n\n# %% [markdown]\n# # Data collection\n# The database used in this study is comprising of 44406 fruit images, which we collected\n# in a period of 6 months. The images where made with in our lab’s environment under different\n# scenarios which we mention below. We captured all the images on a clear background with\n# resolution of 320×258 pixels. We used HD Logitech web camera to took the pictures. During\n# collecting this database, we created all kind of challenges, which, we have to face in real-world\n# recognition scenarios in supermarket and fruit shops such as light, shadow, sunshine, pose\n# variation, to make our model robust for, it might be necessary to cope with illumination\n# variation, camera capturing artifacts, specular reflection shading and shadows. We tested our\n# model’s robustness in all scenarios and it perform quit well.\n# All of images were stored in RGB color-space at 8 bits per channel. The images were\n# gathered at various day times of the day and in different days for the same category. These\n# features increase the dataset variability and represent more realistic scenario. The Images had\n# large variation in quality and lighting. Illumination is one of those variations in imagery. In fact,\n# illumination can make two images of same fruit less similar than two images of different kind\n# of fruits. We were used our own intelligent weight machine and camera to captured all images.\n# The fruit dataset was collected under relatively unconstrained conditions. There are also images\n# with the room light on and room lights off, moved the camera and intelligent weight machine\n# near to the windows of our lab than open windows, closed windows, open window curtains,\n# closed curtains. For a real application in a supermarket, it might be necessary to cope with\n# illumination variation, camera capturing artifacts, specular reflection shading and shadows.\n# Below are the few conditions which we were considered during collected dataset.\n# - Pose Variations with different categories of fruits\n# - Variability on the number of elements of fruits\n# - Used HD camera with 5-megapixel snapshots\n# - Same color but different Category fruits images with illumination variation\n# - Cropping and partial occlusion\n# - Different color same category fruit images\n# - Different lighting conditions (e.g. fluorescent, natural light some of the fruits shops\n# - and supermarkets are without sunshine so it can easily affect the recognition system\n# - Six different kind of apple fruit images\n# - Three categories of mango fruit with specular reflecting shading and shadows\n# - Three categories of Kiwi fruit images\n# - Natural and artificial lighting effect on images\n# - Partial occlusion with hand\n# \n# \n\n# %% [markdown]\n# # 1. Load and visualize the dataset<a class=\"anchor\" id=\"1\"></a>\n# \n# The database used in this study is comprising of 70549 fruit images, which were collected in a period of 6 months. The images where made with in a lab’s environment under different scenarios which we mention below. All the images were captured on a clear background with resolution of 320×258 pixels.\n# \n# <strong><u>Type of fruits in the dataset:</u></strong>\n# - Apple\n# - Banana\n# - Carambola\n# - Guava\n# - Kiwi\n# - Mango\n# - Orange\n# - Peach\n# - Pear\n# - Persimmon\n# - Pitaya\n# - Plum\n# - Pomegranate\n# - Tomatoes\n# - muskmelon\n\n# %% [code]\n# Load the libraries\nimport pandas as pd\nimport numpy as np\nimport seaborn as sns\nimport os\nimport cv2\nimport matplotlib.pyplot as plt\nimport random\nimport time\nfrom sklearn.metrics import classification_report, confusion_matrix, accuracy_score\nfrom sklearn.model_selection import train_test_split\nimport keras\nfrom keras import Sequential\nfrom keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D\nfrom keras.utils import to_categorical\nfrom keras.callbacks import EarlyStopping, ModelCheckpoint\nimport gc\nfrom IPython.display import Markdown, display\ndef printmd(string):\n    # Print with Markdowns    \n    display(Markdown(string))\n    \nnp.random.seed(0) # Add random seed of training for reproducibility\n\ndef load_images_from_folder(folder,only_path = False, label = \"\"):\n# Load the paths to the images in a directory\n# or load the images\n    if only_path == False:\n        images = []\n        for filename in os.listdir(folder):\n            img = plt.imread(os.path.join(folder,filename))\n            if img is not None:\n                images.append(img)\n        return images\n    else:\n        path = []\n        for filename in os.listdir(folder):\n            img_path = os.path.join(folder,filename)\n            if img_path is not None:\n                path.append([label,img_path])\n        return path\n\n# %% [code]\n!kaggle datasets download -d chrisfilo/fruit-recognition -p /kaggle/working/\n\n\n# %% [code]\nimport pickle\nfrom tensorflow.keras.models import load_model\n\n# Specify the path to your .h5 model file\nmodel_path = '/kaggle/input/testmodel-fruits/tensorflow2/default/1/best_model.h5'\n\n# Load the model\nloaded_model = load_model(model_path)\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-29T17:19:02.240749Z\",\"iopub.execute_input\":\"2024-08-29T17:19:02.241138Z\",\"iopub.status.idle\":\"2024-08-29T17:19:02.250270Z\",\"shell.execute_reply.started\":\"2024-08-29T17:19:02.241100Z\",\"shell.execute_reply\":\"2024-08-29T17:19:02.248635Z\"}}\nimport streamlit as st\njupyter nbconvert --to script fruitsclass.ipynb\n# Define a function to make predictions\ndef make_prediction(input_data):\n    input_array = np.array([input_data])  # Convert input to a numpy array\n    prediction = model.predict(input_array)\n    return prediction\n\n# Streamlit UI\nst.title(\"Fruit Recognition Model\")\n\n# Create input fields\nfeature1 = st.number_input('Apple')\nfeature2 = st.number_input('Kiwi')\nfeature3 = st.number_input('Guava')\nfeature4 = st.number_input('Mango')\n\n# When the user clicks 'Predict'\nif st.button('Predict'):\n    input_data = [feature1, feature2, feature3, feature4]  # Adjust based on your model's input requirements\n    prediction = make_prediction(input_data)\n    st.write(f\"Prediction: {prediction}\")\n\n\n# %% [code] {\"execution\":{\"iopub.status.busy\":\"2024-08-28T23:55:36.465141Z\",\"iopub.execute_input\":\"2024-08-28T23:55:36.465864Z\",\"iopub.status.idle\":\"2024-08-28T23:55:36.471747Z\",\"shell.execute_reply.started\":\"2024-08-28T23:55:36.465823Z\",\"shell.execute_reply\":\"2024-08-28T23:55:36.470352Z\"}}\nstreamlit run app.py\n\n# %% [code]\n# Print the model summary to confirm it has loaded\nloaded_model.summary()\n\n# %% [code]\n# Load the paths on the images\nimages = []\ndirp = \"/kaggle/input/fruit-recognition/\"\nfor f in os.listdir(dirp):\n    if \"png\" in os.listdir(dirp+f)[0]:\n        images += load_images_from_folder(dirp+f,True,label = f)\n    else: \n        for d in os.listdir(dirp+f):\n            images += load_images_from_folder(dirp+f+\"/\"+d,True,label = f)\n            \n# Create a dataframe with the paths and the label for each fruit\ndf = pd.DataFrame(images, columns = [\"fruit\", \"path\"])\n\n# Shuffle the dataset\nfrom sklearn.utils import shuffle\ndf = shuffle(df, random_state = 0)\ndf = df.reset_index(drop=True)\n\n# Assign to each fruit a specific number\nfruit_names = sorted(df.fruit.unique())\nmapper_fruit_names = dict(zip(fruit_names, [t for t in range(len(fruit_names))]))\ndf[\"label\"] = df[\"fruit\"].map(mapper_fruit_names)\nprint(mapper_fruit_names)\n\n# Visualize the resulting dataframe\ndf.head()\n\n# %% [code]\n# Display the number of pictures of each category\nvc = df[\"fruit\"].value_counts()\nplt.figure(figsize=(10,5))\nsns.barplot(x = vc.index, y = vc, palette = \"rocket\")\nplt.title(\"Number of pictures of each category\", fontsize = 15)\nplt.xticks(rotation=90)\nplt.show()\n\n# %% [code]\n# Display some pictures of the dataset\nfig, axes = plt.subplots(nrows=4, ncols=5, figsize=(15, 15),\n                        subplot_kw={'xticks': [], 'yticks': []})\n\nfor i, ax in enumerate(axes.flat):\n    ax.imshow(plt.imread(df.path[i]))\n    ax.set_title(df.fruit[i], fontsize = 12)\nplt.tight_layout(pad=0.0)\nplt.show()\n\n# %% [markdown]\n# # 2. Train the neural network from scratch with Keras and w/o generator<a class=\"anchor\" id=\"2\"></a><a class=\"anchor\" id=\"1\"></a>\n\n# %% [code]\n# The pictures will be resized to have the same size for the neural network\nimg = plt.imread(df.path[0])\nplt.imshow(img)\nplt.title(\"Original image\")\nplt.show()\n\nplt.imshow(cv2.resize(img, (150,150)))\nplt.title(\"After resizing\")\nplt.show()\n\n# %% [markdown]\n# ## 2.1. Create and train the CNN Model<a class=\"anchor\" id=\"2\"></a>\n\n# %% [code]\ndef cut_df(df, number_of_parts, part):\n# Return a part of the dataframe\n# For example, if a dataframe has 10 rows and we want to return a part of them\n# if it is cut in two, it will return the first 5 rows or the last 5 rows depending the part wanted\n\n# Args:\n#     df (pandas.DataFrame): The dataframe to cut a part of\n#     number_of_parts (int): In how many parts should the dataframe be cut\n#     part (int): The part of the dataframe to return\n\n    if part < 1:\n        print(\"Error, the part should be at least 1\")\n    elif part > number_of_parts:\n        print(\"Error, the part cannot be higher than the number_of_parts\")\n        \n    number_imgs_each_part = int(df.shape[0]/number_of_parts)\n    idx1 = (part-1) * number_imgs_each_part\n    idx2 = part * number_imgs_each_part\n    return df.iloc[idx1:idx2]\n\ndef load_img(df):\n# Load the images using their contained in the dataframe df\n# Return a list of images and a list with the labels of the images\n    img_paths = df[\"path\"].values\n    img_labels = df[\"label\"].values\n    X = []\n    y = []\n    \n    for i,path in enumerate(img_paths):\n        img =  plt.imread(path)\n        img = cv2.resize(img, (150,150))\n        label = img_labels[i]\n        X.append(img)\n        y.append(label)\n    return np.array(X),np.array(y)\n\n# %% [code]\ndef create_model():\n    shape_img = (150,150,3)\n    \n    model = Sequential()\n\n    model.add(Conv2D(filters=32, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Conv2D(filters=64, kernel_size=(3,3),input_shape=shape_img, activation='relu', padding = 'same'))\n    model.add(MaxPooling2D(pool_size=(2, 2)))\n\n    model.add(Flatten())\n\n    model.add(Dense(256))\n    model.add(Activation('relu'))\n    model.add(Dropout(0.5))\n\n    model.add(Dense(len(mapper_fruit_names)))\n    model.add(Activation('softmax'))\n\n    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])\n    \n    return model\n\n# %% [code]\ndef from_categorical(lst):\n    \"\"\"\n    Inverse of to_categorical\n    Example: [[0,0,0,1,0], [1,0,0,0,0]] => [3,0]\n    \"\"\"\n    \n    lst = lst.tolist()\n    lst2 = []\n    for x in lst:\n        lst2.append(x.index(max(x)))\n    return lst2\n\ndef display_stats(y_test, pred):\n# Display prediction statistics\n    print(f\"### Result of the predictions using {len(y_test)} test data ###\\n\")\n    y_test_class = from_categorical(y_test)\n    print(\"Classification Report:\\n\")\n    print(classification_report(y_test_class, pred))\n    print(\"\\nConfusion Matrix:\\n\\n\")\n    print(confusion_matrix(y_test_class, pred))\n    print(\"\\n\")\n    printmd(f\"# Accuracy: {round(accuracy_score(y_test_class, pred),5)}\")\n    \ndef plot_training(model):\n    history = pd.DataFrame(model.history.history)\n    history[[\"accuracy\",\"val_accuracy\"]].plot()\n    plt.title(\"Training results\")\n    plt.xlabel(\"# epoch\")\n    plt.show()\n\n# %% [code] {\"_kg_hide-output\":true}\nmodel = create_model()\nhists = []\n\n# The model will be trained with one part of the data.\n# There isn't enough RAM on Kaggle to handle all the data.\n# In the next chapter a generator will be used\n# to \"feed\" the ANN step by step.\n# For Kaggle set divisor <= 5. 1/5 of the data will be used\ndivisor = 5\n\nstart_time = time.time()\nX_train, y_train = load_img(cut_df(df,divisor,1))\ny_train = to_categorical(y_train)\n\n# If the ANN doesn't increase its prediction accuracy on the validation data after \n# 10 epochs, stop the training and take the best of the ANN.\ncallbacks = [EarlyStopping(monitor='val_loss', patience=20),\n             ModelCheckpoint(filepath='best_model.h5', monitor='val_loss', save_best_only=True)]\n\nmodel.fit(X_train, y_train, batch_size=128, epochs=100, callbacks=callbacks, validation_split = 0.1, verbose = 1)\nhists.append(model.history.history)\n\n\n# %% [code]\n# Run the garbage collector\ngc.collect()\n\n# %% [code]\ntime_model = time.time() - start_time\nprint(f\"Time to train the model: {int(time_model)} seconds\")\n\n# %% [code]\nacc = []\nval_acc = []\nfor i in range(len(hists)):\n    acc += hists[i][\"accuracy\"]\n    val_acc += hists[i][\"val_accuracy\"]\nhist_df = pd.DataFrame({\"# Epoch\": [e for e in range(1,len(acc)+1)],\"Accuracy\": acc, \"Val_accuracy\": val_acc})\nhist_df.plot(x = \"# Epoch\", y = [\"Accuracy\",\"Val_accuracy\"])\nplt.title(\"Accuracy vs Validation Accuracy\")\nplt.show()\n\n# %% [markdown]\n# ## 2.3. Predictions<a class=\"anchor\" id=\"3\"></a>\n\n# %% [code] {\"_kg_hide-output\":false}\nimport warnings\nwarnings.filterwarnings(\"ignore\")\n\n# Make predictions with the model using the last 1/20 part of the dataset\nX, y = load_img(cut_df(df, 20, 20))\npred = model.predict_classes(X)\ny_test = to_categorical(y)\n\n# Display statistics\ndisplay_stats(y_test, pred)\n\n# %% [markdown]\n# ## 2.4. Visualize the result with pictures of fruits\n\n# %% [code]\nfig, axes = plt.subplots(nrows=4, ncols=4, figsize=(10, 10),\n                        subplot_kw={'xticks': [], 'yticks': []})\n\nfor i, ax in enumerate(axes.flat):\n    ax.imshow(X[-i])\n    ax.set_title(f\"True label: {fruit_names[y[-i]]}\\nPredicted label: {fruit_names[pred[-i]]}\")\n\nplt.tight_layout()\nplt.show()\n\n# %% [markdown]\n# <strong>The predictions are very good with around 97% accuracy using only 1/5 of the dataset to train the model.</strong>\n\n# %% [markdown]\n# # 3. Competition of 27 pre-trained architectures - May the best win<a class=\"anchor\" id=\"3\"></a><a class=\"anchor\" id=\"1\"></a>\n# *Transfer Learning, Data Generator, Data Augmentation*\n# \n# More info about the architectures under: [Module: tf.keras.applications](https://www.tensorflow.org/api_docs/python/tf/keras/applications?hl=enhttps%3A%2F%2Fwww.tensorflow.org%2Fapi_docs%2Fpython%2Ftf%2Fkeras%2Fapplications%3Fhl%3Den)\n\n# %% [code]\n# Use only 5% on the pictures to speed up the training\ntrain_df,test_df = train_test_split(df[['path','fruit']].sample(frac=0.05,random_state=0), test_size=0.2,random_state=0)\n\n# %% [code] {\"_kg_hide-output\":true}\nimport tensorflow as tf\nfrom time import perf_counter\n\ndef create_gen():\n    # Load the Images with a generator and Data Augmentation\n    train_generator = tf.keras.preprocessing.image.ImageDataGenerator(\n        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input,\n        validation_split=0.1\n    )\n\n    test_generator = tf.keras.preprocessing.image.ImageDataGenerator(\n        preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input\n    )\n\n    train_images = train_generator.flow_from_dataframe(\n        dataframe=train_df,\n        x_col='path',\n        y_col='fruit',\n        target_size=(224, 224),\n        color_mode='rgb',\n        class_mode='categorical',\n        batch_size=32,\n        shuffle=True,\n        seed=0,\n        subset='training',\n#         rotation_range=30, # Uncomment those lines to use data augmentation\n#         zoom_range=0.15,\n#         width_shift_range=0.2,\n#         height_shift_range=0.2,\n#         shear_range=0.15,\n#         horizontal_flip=True,\n#         fill_mode=\"nearest\"\n    )\n\n    val_images = train_generator.flow_from_dataframe(\n        dataframe=train_df,\n        x_col='path',\n        y_col='fruit',\n        target_size=(224, 224),\n        color_mode='rgb',\n        class_mode='categorical',\n        batch_size=32,\n        shuffle=True,\n        seed=0,\n        subset='validation',\n#         rotation_range=30, # Uncomment those lines to use data augmentation\n#         zoom_range=0.15,\n#         width_shift_range=0.2,\n#         height_shift_range=0.2,\n#         shear_range=0.15,\n#         horizontal_flip=True,\n#         fill_mode=\"nearest\"\n    )\n\n    test_images = test_generator.flow_from_dataframe(\n        dataframe=test_df,\n        x_col='path',\n        y_col='fruit',\n        target_size=(224, 224),\n        color_mode='rgb',\n        class_mode='categorical',\n        batch_size=32,\n        shuffle=False\n    )\n    \n    return train_generator,test_generator,train_images,val_images,test_images\n\ndef get_model(model):\n# Load the pretained model\n    kwargs =    {'input_shape':(224, 224, 3),\n                'include_top':False,\n                'weights':'imagenet',\n                'pooling':'avg'}\n    \n    pretrained_model = model(**kwargs)\n    pretrained_model.trainable = False\n    \n    inputs = pretrained_model.input\n\n    x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)\n    x = tf.keras.layers.Dense(128, activation='relu')(x)\n\n    outputs = tf.keras.layers.Dense(15, activation='softmax')(x)\n\n    model = tf.keras.Model(inputs=inputs, outputs=outputs)\n\n    model.compile(\n        optimizer='adam',\n        loss='categorical_crossentropy',\n        metrics=['accuracy']\n    )\n    \n    return model\n\n# Dictionary with the models\nmodels = {\n    \"DenseNet121\": {\"model\":tf.keras.applications.DenseNet121, \"perf\":0},\n    \"MobileNetV2\": {\"model\":tf.keras.applications.MobileNetV2, \"perf\":0},\n    \"DenseNet169\": {\"model\":tf.keras.applications.DenseNet169, \"perf\":0},\n    \"DenseNet201\": {\"model\":tf.keras.applications.DenseNet201, \"perf\":0},\n    \"EfficientNetB0\": {\"model\":tf.keras.applications.EfficientNetB0, \"perf\":0},\n    \"EfficientNetB1\": {\"model\":tf.keras.applications.EfficientNetB1, \"perf\":0},\n    \"EfficientNetB2\": {\"model\":tf.keras.applications.EfficientNetB2, \"perf\":0},\n    \"EfficientNetB3\": {\"model\":tf.keras.applications.EfficientNetB3, \"perf\":0},\n    \"EfficientNetB4\": {\"model\":tf.keras.applications.EfficientNetB4, \"perf\":0},\n    \"EfficientNetB5\": {\"model\":tf.keras.applications.EfficientNetB4, \"perf\":0},\n    \"EfficientNetB6\": {\"model\":tf.keras.applications.EfficientNetB4, \"perf\":0},\n    \"EfficientNetB7\": {\"model\":tf.keras.applications.EfficientNetB4, \"perf\":0},\n    \"InceptionResNetV2\": {\"model\":tf.keras.applications.InceptionResNetV2, \"perf\":0},\n    \"InceptionV3\": {\"model\":tf.keras.applications.InceptionV3, \"perf\":0},\n    \"MobileNet\": {\"model\":tf.keras.applications.MobileNet, \"perf\":0},\n    \"MobileNetV2\": {\"model\":tf.keras.applications.MobileNetV2, \"perf\":0},\n    \"MobileNetV3Large\": {\"model\":tf.keras.applications.MobileNetV3Large, \"perf\":0},\n    \"MobileNetV3Small\": {\"model\":tf.keras.applications.MobileNetV3Small, \"perf\":0},\n#     \"NASNetLarge\": {\"model\":tf.keras.applications.NASNetLarge, \"perf\":0}, Deleted because the input shape has to be another one\n    \"NASNetMobile\": {\"model\":tf.keras.applications.NASNetMobile, \"perf\":0},\n    \"ResNet101\": {\"model\":tf.keras.applications.ResNet101, \"perf\":0},\n    \"ResNet101V2\": {\"model\":tf.keras.applications.ResNet101V2, \"perf\":0},\n    \"ResNet152\": {\"model\":tf.keras.applications.ResNet152, \"perf\":0},\n    \"ResNet152V2\": {\"model\":tf.keras.applications.ResNet152V2, \"perf\":0},\n    \"ResNet50\": {\"model\":tf.keras.applications.ResNet50, \"perf\":0},\n    \"ResNet50V2\": {\"model\":tf.keras.applications.ResNet50V2, \"perf\":0},\n    \"VGG16\": {\"model\":tf.keras.applications.VGG16, \"perf\":0},\n    \"VGG19\": {\"model\":tf.keras.applications.VGG19, \"perf\":0},\n    \"Xception\": {\"model\":tf.keras.applications.Xception, \"perf\":0}\n}\n\n# Create the generators\ntrain_generator,test_generator,train_images,val_images,test_images=create_gen()\nprint('\\n')\n\n# Fit the models\nfor name, model in models.items():\n    \n    # Get the model\n    m = get_model(model['model'])\n    models[name]['model'] = m\n    \n    start = perf_counter()\n    \n    # Fit the model\n    history = m.fit(train_images,validation_data=val_images,epochs=1,verbose=0)\n    \n    # Sav the duration and the val_accuracy\n    duration = perf_counter() - start\n    duration = round(duration,2)\n    models[name]['perf'] = duration\n    print(f\"{name:20} trained in {duration} sec\")\n    \n    val_acc = history.history['val_accuracy']\n    models[name]['val_acc'] = [round(v,4) for v in val_acc]\n\n# %% [code]\nfor name, model in models.items():\n    \n    # Predict the label of the test_images\n    pred = models[name]['model'].predict(test_images)\n    pred = np.argmax(pred,axis=1)\n\n    # Map the label\n    labels = (train_images.class_indices)\n    labels = dict((v,k) for k,v in labels.items())\n    pred = [labels[k] for k in pred]\n\n    y_test = list(test_df.fruit)\n    acc = accuracy_score(y_test,pred)\n    models[name]['acc'] = round(acc,4)\n#     printmd(f'**{name} has a {acc * 100:.2f}% accuracy on the test set**')\n\n# %% [code] {\"_kg_hide-output\":true}\n# Create a DataFrame with the results\nmodels_result = []\n\nfor name, v in models.items():\n    models_result.append([ name, models[name]['val_acc'][-1], \n                          models[name]['acc'],\n                          models[name]['perf']])\n    \ndf_results = pd.DataFrame(models_result, \n                          columns = ['model','val_accuracy','accuracy','Training time (sec)'])\ndf_results.sort_values(by='accuracy', ascending=False, inplace=True)\ndf_results.reset_index(inplace=True,drop=True)\ndf_results\n\n# %% [code]\nplt.figure(figsize = (15,5))\nsns.barplot(x = 'model', y = 'accuracy', data = df_results)\nplt.title('Accuracy on the test set (after 1 epoch))', fontsize = 15)\nplt.ylim(0,1)\nplt.xticks(rotation=90)\nplt.show()\n\n# %% [code]\nplt.figure(figsize = (15,5))\nsns.barplot(x = 'model', y = 'Training time (sec)', data = df_results)\nplt.title('Training time for each model in sec', fontsize = 15)\n# plt.ylim(0,20)\nplt.xticks(rotation=90)\nplt.show()\n\n# %% [markdown]\n# # 4. Train the architecture with the best results<a class=\"anchor\" id=\"4\"></a>\n\n# %% [code]\n# Split into train/test datasets using all of the pictures\ntrain_df,test_df = train_test_split(df, test_size=0.1, random_state=0)\n\n# Create the generator\ntrain_generator,test_generator,train_images,val_images,test_images=create_gen()\n\n# %% [code] {\"_kg_hide-output\":false}\n# Create and train the model\nmodel = get_model(tf.keras.applications.DenseNet201)\nhistory = model.fit(train_images,\n                    validation_data=val_images,\n                    epochs=5,\n                    callbacks=[\n                        tf.keras.callbacks.EarlyStopping(\n                            monitor='val_loss',\n                            patience=1,\n                            restore_best_weights=True)]\n                    )\n\n# %% [code]\npd.DataFrame(history.history)[['accuracy','val_accuracy']].plot()\nplt.title(\"Accuracy\")\nplt.show()\n\n# %% [code]\npd.DataFrame(history.history)[['loss','val_loss']].plot()\nplt.title(\"Loss\")\nplt.show()\n\n# %% [code]\n# Predict the label of the test_images\npred = model.predict(test_images)\npred = np.argmax(pred,axis=1)\n\n# Map the label\nlabels = (train_images.class_indices)\nlabels = dict((v,k) for k,v in labels.items())\npred = [labels[k] for k in pred]\n\n# Get the accuracy on the test set\ny_test = list(test_df.fruit)\nacc = accuracy_score(y_test,pred)\nprintmd(f'# Accuracy on the test set: {acc * 100:.2f}%')\n\n# %% [code]\n# Display a confusion matrix\nfrom sklearn.metrics import confusion_matrix\ncf_matrix = confusion_matrix(y_test, pred, normalize='true')\nplt.figure(figsize = (10,7))\nsns.heatmap(cf_matrix, annot=False, xticklabels = sorted(set(y_test)), yticklabels = sorted(set(y_test)),cbar=False)\nplt.title('Normalized Confusion Matrix', fontsize = 23)\nplt.xticks(fontsize=15)\nplt.yticks(fontsize=15)\nplt.show()\n\n# %% [markdown]\n# # 5. Example of prediction<a class=\"anchor\" id=\"5\"></a>\n\n# %% [code]\n# Display picture of the dataset with their labels\nfig, axes = plt.subplots(nrows=4, ncols=6, figsize=(20, 12),\n                        subplot_kw={'xticks': [], 'yticks': []})\n\nfor i, ax in enumerate(axes.flat):\n    ax.imshow(plt.imread(test_df.path.iloc[i]))\n    ax.set_title(f\"True: {test_df.fruit.iloc[i].split('_')[0]}\\nPredicted: {pred[i].split('_')[0]}\", fontsize = 15)\nplt.tight_layout()\nplt.show()","metadata":{"_uuid":"9cd40697-7cd6-429a-86ac-3fc39fdf05cd","_cell_guid":"e1e925b9-2735-44a0-9ad2-70615087c109","collapsed":false,"jupyter":{"outputs_hidden":false},"trusted":true},"execution_count":null,"outputs":[]}]}