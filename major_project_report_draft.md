# Major Project Report Draft

## Title

**Lane Detection and Lane Region Visualization for Road Scenes Using Deep Learning**

---

## Abstract

Lane detection is a core perception task in intelligent transportation systems, advanced driver assistance systems, and autonomous vehicles. Reliable detection of lane markings helps estimate lane boundaries, maintain road alignment, and support safe navigation. This project presents a deep-learning-based lane detection system using the TuSimple Lane Detection dataset. The problem is formulated as a binary semantic segmentation task in which annotated lane points are converted into dense pixel-level masks. A VGG16-UNet architecture is trained to detect lane regions from road images after preprocessing, frame extraction, and mask generation. The model is optimized using Dice loss and evaluated using Dice coefficient, precision, recall, and accuracy. The current system achieves moderate validation performance, with validation Dice reaching approximately 0.62 and validation precision exceeding 0.76 in the saved experiment. To improve interpretability and practical usability, the trained model is deployed through a FastAPI backend and a React-based frontend that allows users to upload a road image and visualize lane-focused output. The project demonstrates a complete pipeline from dataset preparation to deployable inference and provides a solid baseline for future work in real-time lane detection and intelligent driving assistance.

**Keywords:** lane detection, semantic segmentation, TuSimple, VGG16, U-Net, computer vision, autonomous driving, deep learning

---

# Chapter 1: Introduction

## 1.1 Background

Modern transportation systems increasingly depend on intelligent perception modules to support driver assistance and autonomous navigation. Among these perception modules, lane detection is one of the most essential tasks because lane markings define the road structure and guide vehicle motion. Accurate lane detection enables applications such as lane keeping, lane departure warning, road alignment estimation, and drivable region analysis.

Traditional lane detection approaches relied on handcrafted image-processing methods such as edge detection, color thresholding, and Hough transforms. Although such approaches can work in controlled environments, they often fail under varying illumination, shadows, occlusion, road curvature, and degraded lane markings. Deep learning provides a more robust alternative by learning semantic and structural features directly from data.

This project focuses on developing a deep-learning-based lane detection system that identifies lane regions from road images and presents the output through an interactive frontend. The work combines data preprocessing, segmentation-model training, evaluation, and deployment.

## 1.2 Problem Statement

Lane markings are often difficult to detect reliably because road scenes contain dynamic lighting, perspective distortion, shadows, vehicles, and environmental clutter. A system is required that can learn robust visual patterns of lane markings and generate a useful lane-region output from road images.

The problem addressed in this project is:

**How can a deep learning model be trained on TuSimple lane data to detect lane regions effectively and present the results through an interpretable user-facing system?**

## 1.3 Aim

To design and implement a deep-learning-based lane detection system that performs lane-region segmentation from road images and provides deployment-ready visual output through a web interface.

## 1.4 Objectives

The main objectives of this project are:

1. To study the lane detection problem in road scenes.
2. To preprocess the TuSimple dataset into image-mask pairs suitable for segmentation.
3. To build a VGG16-UNet model for binary lane segmentation.
4. To train the model and evaluate it using segmentation-relevant metrics.
5. To deploy the trained model through a FastAPI backend and React frontend.
6. To present the predicted lane region in a visually interpretable form.

## 1.5 Scope

This project focuses on:

- image-based lane detection
- binary lane-region segmentation
- deep learning model training on TuSimple data
- inference on static road images
- frontend-based result visualization

This project does not yet include:

- real-time video inference
- temporal modeling across frame sequences
- lane instance separation
- embedded deployment
- full benchmark submission formatting for TuSimple evaluation

## 1.6 Significance of the Study

This work is significant because it demonstrates an end-to-end intelligent perception pipeline using a standard lane detection dataset and deploys the trained model in a practical interface. It is relevant for academic study in:

- computer vision
- machine learning
- autonomous driving
- driver assistance systems
- intelligent transportation

---

# Chapter 2: Literature Review

## 2.1 Overview of Lane Detection

Lane detection is the process of identifying lane boundaries or lane regions from road images or video frames. It is a key component in ADAS and autonomous driving perception stacks.

