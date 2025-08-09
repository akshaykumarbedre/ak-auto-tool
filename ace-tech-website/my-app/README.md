# Ace Tech Solutions - AI Automation Company Website

A modern, responsive website for Ace Tech Solutions, a Bangalore-based AI automation company specializing in affordable, high-impact automation services.

## 🌐 Live Demo

Visit the website at: [Local Development Server](http://localhost:3000)

## 📋 Features

### Core Pages
- **Home** (`/`) - Hero section, services overview, value propositions, case study, and CTA
- **About** (`/about`) - Company story, values, team information, and mission
- **Services** (`/services`) - Detailed breakdown of AI automation offerings
- **Contact** (`/contact`) - Contact form, company information, and FAQ
- **Privacy** (`/privacy`) - Privacy policy and data protection information  
- **Terms** (`/terms`) - Terms of service and legal information

### Technical Features
- ✅ **Next.js 15** with App Router for optimal performance
- ✅ **Tailwind CSS** for modern, responsive design
- ✅ **Mobile-first responsive design** with breakpoints
- ✅ **SEO optimized** with proper meta tags and Open Graph
- ✅ **Interactive contact form** with validation and success states
- ✅ **Clean, accessible HTML** with semantic structure
- ✅ **Fast loading** with optimized assets and static generation
- ✅ **Professional design** with consistent branding

### Components
- `Header` - Navigation with responsive mobile menu
- `Footer` - Company info, links, and social media
- `Hero` - Main landing section with compelling CTA
- `ServicesSection` - Overview of automation services
- `ContactForm` - Interactive form with validation

## 🚀 Getting Started

### Prerequisites
- Node.js 18.0 or later
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ace-tech-website/my-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build Commands

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── about/page.js      # About page
│   ├── contact/page.js    # Contact page  
│   ├── services/page.js   # Services page
│   ├── privacy/page.js    # Privacy policy
│   ├── terms/page.js      # Terms of service
│   ├── layout.js          # Root layout with Header/Footer
│   ├── page.js           # Home page
│   └── globals.css       # Global styles
└── components/            # Reusable components
    ├── Header.js         # Navigation header
    ├── Footer.js         # Site footer
    ├── Hero.js           # Hero section
    ├── ServicesSection.js # Services overview
    └── ContactForm.js    # Contact form
```

## 🎨 Design System

### Colors
- **Primary Blue**: `#2563eb` (blue-600)
- **Background**: `#ffffff` (white)
- **Text**: `#374151` (gray-700)
- **Accent**: Gradient from blue to indigo

### Typography
- **System font stack** for fast loading and cross-platform compatibility
- **Responsive text sizing** with mobile-first approach
- **Clear hierarchy** with consistent heading styles

### Layout
- **Max-width containers** (max-w-7xl) for optimal reading experience
- **Responsive grid systems** for flexible layouts
- **Consistent spacing** using Tailwind's spacing scale

## 📧 Contact Form

The contact form includes:
- **Client-side validation** for required fields
- **Success/error states** with user feedback
- **Responsive design** for all screen sizes
- **Accessible form elements** with proper labels

*Note: Form currently shows success message for demonstration. In production, integrate with your preferred backend service (EmailJS, Formspree, or custom API).*

## 🔧 Customization

### Adding New Pages
1. Create a new directory in `src/app/`
2. Add a `page.js` file with your component
3. Include proper metadata for SEO

### Modifying Content
- Update text content directly in the component files
- Modify colors and styling in `tailwind.config.js`
- Add new components in the `src/components/` directory

### SEO Optimization
Each page includes:
- Custom title and description
- Open Graph tags for social sharing
- Semantic HTML structure
- Fast loading times

## 🚀 Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Connect repository to Vercel
3. Deploy automatically

### Other Platforms
The app can be deployed to:
- Netlify
- AWS Amplify
- DigitalOcean App Platform
- Any static hosting service

### Build Output
- All pages are statically generated for optimal performance
- Total bundle size: ~105kB first load JS
- Lighthouse score: 95+ performance

## 📱 Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 License

This project is created for Ace Tech Solutions. All rights reserved.

## 🤝 Contributing

This is a client project. For modifications or updates, please contact the development team.

## 📞 Support

For technical support or questions about this website:
- Email: contact@acetechsolutions.in
- Location: Bangalore, India

---

**Built with ❤️ using Next.js and Tailwind CSS**
