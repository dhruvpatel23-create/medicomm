export function Button({ className = "", variant = "primary", ...props }) {
  return <button className={`button button-${variant}${className ? ` ${className}` : ""}`} {...props} />;
}

export function Card({ className = "", as: Component = "article", ...props }) {
  return <Component className={`card${className ? ` ${className}` : ""}`} {...props} />;
}

export function Panel({ className = "", ...props }) {
  return <Card className={`panel${className ? ` ${className}` : ""}`} {...props} />;
}

export function Field({ label, children, className = "" }) {
  return (
    <label className={`field${className ? ` ${className}` : ""}`}>
      <span>{label}</span>
      {children}
    </label>
  );
}

export function Input({ className = "", ...props }) {
  return <input className={className} {...props} />;
}

export function Badge({ className = "", children }) {
  return <span className={`rank-pill${className ? ` ${className}` : ""}`}>{children}</span>;
}
