import { useEffect, useState } from "react";

import { predictLane } from "../api/client";
import { Layout } from "../components/Layout";
import { PreviewCard } from "../components/PreviewCard";
import { ResultCard } from "../components/ResultCard";
import { StatusBanner } from "../components/StatusBanner";
import { UploadPanel } from "../components/UploadPanel";
import type { PredictionResponse, Status } from "../types/prediction";

const ALLOWED_TYPES = new Set(["image/jpeg", "image/png"]);

export function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl(null);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  function resetAll() {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setStatus("idle");
  }

  function handleFileChange(file: File | null) {
    if (!file) {
      resetAll();
      return;
    }

    if (!ALLOWED_TYPES.has(file.type)) {
      setError("Please upload a JPG or PNG road image.");
      setStatus("error");
      setSelectedFile(null);
      setPreviewUrl(null);
      setResult(null);
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setError(null);
    setStatus("ready");
  }

  async function handlePredict() {
    if (!selectedFile) return;

    setStatus("predicting");
    setError(null);

    try {
      const prediction = await predictLane(selectedFile);
      setResult(prediction);
      setStatus("success");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Prediction failed.";
      setError(message);
      setStatus("error");
    }
  }

  return (
    <Layout>
      <StatusBanner status={status} error={error} />

      <div className="top-grid">
        <UploadPanel
          selectedFile={selectedFile}
          disabled={status === "predicting"}
          onFileChange={handleFileChange}
          onPredict={handlePredict}
          onReset={resetAll}
        />
        <PreviewCard previewUrl={previewUrl} filename={selectedFile?.name ?? null} />
      </div>

      <section className="results-section">
        <div className="panel-header">
          <h2>Results</h2>
          <p>
            {result
              ? `Inference time: ${result.inference_time_ms} ms | Original size: ${result.original_width} x ${result.original_height}`
              : "Run prediction to generate the mask and overlay."}
          </p>
        </div>
        <div className="results-grid">
          <ResultCard
            title="Original Image"
            subtitle="Local browser preview"
            imageUrl={previewUrl}
            downloadName={selectedFile?.name}
          />
          <ResultCard
            title="Predicted Mask"
            subtitle="Binary lane segmentation output"
            imageUrl={result?.mask_url ?? null}
            downloadName="lane-mask.png"
          />
          <ResultCard
            title="Lane Overlay"
            subtitle="Detected lanes blended on the original road"
            imageUrl={result?.overlay_url ?? null}
            downloadName="lane-overlay.png"
          />
        </div>
      </section>
    </Layout>
  );
}
