import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        paper: "#f8f5ef",
        ember: "#b45309",
        ocean: "#0f766e",
        rose: "#be123c"
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        body: ["Trebuchet MS", "Verdana", "sans-serif"]
      },
      boxShadow: {
        soft: "0 20px 50px rgba(15, 23, 42, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;