Broadly, lane detection methods can be divided into:

1. traditional vision-based methods
2. learning-based methods
3. deep-learning-based methods

## 2.2 Traditional Methods

Earlier approaches used:

- grayscale conversion
- edge detection
- region-of-interest selection
- Hough transform
- polynomial curve fitting
- color thresholding

These methods are computationally simple, but their performance is sensitive to:

- lighting variation
- shadows
- lane fading
- noise
- road texture

## 2.3 Machine Learning and Deep Learning Approaches

Learning-based approaches improved lane detection by using learned features rather than fixed handcrafted rules. Deep learning models, especially convolutional neural networks, have become the dominant choice due to their ability to model complex visual structures.

Deep-learning lane detection methods commonly follow one of these strategies:

- semantic segmentation
- instance segmentation
- row-wise classification
- parametric lane fitting

## 2.4 Segmentation-Based Lane Detection

Semantic segmentation models predict a pixel-wise class label for every pixel in the image. This is appropriate for lane detection because the task naturally contains strong spatial structure.

Benefits of segmentation-based lane detection include:

- dense spatial prediction
- easier visual interpretation
- suitability for encoder-decoder architectures
- direct compatibility with overlay-based display

## 2.5 U-Net and Encoder-Decoder Networks

U-Net is a popular segmentation architecture originally designed for biomedical segmentation. It uses:

- an encoder to capture semantic features
- a decoder to recover spatial resolution
- skip connections to preserve fine details

This makes U-Net well suited for lane detection, where thin and elongated structures must be localized accurately.

## 2.6 VGG16 as a Backbone

VGG16 is a widely used convolutional network that can act as a strong feature extractor. When used as an encoder inside a U-Net-like architecture, it benefits from:

- pretrained ImageNet features
- stable layer organization
- effective hierarchical feature extraction

However, it is heavier than newer backbones and may not be optimal for real-time deployment.

## 2.7 Gap Addressed by This Project

This project focuses not only on segmentation model training but also on practical usability. It bridges:

- benchmark dataset preprocessing
- deep-learning segmentation
- deployable image-based inference
- user-facing visualization

Thus, the work is both technically and practically relevant.

---

# Chapter 3: Dataset and Data Preparation

## 3.1 Dataset Used

The project uses the **TuSimple Lane Detection Challenge Dataset**.

The dataset contains forward-facing road scenes in video-clip form. The final frame of each clip is annotated with lane information.

## 3.2 Training Data

According to the dataset documentation:

- number of training clips: **3626**
- number of labeled training frames: **3626**
- frames per clip: **20**

The local training dataset contains:

- `train_set/clips/`
- `train_set/label_data_0313.json`
- `train_set/label_data_0531.json`
- `train_set/label_data_0601.json`

## 3.3 Test Data

The test dataset contains:

- number of test clips: **2782**
- `test_set/clips/`
- `test_set/test_tasks_0627.json`

## 3.4 Annotation Format

Each training sample contains:

- `raw_file`: file path of the clip frame
- `lanes`: x-coordinates of lane points
- `h_samples`: y-coordinates corresponding to each lane point

The annotation uses `-2` for missing lane points.

## 3.5 Data Extraction

The project extracts only the `20.jpg` frame from every clip because this is the annotated frame in TuSimple.

The extraction pipeline:

1. iterates over clip groups inside `train_set/clips/`
2. locates `20.jpg` in each clip folder
3. copies the image into a processed directory
4. renames the image using:
   - `<clip_group>_<clip_id>.jpg`

This creates a flat training-image structure aligned with the annotations.

## 3.6 Mask Generation

The TuSimple annotations are sparse lane points rather than dense segmentation masks. Therefore, the project converts them into binary masks.

Mask generation process:

1. create a blank mask of size `720 x 1280`
2. read lane x-coordinates and vertical samples
3. remove invalid `-2` points
4. form lane-point polylines
5. draw each lane using `cv2.polylines()`

Current mask thickness:

- **15 pixels**

This creates thicker lane regions that are easier for a segmentation model to learn.

## 3.7 Train-Test Split

After image and mask generation:

