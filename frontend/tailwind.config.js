/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#F5F0F8',
          100: '#E9DCEF',
          200: '#CBAFDA',
          300: '#AC82C4',
          400: '#8A5CA6',
          500: '#5E3B76',
          600: '#4B2F60',
          700: '#452A58',
          800: '#341F43',
          900: '#241530',
        },
        surface: {
          DEFAULT: '#F5F6F8',
          card: '#FFFFFF',
          border: '#E4E6EB',
          muted: '#EFF1F5',
        },
        ink: {
          DEFAULT: '#1F2430',
          muted: '#6B7280',
          soft: '#9CA3AF',
        },
        status: {
          available: '#1F9E77',
          allocated: '#3E6FD9',
          reserved: '#D98E04',
          maintenance: '#B45FBE',
          lost: '#DC4C4C',
          retired: '#6B7280',
          disposed: '#3F4451',
        },
      },
      boxShadow: {
        card: '0 1px 2px rgba(31, 36, 48, 0.06), 0 1px 8px rgba(31, 36, 48, 0.04)',
        popover: '0 8px 24px rgba(31, 36, 48, 0.12)',
      },
      borderRadius: {
        card: '10px',
      },
    },
  },
  plugins: [],
};
