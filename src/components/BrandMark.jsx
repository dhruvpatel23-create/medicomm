export function BrandMark({ className = "", title = "Medulla" }) {
  return (
    <img
      className={`brand-mark-image${className ? ` ${className}` : ""}`}
      src="/medulla-logo.jpg"
      alt={title}
      aria-hidden={title ? undefined : "true"}
      width="1254"
      height="1254"
      draggable={false}
    />
  );
}
