import { SESSION_TOKEN_KEY } from "./clientStorage";

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem(SESSION_TOKEN_KEY);
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers ?? {}),
  };
  const controller = new AbortController();
  const timeoutMs = options.timeoutMs ?? 8000;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(path, {
      ...options,
      headers,
      signal: controller.signal,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.message ?? "Request failed.");
    }

    return data;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The local server took too long to respond.");
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}