- images and masks are split with `train_test_split`
- `test_size = 0.1`
- `random_state = 42`

This produces:

- 90% training data
- 10% testing data

## 3.8 Research Discussion

The preprocessing pipeline transforms TuSimple from a lane-point detection dataset into a binary segmentation dataset. This is an important methodological decision because it makes the problem suitable for U-Net-style training, but it also changes the evaluation emphasis from geometric lane estimation to region overlap quality.

---

# Chapter 4: Proposed Methodology

## 4.1 Problem Formulation

This project formulates lane detection as a **binary semantic segmentation problem**.

Given an input image of size `224 x 224 x 3`, the model predicts a binary lane mask of size `224 x 224 x 1`.

## 4.2 Input Processing

The input preprocessing pipeline includes:

- reading the image from disk
- JPEG decoding
- resizing to `224 x 224`
- normalization to `[0, 1]`

Ground-truth masks are:

- read from disk
- decoded as grayscale
- resized using nearest-neighbor interpolation
- normalized to `[0, 1]`

## 4.3 Model Architecture

The project uses a **VGG16-UNet** architecture.

### Encoder

The encoder is based on:

- `VGG16(weights='imagenet', include_top=False)`

All layers are trainable.

### Decoder

The decoder:

- upsamples feature maps
- concatenates them with encoder skip connections
- applies convolution, batch normalization, and dropout

### Output

The final layer is:

- `Conv2D(1, (1,1), activation='sigmoid')`

This produces a probability map for lane pixels.

## 4.4 Loss Function

The model is trained using **Dice loss**:

```text
Dice Loss = 1 - Dice Coefficient
```

Dice loss is appropriate because lane pixels occupy a relatively small fraction of the image.

## 4.5 Evaluation Metrics

The model uses:

- Dice coefficient
- smoothed precision
- smoothed recall
- accuracy

Dice coefficient is the most meaningful segmentation-quality measure in this project.

## 4.6 Training Pipeline

The TensorFlow pipeline uses:

- `cache()`
- `shuffle()`
- `repeat()`
- `batch()`
- `prefetch()`

Current configuration:

- `BATCH_SIZE = 32`
- `BUFFER_SIZE = 1000`

Reduced-step schedule:

- `EPOCHS = 10`
- `MAX_STEPS_PER_EPOCH = 10`
- `MAX_VALIDATION_STEPS = 10`

This configuration was adopted due to training-time constraints on local hardware.

## 4.7 Model Saving and Best Checkpoint

The project uses:

- `ModelCheckpoint('best_model.keras', save_best_only=True)`

This ensures that the best validation-loss model is retained.

---

# Chapter 5: Experimental Setup and Results

## 5.1 Environment

The project was developed in a local environment with:

- Python
- TensorFlow
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Scikit-learn

The saved trained model file is:

- `best_model.keras`

## 5.2 Training Behavior

The model was trained using a reduced number of steps per epoch:

- `10` steps per epoch
- batch size `32`

Thus, only about `320` training images are used per epoch, even though the training dataset is much larger.

This makes training feasible, but less stable than full-dataset training.

## 5.3 Selected Results

In the saved experiment output, the final epoch achieved approximately:

- train Dice: `0.6228`
- train precision: `0.5255`
- train recall: `0.7649`
- validation Dice: `0.6223`
- validation precision: `0.7667`
- validation recall: `0.5247`
- validation accuracy: `0.9733`

## 5.4 Result Interpretation

These values suggest:

1. The model is reasonably precise in validation predictions.
2. The model still misses some true lane regions.
3. Dice score is moderate, indicating useful but improvable overlap.
4. Accuracy is high due to large background area and should not be treated as the primary success metric.

## 5.5 Visual Output

The inference outputs include:

- lane mask
- masked original image
- lane overlay

For presentation purposes, the masked original image and overlay provide better interpretability than a raw binary mask.

## 5.6 Discussion

The results are sufficient to demonstrate a functioning segmentation-based lane detection baseline. However, they do not yet support very strong claims of high robustness or production readiness. The project is best presented as:

- an end-to-end major-project prototype
- a research baseline
- a deployable academic demonstration

---

# Chapter 6: Deployment and User Interface

