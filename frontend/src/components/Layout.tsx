import type { PropsWithChildren } from "react";

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="page-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Lane Segmentation Demo</p>
          <h1>Upload a road image and detect lane markings.</h1>
        </div>
      </header>
      <main className="content-grid">{children}</main>
    </div>
  );
}
