/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#8A2BE2',
        'primary-light': '#9D50BB',
        dark: '#121212',
        darker: '#0a0a0a',
        light: '#f8f8f8',
        'card-bg': 'rgba(30, 30, 30, 0.7)',
        'purple-end': '#16082f',
        'purple-accent': '#cc6eff',
        'purple-darker': '#6a11cb'
      },
      backgroundImage: {
        'gradient-main': 'linear-gradient(135deg, #0a0a0a 0%, #16082f 100%)',
        'gradient-primary': 'linear-gradient(90deg, #8A2BE2 0%, #cc6eff 100%)',
        'gradient-button': 'linear-gradient(135deg, #8A2BE2 0%, #6a11cb 100%)',
        'gradient-radial': 'radial-gradient(circle, var(--tw-gradient-stops))',
      },
      fontFamily: {
        'segoe': ['Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif'],
      },
      boxShadow: {
        'purple': '0 0 20px rgba(138, 43, 226, 0.3)',
        'purple-strong': '0 0 25px rgba(138, 43, 226, 0.5)',
        'purple-button': '0 5px 15px rgba(138, 43, 226, 0.4)',
        'purple-hover': '0 8px 25px rgba(138, 43, 226, 0.5)',
        'card': '0 10px 30px rgba(0, 0, 0, 0.3)',
        'card-hover': '0 15px 40px rgba(138, 43, 226, 0.2)',
      },
      animation: {
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(138, 43, 226, 0.3)' },
          '100%': { boxShadow: '0 0 30px rgba(138, 43, 226, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}