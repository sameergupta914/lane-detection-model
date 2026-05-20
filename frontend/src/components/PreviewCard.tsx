type PreviewCardProps = {
  previewUrl: string | null;
  filename: string | null;
};

export function PreviewCard({ previewUrl, filename }: PreviewCardProps) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Preview</h2>
        <p>{filename ?? "No file selected yet."}</p>
      </div>
      <div className="image-frame">
        {previewUrl ? <img src={previewUrl} alt="Selected road" /> : <div className="empty-card">No preview</div>}
      </div>
    </section>
  );
}
