# Ace Tech Solutions - Company Website

A modern, responsive website for Ace Tech Solutions, a Bangalore-based AI automation company. Built with Next.js 14, TypeScript, and Tailwind CSS.

## 🌐 Live Demo

Visit the website: [https://www.acetechsolutions.in](https://www.acetechsolutions.in)

## 🚀 Features

- **Modern Design**: Clean, professional design with mobile-first responsive layout
- **Fast Performance**: Built with Next.js 14 for optimal loading speeds
- **SEO Optimized**: Proper meta tags, Open Graph, and Twitter Cards for all pages
- **Accessibility**: Semantic HTML, keyboard navigation, and ARIA labels
- **Interactive Contact Form**: Form validation with React Hook Form
- **TypeScript**: Full type safety throughout the application
- **Tailwind CSS**: Utility-first CSS framework for rapid development

## 📁 Project Structure

```
ace-tech-website/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── about/             # About us page
│   │   ├── contact/           # Contact page with form
│   │   ├── privacy/           # Privacy policy page
│   │   ├── services/          # Services overview page
│   │   ├── terms/             # Terms of service page
│   │   ├── globals.css        # Global styles
│   │   ├── layout.tsx         # Root layout with header/footer
│   │   └── page.tsx           # Homepage
│   └── components/            # Reusable React components
│       ├── ContactForm.tsx    # Contact form with validation
│       ├── Footer.tsx         # Site footer
│       ├── Header.tsx         # Navigation header
│       ├── Hero.tsx           # Homepage hero section
│       └── ServicesSection.tsx # Services preview section
├── public/                    # Static assets
├── package.json              # Dependencies and scripts
└── README.md                 # This file
```

## 🛠 Technologies Used

- **Framework**: [Next.js 14](https://nextjs.org/) with App Router
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Icons**: [Heroicons](https://heroicons.com/)
- **Form Handling**: [React Hook Form](https://react-hook-form.com/)
- **Build Tool**: [Turbopack](https://turbo.build/pack) (Next.js)

## 📄 Pages Overview

### Home (`/`)
- Hero section with value proposition
- Services overview
- Company benefits and case studies
- Call-to-action sections

### About (`/about`)
- Company story and mission
- Core values and team information
- Bangalore-based identity

### Services (`/services`)
- Detailed service offerings:
  - Workflow Automation
  - AI Agents-as-a-Service
  - Custom AI Solutions
- Technology stack information
- Engagement options

### Contact (`/contact`)
- Interactive contact form with validation
- Company contact information
- FAQ section
- Process overview

### Legal Pages
- **Privacy Policy** (`/privacy`): Data protection and privacy practices
- **Terms of Service** (`/terms`): Service terms and conditions

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ace-tech-website
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**
   
   Navigate to [http://localhost:3000](http://localhost:3000) to view the website.

### Available Scripts

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm start` - Start the production server (after build)
- `npm run lint` - Run ESLint to check code quality

## 🎨 Customization

### Styling
- Primary colors and design tokens are defined in `tailwind.config.ts`
- Global styles are in `src/app/globals.css`
- Component-specific styles use Tailwind utility classes

### Content
- Page content can be modified directly in the respective page files
- Contact information is centralized in the Footer component
- SEO metadata is defined in each page's `metadata` export

### Contact Form
- Form validation rules are in `src/components/ContactForm.tsx`
- Currently logs form data to console (replace with actual submission logic)
- Form fields can be modified as needed

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file for environment-specific configuration:

```env
# Add your environment variables here
NEXT_PUBLIC_SITE_URL=https://www.acetechsolutions.in
```

### SEO Configuration
- Meta tags are configured in each page's `metadata` export
- Open Graph and Twitter Card support included
- Sitemap and robots.txt can be added to the `public` directory

## 📱 Responsive Design

The website is built with a mobile-first approach:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px

All components are fully responsive and tested across different screen sizes.

## ♿ Accessibility

- Semantic HTML structure
- Proper heading hierarchy
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Screen reader friendly

## 🚀 Deployment

### Vercel (Recommended)
1. Push code to GitHub repository
2. Connect repository to Vercel
3. Deploy automatically on push to main branch

### Other Platforms
The website can be deployed to any platform that supports Next.js:
- Netlify
- AWS Amplify
- DigitalOcean App Platform
- Railway

### Build Command
```bash
npm run build
```

### Start Command
```bash
npm start
```

## 📊 Performance

The website is optimized for performance:
- Static page generation where possible
- Optimized images and assets
- Minimal JavaScript bundle size
- Fast loading times

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For questions or support regarding this website:
- **Email**: contact@acetechsolutions.in
- **Location**: Bangalore, India

## 📄 License

This project is private and proprietary to Ace Tech Solutions.

---

**Built with ❤️ by Ace Tech Solutions**
