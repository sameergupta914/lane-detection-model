import type { PredictionResponse } from "../types/prediction";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error("Backend health check failed.");
  }
  return response.json();
}

export async function predictLane(file: File): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    let error = "Prediction failed.";
    try {
      const body = await response.json();
      error = body.detail ?? body.error ?? error;
    } catch {
      // Keep the generic message.
    }
    throw new Error(error);
  }

  return response.json() as Promise<PredictionResponse>;
}
