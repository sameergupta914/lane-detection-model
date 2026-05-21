# System Diagram

## High-Level System Architecture

```mermaid
flowchart LR
    U[User] --> F[React Frontend]

    subgraph Frontend[Frontend Layer]
        F1[Upload Road Image]
        F2[Preview Selected Image]
        F3[Send Image to API]
        F4[Display Model Output]
        F5[Display Lane Overlay]
        F --> F1 --> F2 --> F3 --> F4
        F4 --> F5
    end

    F3 --> B

    subgraph Backend[FastAPI Backend Layer]
        B[FastAPI API]
        B1[Validate Uploaded File]
        B2[Load Trained Model]
        B3[Preprocess Image]
        B4[Run Inference]
        B5[Generate Mask]
        B6[Generate Masked Original]
        B7[Generate Lane Overlay]
        B8[Save Output Images]
        B --> B1 --> B2 --> B3 --> B4 --> B5
        B5 --> B6
        B6 --> B7
        B7 --> B8
    end

    B2 --> M[(best_model.keras)]

    B8 --> O[(backend/outputs)]
    O --> R[API Response with Output URLs]

    R --> F4
    F5 --> U
```

---

## Detailed Data Flow

```mermaid
sequenceDiagram
    participant User
    participant React as React Frontend
    participant API as FastAPI Backend
    participant Model as Trained Model
    participant Storage as Output Storage

    User->>React: Select road image
    React->>React: Preview image locally
    User->>React: Click Detect Lanes
    React->>API: POST /api/predict with image
    API->>API: Validate file type and size
    API->>API: Decode and preprocess image
    API->>Model: Run prediction
    Model-->>API: Predicted lane mask
    API->>API: Postprocess mask
    API->>API: Create masked original image
    API->>API: Create lane overlay image
    API->>Storage: Save output PNG files
    Storage-->>API: File paths / names
    API-->>React: JSON response with output URLs
    React->>React: Render model output and overlay
    React-->>User: Show final lane detection results
```

---

## Component Explanation

### 1. User

The user interacts with the system through the browser by:

- uploading a road image
- previewing the selected image
- requesting lane detection
- viewing the final results

### 2. React Frontend

The frontend is responsible for:

- file selection and upload
- image preview before inference
- showing loading and error states
- displaying final result images returned by the backend

Visible frontend outputs:

- model output
- lane overlay

### 3. FastAPI Backend

The backend is responsible for:

- receiving the uploaded image
- validating file type and size
- loading the trained segmentation model
- preprocessing the image to the model input size
- running inference
- converting the raw model prediction into visual outputs

### 4. Trained Model

The trained model file:

- `best_model.keras`

This model performs lane-region segmentation on the uploaded road image.

### 5. Output Storage

Generated result images are written to:

- `backend/outputs/`

These files are then served back to the frontend as static URLs.

---

## Functional Summary

The system works in the following order:

1. The user uploads a road image in the React frontend.
2. The frontend sends the image to the FastAPI backend.
3. The backend preprocesses the image and runs inference using `best_model.keras`.
4. The backend generates:
   - lane mask
   - masked original image
   - lane overlay
5. The backend stores the generated outputs and returns their URLs.
6. The frontend shows the processed outputs to the user.

---

## Short Description for Report Use

This project follows a client-server architecture. The React frontend handles user interaction, image upload, and result presentation. The FastAPI backend handles model loading, preprocessing, inference, postprocessing, and output generation. The trained lane-segmentation model predicts lane regions from uploaded road images, and the backend converts the prediction into visually interpretable outputs such as masked lane-region images and lane overlays. These outputs are returned to the frontend and presented to the user through a browser interface.