## 6.1 Deployment Objective

A major project should not stop at model training. Therefore, this project includes a deployment-oriented system that allows a user to test the model on uploaded road images.

## 6.2 Backend

The backend is built using **FastAPI**.

Its responsibilities are:

- loading `best_model.keras`
- preprocessing uploaded images
- running inference
- producing output files
- returning URLs for result visualization

Key endpoints:

- `GET /health`
- `POST /api/predict`

## 6.3 Frontend

The frontend is built using **React**.

Its features include:

- upload road image
- local image preview
- send image to backend
- display model output
- display lane overlay

## 6.4 Output Presentation

The final frontend was intentionally simplified for demonstration. The visible result cards emphasize:

- **Model Output**: masked original image
- **Lane Overlay**: predicted lane region blended onto the original image

This design makes the project easier to demonstrate to faculty and evaluators.

## 6.5 Importance in a Major Project

This deployment layer adds significant value because it proves:

- practical applicability
- user-facing inference support
- system integration ability
- full-pipeline ownership

---

# Chapter 7: Limitations and Future Work

## 7.1 Current Limitations

The current system has the following limitations:

1. It uses only static-image inference.
2. It does not use temporal information from video clips.
3. It predicts lane regions, not lane instances or fitted lane curves.
4. It uses a reduced-step training regime for computational convenience.
5. It does not yet use data augmentation extensively.
6. It is not benchmarked for real-time deployment.
7. It does not explicitly handle severe weather or nighttime scenarios.

## 7.2 Future Work

The project can be significantly improved by:

1. increasing training rigor
2. using more epochs or more effective dataset coverage
3. applying stronger augmentation
4. testing lighter or stronger encoders
5. extending inference to video
6. converting masks to parametric lane geometry
7. adding real-time performance analysis
8. comparing multiple architectures experimentally

## 7.3 Strong Future Research Directions

Possible advanced extensions:

- temporal lane tracking with sequence models
- transformer-based segmentation
- attention-augmented U-Net
- lane instance segmentation
- real-time ADAS pipeline integration

---

# Chapter 8: Conclusion

This project presented a deep-learning-based lane detection system using the TuSimple dataset and a VGG16-UNet segmentation architecture. The work transformed sparse lane-point annotations into trainable binary masks, trained a segmentation model using Dice loss, evaluated the system using standard segmentation metrics, and deployed the trained model through a FastAPI and React application.

The current model demonstrates moderate segmentation performance and produces visually meaningful lane outputs. While the system is not yet optimized for state-of-the-art performance or real-time deployment, it serves as a complete and valid major-project implementation. It combines research relevance, practical system design, and deployable inference into a coherent end-to-end solution.

The project can therefore be considered a strong academic prototype and a solid foundation for future research in intelligent transportation and road-scene perception.

---

# References Draft Pointers

You should later add proper formatted references for:

1. TuSimple Lane Detection Challenge dataset
2. U-Net paper
3. VGG16 paper
4. deep-learning lane detection survey papers
5. semantic segmentation papers

Suggested types of papers to cite:

- original U-Net paper
- original VGG paper
- lane detection survey/review papers
- TuSimple benchmark-related works
- semantic segmentation methodology papers

---

# Appendix A: Current Project Files

Main research/training files:

- `lanenet_model_mp.ipynb`
- `best_model.keras`
- `train_set/`
- `test_set/`

Deployment files:

- `backend/`
- `frontend/`

Documentation files:

- `research.md`
- `project_brain.md`
- `README.md`

---

# Appendix B: Recommended Viva Summary

If asked to summarize the project in one paragraph:

This project develops a lane detection system for road scenes using a segmentation-based deep learning approach. The TuSimple dataset is preprocessed by extracting labeled road frames and generating binary lane masks from sparse lane annotations. A VGG16-UNet model is trained using Dice loss to detect lane regions. The trained model is then deployed through a FastAPI backend and React frontend, allowing users to upload road images and visualize lane-focused results such as masked road regions and lane overlays. The work demonstrates a complete pipeline from data preparation to practical inference and forms a strong baseline for further research in intelligent driving assistance.
