export async function apiRequest(path, options = {}) {
  localStorage.removeItem("medicomm-session-token");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };
  const controller = new AbortController();
  const timeoutMs = options.timeoutMs ?? 8000;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(path, {
      ...options,
      headers,
      credentials: "same-origin",
      signal: controller.signal,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.message ?? data.error ?? "Request failed.");
    }

    return data;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The server took too long to respond.");
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}
