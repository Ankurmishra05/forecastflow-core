import { fireEvent, render, screen } from "@testing-library/react";
import App from "./App";

test("shows validation error when fewer than 14 values are entered", async () => {
  render(<App />);

  fireEvent.change(screen.getByPlaceholderText(/112,118,132/i), {
    target: { value: "1,2,3" }
  });
  fireEvent.click(screen.getByRole("button", { name: /predict/i }));

  expect(
    await screen.findByText(/enter at least 14 historical values/i)
  ).toBeInTheDocument();
});
