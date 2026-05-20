# Project Brain

## Project Overview

This project is a TuSimple lane detection training pipeline built primarily in the notebook `lanenet_model_mp.ipynb`.

The workflow in the notebook is:

1. Install/import the ML stack.
2. Read the TuSimple training dataset from `train_set`.
3. Extract the last frame (`20.jpg`) from each training clip into a processed image folder.
4. Read lane annotations from the TuSimple JSON label files.
5. Generate binary lane masks for each extracted image.
6. Split processed images and masks into train/test folders.
7. Build TensorFlow datasets from those folders.
8. Train a segmentation model based on `VGG16`.
9. Save/load `best_model.keras`.
10. Run prediction on a sample image and display the predicted mask.

## Repository Structure

Relevant top-level items:

- `lanenet_model_mp.ipynb`
- `requirements.txt`
- `test_label.json`
- `train_set/`
- `test_set/`

Dataset notes:

- `train_set/`
  - `clips/`
  - `seg_label/`
  - `label_data_0313.json`
  - `label_data_0531.json`
  - `label_data_0601.json`
  - `readme.md`
- `test_set/`
  - `clips/`
  - `test_tasks_0627.json`
  - `readme.md`

## Environment Context

- Workspace root: `E:\lanenet model major`
- Shell: PowerShell
- Main environment seen in notebook: local `.venv`
- Current date during session: `2026-05-20`
- User requested that large dataset/code files be skimmed, not exhaustively dumped

## What Was Inspected

Files reviewed this session:

- `lanenet_model_mp.ipynb`
- `requirements.txt`
- `test_label.json`
- `train_set/readme.md`
- `test_set/readme.md`

Large folders `train_set` and `test_set` were not traversed deeply beyond structure/path validation.

## Key Findings About The Notebook

The notebook was originally written for Kaggle and had hardcoded paths like:

- `/kaggle/input/tusimple/TUSimple/train_set/clips`
- `/kaggle/input/tusimple/TUSimple/train_set/label_data_0313.json`

That made it fail locally in this workspace.

The notebook also used Linux-style path splitting:

- `frame_path[:-7].split('/')[-2:]`

That is fragile on Windows because local paths use backslashes.

## Changes Made This Session

### 1. Local path configuration added

The notebook was updated to derive paths from the current working directory instead of Kaggle.

Current path config in the notebook:

```python
from pathlib import Path

PROJECT_ROOT = Path.cwd()
TRAIN_SET_DIR = PROJECT_ROOT / 'train_set'
TEST_SET_DIR = PROJECT_ROOT / 'test_set'
PROCESSED_DIR = PROJECT_ROOT / 'tusimple_processed'
IMAGE_FOLDER = PROCESSED_DIR / 'images'
MASK_FOLDER = PROCESSED_DIR / 'mask'
LABEL_FILES = [
    TRAIN_SET_DIR / 'label_data_0313.json',
    TRAIN_SET_DIR / 'label_data_0531.json',
    TRAIN_SET_DIR / 'label_data_0601.json'
]
```

### 2. Clip path fixed

This was changed:

```python
CLIPS_PATH = "/kaggle/input/tusimple/TUSimple/train_set/clips"
```

to:

```python
CLIPS_PATH = TRAIN_SET_DIR / 'clips'
```

### 3. Windows-safe filename extraction fixed

This was changed:

```python
temp = frame_path[:-7].split('/')[-2:]
```

to:

```python
temp = Path(frame_path).parts[-2:]
```

This allows the generated filename logic to work on local Windows paths.

### 4. JSON label loading simplified and localized

The three hardcoded Kaggle JSON reads were replaced with:

```python
dataframes = [pd.read_json(label_file, lines=True) for label_file in LABEL_FILES]
df = pd.concat(dataframes, ignore_index=True)
```

### 5. Processed train/test output folders localized

These notebook variables now point into the local processed folder tree:

```python
train_image_folder = PROCESSED_DIR / 'train' / 'images'
test_image_folder  = PROCESSED_DIR / 'test' / 'images'
train_mask_folder  = PROCESSED_DIR / 'train' / 'masks'
test_mask_folder   = PROCESSED_DIR / 'test' / 'masks'
```

### 6. Sample inference image path fixed

This was changed from a Kaggle absolute path to:

```python
image_path = next(TRAIN_SET_DIR.glob('clips/*/*/20.jpg'))
```

### 7. Cell self-containment fix

After the first notebook patch, a later run produced:

```python
NameError: name 'Path' is not defined
```

Reason:

- the config cell depended on `Path` having already been imported in a previous cell
- if that earlier import cell was not re-run, the config cell failed

Fix applied:

- `from pathlib import Path` was added directly into the config/path cell so it can run independently

## Validation Performed

The following were validated successfully in this session:

- `train_set` exists
- `test_set` exists
- `train_set/clips` exists
- label files exist:
  - `train_set/label_data_0313.json`
  - `train_set/label_data_0531.json`
  - `train_set/label_data_0601.json`
