/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary-dark': 'var(--color-primary-dark)',
        'primary-light': 'var(--color-primary-light)',
        'text-primary': 'var(--color-text-primary)',
        'background-light': 'var(--color-background-light)',
        'text-dark': 'var(--color-text-dark)',
        'accent': 'var(--color-accent)',
        'accent-darker': 'var(--color-accent-darker)',
        // Legacy support
        background: 'var(--background)',
        foreground: 'var(--foreground)',
      },
      fontFamily: {
        primary: 'var(--font-primary)',
        mono: 'var(--font-mono)',
        sans: ['var(--font-primary)', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xxl': 'var(--fz-xxl)',
        'xl': 'var(--fz-xl)',
        'lg': 'var(--fz-lg)',
        'md': 'var(--fz-md)',
        'sm': 'var(--fz-sm)',
        'xs': 'var(--fz-xs)',
      },
      spacing: {
        'xs': 'var(--space-xs)',
        'sm': 'var(--space-sm)',
        'md': 'var(--space-md)',
        'lg': 'var(--space-lg)',
        'xl': 'var(--space-xl)',
      },
      borderRadius: {
        'sm': 'var(--border-radius-sm)',
        'md': 'var(--border-radius-md)',
      },
      boxShadow: {
        'light': 'var(--box-shadow-light)',
        'heavy': 'var(--box-shadow-heavy)',
      },
      transitionTimingFunction: {
        'custom': 'cubic-bezier(0.645, 0.045, 0.355, 1)',
      },
    },
  },
  plugins: [],
}