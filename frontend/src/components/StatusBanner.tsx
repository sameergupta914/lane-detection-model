import type { Status } from "../types/prediction";

const STATUS_COPY: Record<Status, string> = {
  idle: "Choose a road image to begin.",
  ready: "Image selected. Run prediction when ready.",
  predicting: "Running inference. This may take a few seconds.",
  success: "Prediction completed successfully.",
  error: "Prediction failed. Review the error and try another image."
};

export function StatusBanner({ status, error }: { status: Status; error: string | null }) {
  return (
    <section className={`status-banner status-${status}`}>
      <strong>{STATUS_COPY[status]}</strong>
      {error ? <span>{error}</span> : null}
    </section>
  );
}
