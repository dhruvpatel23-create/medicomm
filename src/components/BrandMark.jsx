import { useId } from "react";

export function BrandMark({ className = "", title = "Medulla" }) {
  const rawId = useId().replace(/:/g, "");
  const leftId = `${rawId}-left`;
  const rightId = `${rawId}-right`;
  const chevronId = `${rawId}-chevron`;
  const titleId = title ? `${rawId}-title` : undefined;

  return (
    <svg
      className={`brand-mark-svg${className ? ` ${className}` : ""}`}
      viewBox="0 0 64 64"
      role={title ? "img" : "presentation"}
      aria-labelledby={titleId}
      aria-hidden={title ? undefined : "true"}
      focusable="false"
    >
      {title ? <title id={titleId}>{title}</title> : null}
      <defs>
        <linearGradient id={leftId} x1="6" y1="13" x2="27" y2="59" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#42DEFF" />
          <stop offset="0.48" stopColor="#1187FF" />
          <stop offset="1" stopColor="#1153E6" />
        </linearGradient>
        <linearGradient id={rightId} x1="58" y1="13" x2="37" y2="59" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#2DF7C9" />
          <stop offset="0.55" stopColor="#15C5D6" />
          <stop offset="1" stopColor="#1174F1" />
        </linearGradient>
        <linearGradient id={chevronId} x1="12" y1="11" x2="52" y2="40" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="#F3FCFF" />
          <stop offset="0.4" stopColor="#A7EEFF" />
          <stop offset="1" stopColor="#20E4C7" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="60" height="60" rx="13" fill="#071327" />
      <path d="M8 18.2c0-4.8 5.4-7.6 9.3-4.8L32 24v17.7L8 25.4v-7.2Z" fill={`url(#${leftId})`} />
      <path d="M8 25.4 32 41.8l-8.3 8.5L8 39.7V25.4Z" fill="#0A6CF6" opacity=".92" />
      <path d="M8 25.4 23.8 36v21.3l-11.6-7.9A9.9 9.9 0 0 1 8 41.2V25.4Z" fill={`url(#${leftId})`} />
      <path d="M56 18.2c0-4.8-5.4-7.6-9.3-4.8L32 24v17.7l24-16.3v-7.2Z" fill={`url(#${rightId})`} />
      <path d="M56 25.4 40.2 36v21.3l11.6-7.9a9.9 9.9 0 0 0 4.2-8.2V25.4Z" fill={`url(#${rightId})`} />
      <path d="M13 13.8 32 30l19-16.2v10.8L32 42.4 13 24.6V13.8Z" fill={`url(#${chevronId})`} />
      <path d="M18 19.7 32 32.3l14-12.6v5.4L32 38.2 18 25.1v-5.4Z" fill="#FFFFFF" opacity=".76" />
      <circle cx="32" cy="11.5" r="4.5" fill="#25DFF2" />
    </svg>
  );
}