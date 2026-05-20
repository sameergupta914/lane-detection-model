import type { ChangeEvent, DragEvent } from "react";

type UploadPanelProps = {
  selectedFile: File | null;
  disabled: boolean;
  onFileChange: (file: File | null) => void;
  onPredict: () => void;
  onReset: () => void;
};

export function UploadPanel({
  selectedFile,
  disabled,
  onFileChange,
  onPredict,
  onReset
}: UploadPanelProps) {
  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    onFileChange(event.target.files?.[0] ?? null);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    if (disabled) return;
    const file = event.dataTransfer.files?.[0] ?? null;
    onFileChange(file);
  }

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Upload</h2>
        <p>Accepted formats: JPG, JPEG, PNG</p>
      </div>
      <label
        className={`dropzone ${disabled ? "dropzone-disabled" : ""}`}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".jpg,.jpeg,.png,image/jpeg,image/png"
          onChange={handleInputChange}
          disabled={disabled}
        />
        <span>{selectedFile ? selectedFile.name : "Drop an image here or click to browse."}</span>
      </label>
      <div className="button-row">
        <button className="primary-button" onClick={onPredict} disabled={!selectedFile || disabled}>
          Detect Lanes
        </button>
        <button className="secondary-button" onClick={onReset} disabled={disabled}>
          Reset
        </button>
      </div>
    </section>
  );
}
