import type { PropsWithChildren } from "react";

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Lane Segmentation Demo</p>
          <h1>Upload a road image and detect lane markings.</h1>
          <p className="hero-copy">
            This UI sends your image to the FastAPI inference service, generates a lane mask, and
            shows a visual overlay on the original road scene.
          </p>
        </div>
      </header>
      <main className="content-grid">{children}</main>
    </div>
  );
}
