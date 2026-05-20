export type PredictionResponse = {
  success: boolean;
  filename: string;
  inference_time_ms: number;
  original_width: number;
  original_height: number;
  mask_url: string;
  overlay_url: string;
};

export type Status = "idle" | "ready" | "predicting" | "success" | "error";
