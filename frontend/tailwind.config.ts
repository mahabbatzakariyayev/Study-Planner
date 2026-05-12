import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: "#f7fafc",
        ink: "#0f172a",
        accent: "#0f766e",
        accentSoft: "#e6fffa"
      }
    },
  },
  plugins: [],
};

export default config;
