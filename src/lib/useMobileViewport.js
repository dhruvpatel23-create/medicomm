import { useEffect, useState } from "react";

const MOBILE_VIEWPORT_QUERY = "(max-width: 820px)";

export function useMobileViewport() {
  const [mobile, setMobile] = useState(
    () => window.matchMedia(MOBILE_VIEWPORT_QUERY).matches,
  );

  useEffect(() => {
    const query = window.matchMedia(MOBILE_VIEWPORT_QUERY);
    const update = () => setMobile(query.matches);
    query.addEventListener("change", update);
    return () => query.removeEventListener("change", update);
  }, []);

  return mobile;
}