- sample image resolved successfully:
  - `E:\lanenet model major\train_set\clips\0313-1\10000\20.jpg`
- the three training JSON files loaded successfully
- concatenated training annotation count: `3626`
- annotation columns:
  - `lanes`
  - `h_samples`
  - `raw_file`
- remaining Kaggle path references were removed from the notebook

## Requirements

From `requirements.txt`:

- `numpy==2.1.3`
- `scipy==1.14.0`
- `tensorflow==2.19.0`
- `pandas==3.0.3`
- `matplotlib==3.10.9`
- `opencv-python==4.13.0.92`
- `scikit-learn==1.8.0`
- `tqdm==4.67.3`
- `jupyter==1.1.1`
- `ipykernel==7.2.0`

## Current State At End Of Session

The notebook path layer is fixed for local use.

What is done:

- Kaggle-only dataset paths replaced with local project-root-based paths
- config cell made self-contained with `from pathlib import Path`
- local dataset existence and path resolution checked
- notebook structure understood at a high level
- FastAPI backend scaffold created under `backend/`
- React frontend scaffold created under `frontend/`
- backend and frontend dependencies installed
- backend inference path tested successfully against `best_model.keras`
- React frontend production build completed successfully

What is not yet done:

- full end-to-end notebook execution was not run
- training was started by the user, but not fully validated end-to-end by me
- no verification yet that every notebook cell completes in sequence
- no conversion from notebook to `.py` script
- no cleanup/refactor of notebook execution order
- browser-level manual test of the full React -> FastAPI upload flow was not run by me

## Additional Issue Found Later

After the initial path fixes, a later notebook run exposed a filename mismatch between extracted images and generated masks.

Problem:

- extracted images were being named like `10000_20.jpg.jpg`
- masks were being named like `0313-1_10000.jpg`
- `visualize_image(...)` assumes image and mask filenames match
- because of that mismatch, `cv2.imread(mask_path)` returned `None`
- Matplotlib then failed with:

```python
TypeError: Image data of dtype object cannot be converted to float
```

Root cause:

- the image extraction cell used the wrong slice of `Path(frame_path).parts`
- it picked the frame directory plus `20.jpg`, instead of clip directory plus frame directory

Fix applied:

- image extraction now uses:

```python
temp = Path(frame_path).parts[-3:-1]
```

- mask generation now also uses a `Path(...)`-based version:

```python
temp = Path(raw_file).parts[-3:-1]
```

- visualization now reads the mask as grayscale and raises a clear `FileNotFoundError` if the image or mask is missing

Important recovery note:

- if `tusimple_processed/images` and `tusimple_processed/mask` were already generated before this fix, they may still contain stale mismatched files
- to recover cleanly, delete the generated `tusimple_processed` folder and re-run the notebook from the extraction step onward, or just restart and run all after removing generated outputs

## More Fixes Applied After That

### 1. `pydot` installed in the local virtual environment

Installed:

- `pydot==4.0.1`

Installed into:

- `E:\lanenet model major\.venv`

Reason:

- needed for notebook model plotting support

Note:

- if `plot_model(...)` still fails, the likely remaining dependency is the Graphviz system install, not the Python package

### 2. Training epoch length reduced

Observed behavior:

- training was running `101/101` batches per epoch
- user requested reducing this to `10` batches per epoch

Updated training-step logic:

```python
EPOCHS = 10
MAX_STEPS_PER_EPOCH = 10
MAX_VALIDATION_STEPS = 10

full_steps_per_epoch = max(1, len(os.listdir(train_image_folder)) // BATCH_SIZE)
full_validation_steps = max(1, len(os.listdir(test_image_folder)) // BATCH_SIZE)

steps_per_epoch = min(MAX_STEPS_PER_EPOCH, full_steps_per_epoch)
validation_steps = min(MAX_VALIDATION_STEPS, full_validation_steps)

print(f'steps_per_epoch: {steps_per_epoch} / {full_steps_per_epoch}')
print(f'validation_steps: {validation_steps} / {full_validation_steps}')
```

Effect:

- training now uses at most `10` batches per epoch
- validation now uses at most `10` batches per epoch

Notebook note:

- if training was already running when this change was made, it must be interrupted
- then re-run the training config cell and the `model.fit(...)` cell

### 3. TensorFlow sample inference path type fixed

Observed error:

```python
ValueError: Attempt to convert a value (WindowsPath(...)) with an unsupported type (<class 'pathlib.WindowsPath'>) to a Tensor.
```

Cause:

- `next(TRAIN_SET_DIR.glob('clips/*/*/20.jpg'))` returns a `Path` object
- `tf.io.read_file(...)` was being given that `Path` directly

Fix applied:

```python
def load_test_image(image_path):
    size = [224, 224]
    image_path = str(image_path)

    image = tf.io.read_file(image_path)
    ...
```

Notebook note:

- re-run the cell defining `load_test_image(...)`
- then re-run the sample inference cell

## Frontend / Backend App Added

