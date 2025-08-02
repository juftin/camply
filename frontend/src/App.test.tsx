import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "./App";

Object.defineProperty(globalThis, "fetch", {
  value: vi.fn(),
  writable: true,
});

describe("App", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("renders the app title and description", () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      json: async () => ({ status: 200, timestamp: "2024-01-01T00:00:00Z" }),
    });

    render(<App />);

    expect(screen.getByText("Camply Web")).toBeInTheDocument();
    expect(
      screen.getByText("Find campsites at sold-out campgrounds"),
    ).toBeInTheDocument();
    expect(screen.getByText("Backend Status")).toBeInTheDocument();
  });

  it("shows loading state initially", () => {
    (fetch as ReturnType<typeof vi.fn>).mockImplementation(
      () => new Promise(() => {}),
    );

    render(<App />);

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("displays health status when API call succeeds", async () => {
    const mockHealthData = {
      status: 200,
      timestamp: "2024-01-01T12:00:00Z",
    };

    (fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      json: async () => mockHealthData,
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Status: 200")).toBeInTheDocument();
      expect(
        screen.getByText("Timestamp: 2024-01-01T12:00:00Z"),
      ).toBeInTheDocument();
    });
  });

  it("displays error message when API call fails", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(
      new Error("Network error"),
    );

    render(<App />);

    await waitFor(() => {
      expect(
        screen.getByText("Failed to connect to backend"),
      ).toBeInTheDocument();
    });
  });
});
