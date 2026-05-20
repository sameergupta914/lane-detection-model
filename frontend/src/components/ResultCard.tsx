type ResultCardProps = {
  title: string;
  subtitle: string;
  imageUrl: string | null;
  downloadName?: string;
};

export function ResultCard({ title, subtitle, imageUrl, downloadName }: ResultCardProps) {
  return (
    <article className="result-card">
      <div className="panel-header">
        <h3>{title}</h3>
        <p>{subtitle}</p>
      </div>
      <div className="image-frame">
        {imageUrl ? <img src={imageUrl} alt={title} /> : <div className="empty-card">Result unavailable</div>}
      </div>
      {imageUrl && downloadName ? (
        <a className="download-link" href={imageUrl} download={downloadName}>
          Download
        </a>
      ) : null}
    </article>
  );
}