New app structure created:

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/model_loader.py`
- `backend/app/image_utils.py`
- `backend/app/inference.py`
- `backend/app/routes/predict.py`
- `backend/app/schemas.py`
- `backend/requirements.txt`
- `frontend/package.json`
- `frontend/src/...`
- `README.md`

Backend behavior:

- loads `best_model.keras` once through `get_model()`
- serves `GET /health`
- serves `POST /api/predict`
- writes output PNG files into `backend/outputs/`
- serves output images through `/outputs/...`

Frontend behavior:

- upload road image
- local browser preview
- send image to backend
- show status banner
- render original preview, predicted mask, and lane overlay
- allow downloading result images

Verification completed:

- backend Python modules compiled successfully
- model loaded successfully from `best_model.keras`
- sample inference succeeded through `backend.app.inference.run_inference(...)`
- React production build succeeded with `npm run build`

Installed dependencies during this session:

- backend runtime packages added to `.venv`:
  - `fastapi`
  - `uvicorn`
  - `python-multipart`
- frontend packages installed with `npm install`

## Important Resume Notes

If resuming later, the most likely next issue is not dataset paths anymore, but notebook execution order or environment/runtime problems.

Recommended resume sequence:

1. Open `lanenet_model_mp.ipynb`.
2. Restart the kernel.
3. Run the path/config cell first, or use `Restart & Run All`.
4. If old generated outputs exist from before the filename fix, delete `tusimple_processed/` first.
5. Confirm `tusimple_processed/` gets created.
6. Confirm image extraction and mask generation complete.
7. Confirm train/test split folders are populated.
8. Re-run the training config cell so `steps_per_epoch` is capped at `10`.
9. Continue with training and final sample inference.

For the web app:

1. Start the backend with:
   - `.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload`
2. Start the frontend with:
   - `cd frontend`
   - `npm run dev`
3. Open `http://localhost:5173`
4. Upload a road image and verify:
   - original preview
   - predicted mask
   - lane overlay

## Suggested Next Steps

When continuing this project, do these in order:

1. Run the notebook from the top after a kernel restart.
2. Remove stale `tusimple_processed` outputs if they were created before the filename-alignment fix.
3. Stop at the first runtime error, if any.
4. Fix any remaining notebook issues cell by cell.
5. Once the notebook runs cleanly, optionally convert it into a Python script for repeatable training.
6. Optionally add a `README.md` describing setup and run steps.

For the frontend/backend app:

1. Run the FastAPI backend locally.
2. Run the React frontend locally.
3. Do a browser-level manual upload test.
4. Tune overlay colors/opacity if visual output needs improvement.
5. If needed, add drag-drop polish, download naming cleanup, and better error details.

## Session Log Summary

Chronological summary of this session:

1. Repository structure was scanned while excluding deep traversal of dataset folders.
2. It was found that the repo is mainly one notebook plus requirements and dataset files.
3. Notebook code cells were skimmed to identify hardcoded paths and overall project flow.
4. Kaggle path assumptions were identified in:
   - clip extraction
   - JSON label loading
   - sample inference image path
5. Local dataset layout was checked and confirmed to match the expected TuSimple structure.
6. The notebook was patched to use local `Path.cwd()`-based paths.
7. Filename extraction was fixed to work on Windows path separators.
8. Remaining Kaggle references were checked and removed.
9. A user-reported `Path` `NameError` was fixed by making the config cell self-contained.
10. A later visualization error was traced to mismatched generated image and mask filenames.
11. Image extraction and mask naming were corrected to use matching clip/frame identifiers.
12. Visualization was hardened to raise clear missing-file errors and read masks as grayscale.
13. `pydot` was installed into the project virtual environment.
14. Training config was updated so each epoch uses at most `10` training and `10` validation batches.
15. A TensorFlow inference error caused by passing a `WindowsPath` into `tf.io.read_file(...)` was fixed by converting paths to `str`.
16. A FastAPI backend scaffold was created for model inference with `/health` and `/api/predict`.
17. A React frontend scaffold was created for upload, preview, status display, and result rendering.
18. Backend dependencies were installed into `.venv` and frontend dependencies were installed with `npm install`.
19. The backend model loader successfully loaded `best_model.keras`.
20. A real sample image was processed successfully through the new backend inference path.
21. The React app built successfully with `npm run build`.
22. `README.md` and `project_brain.md` were updated with the new app architecture and run steps.

## If You Resume With Codex Later

Tell Codex to read:

- `project_brain.md`
- `lanenet_model_mp.ipynb`

And state:

- the path fixes are already applied
- later fixes already applied include:
  - image/mask filename alignment
  - capped `steps_per_epoch`
  - `pydot` install
  - `Path` to `str` conversion for TensorFlow test-image loading
- a FastAPI + React app scaffold already exists in `backend/` and `frontend/`
- the backend inference path has already been verified on a real sample image
- the next task is to run the backend and frontend together and do the first browser-level manual test, then fix any integration issues
