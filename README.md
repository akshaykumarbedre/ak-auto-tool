# AK Auto Tool - AI & Automation Projects Repository

A collection of AI automation tools and projects including MCP (Model Context Protocol) servers, web applications, and documentation utilities.

## 📚 Repository Overview

This repository contains multiple projects focused on AI automation, web development, and document processing tools. Each project is self-contained with its own documentation and dependencies.

## 🚀 Projects

### 1. **proj1** - MCP Tool Suite

A comprehensive suite of two powerful MCP (Model Context Protocol) tools for documentation and website processing:

#### **MCP Tool for Document Loading and Retrieval**
- **Purpose**: Load and search documentation from any Python library's URL using hybrid search capabilities
- **Key Features**:
  - URL-based documentation loading with recursive traversal
  - Hybrid search combining vector similarity and keyword matching
  - FAISS-based vector store for efficient retrieval
  - Support for multiple search types (similarity, MMR, threshold-based)
  - Document statistics and analytics
- **Technologies**: Python, LangChain, FAISS, SentenceTransformers, BeautifulSoup
- **Use Cases**: Documentation search, library reference queries, knowledge retrieval

#### **MCP Website Generator**
- **Purpose**: Generate MCP retrievers from websites with semantic search capabilities
- **Key Features**:
  - Recursive website scraping with configurable depth limits
  - Semantic embeddings using SentenceTransformers
  - FAISS integration for efficient vector storage
  - Centralized MCP registry for managing multiple website retrievers
  - CLI interface and Python API
  - Persistent storage of indices and metadata
- **Technologies**: Python, FAISS, SentenceTransformers, BeautifulSoup, Requests
- **Use Cases**: Website content indexing, semantic search, documentation retrieval systems

📁 **Location**: `/proj1`  
📖 **Documentation**: See `/proj1/README.md` and `/proj1/mcp_tool/README.md`

---

### 2. **ace-tech-website** - AI Automation Company Website

A modern, professional website for Ace Tech Solutions, a Bangalore-based AI automation company.

- **Purpose**: Corporate website showcasing AI automation services
- **Key Features**:
  - Responsive design with mobile-first approach
  - Multiple pages: Home, About, Services, Contact, Privacy, Terms
  - Interactive contact form with validation
  - SEO optimized with meta tags and Open Graph support
  - Clean, accessible UI with Tailwind CSS
  - Fast loading with Next.js 15 static generation
- **Technologies**: Next.js 15, React 19, Tailwind CSS
- **Pages**:
  - Home: Hero section, services overview, value propositions
  - About: Company story, values, team information
  - Services: Detailed AI automation offerings
  - Contact: Interactive form with FAQ
  - Privacy & Terms: Legal documentation

📁 **Location**: `/ace-tech-website/my-app`  
📖 **Documentation**: See `/ace-tech-website/my-app/README.md`  
🌐 **Local Dev**: `npm run dev` at http://localhost:3000

---

### 3. **proj2** - Future Project

- **Status**: Planning phase
- **Purpose**: Reserved for future development requirements

📁 **Location**: `/proj2`

---

### 4. **proj3** - Future Project

- **Status**: Planning phase
- **Purpose**: Reserved for future development requirements

📁 **Location**: `/proj3`

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.8+** (for proj1 MCP tools)
- **Node.js 18+** (for ace-tech-website)
- **pip** or **uv** (Python package managers)
- **npm** or **yarn** (Node.js package managers)

### Quick Start Guide

#### For MCP Tools (proj1)

```bash
# Navigate to proj1
cd proj1

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Install additional dependencies
pip install sentence-transformers faiss-cpu

# Example 1: Generate MCP from website (Website Generator Tool)
python -m mcp_tool.generate_mcp --url "https://www.langchain.com" --name "langchain"

# Example 2: Query an existing MCP
python -m mcp_tool.generate_mcp --query "langchain" --search "how to use retrievers"

# Note: The Document Loading tool is used programmatically via Python API
# See proj1/README.md for detailed usage examples
```

#### For Ace Tech Website

```bash
# Navigate to the website app
cd ace-tech-website/my-app

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## 📖 Documentation

Each project contains detailed documentation:

- **proj1 MCP Tools**: Comprehensive guides for both tools
  - `/proj1/README.md` - Document Loading and Retrieval tool documentation
  - `/proj1/mcp_tool/README.md` - MCP Website Generator documentation
  - `/proj1/sample_mcp_creation_doc.txt` - Detailed MCP creation tutorial

- **ace-tech-website**: Complete website documentation with setup, features, and deployment guides
  - `/ace-tech-website/my-app/README.md` - Full website documentation

---

## 🎯 Use Cases

### MCP Document Loader
- Search Python library documentation efficiently
- Retrieve relevant information from technical docs
- Build custom documentation search systems
- Integrate with AI assistants for documentation queries

### MCP Website Generator
- Index entire websites for semantic search
- Create searchable knowledge bases from web content
- Build custom retrievers for AI applications
- Connect Claude Desktop to website content

### Ace Tech Website
- Corporate presence for AI automation services
- Lead generation through contact forms
- Showcase AI automation capabilities
- Professional client-facing platform

---

## 🔧 Technologies Used

### proj1 - MCP Tools
- **Python 3.8+**
- **LangChain** - Document processing and retrieval
- **FAISS** - Vector similarity search
- **SentenceTransformers** - Text embeddings
- **BeautifulSoup4** - Web scraping
- **Pandas** - Data manipulation

### ace-tech-website
- **Next.js 15** - React framework
- **React 19** - UI library
- **Tailwind CSS** - Utility-first CSS
- **JavaScript/JSX** - Programming language

### Development Tools
- **Git** - Version control
- **npm** - Node.js package management
- **uv** - Python package management
- **Virtual environments** - Python isolation

---

## 📂 Repository Structure

```
ak-auto-tool/
├── proj1/                          # MCP Tools Suite
│   ├── mcp_tool/                   # Website generator tool
│   │   ├── scrapers/               # Web scraping modules
│   │   ├── indexers/               # FAISS indexing
│   │   ├── mcps/                   # MCP registry
│   │   └── generate_mcp.py         # Main entry point
│   ├── mcp_indices/                # Generated indices storage
│   ├── requirements.txt            # Python dependencies
│   ├── setup.sh                    # Setup script
│   └── README.md                   # Documentation
│
├── ace-tech-website/               # Corporate website
│   └── my-app/                     # Next.js application
│       ├── src/
│       │   ├── app/                # Next.js pages
│       │   └── components/         # React components
│       ├── package.json            # Node dependencies
│       └── README.md               # Website documentation
│
├── proj2/                          # Future project
├── proj3/                          # Future project
└── README.md                       # This file

```

---

## 🤝 Contributing

Contributions are welcome! Each project maintains its own contribution guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities:

- **Email**: contact@acetechsolutions.in (for website-related inquiries)
- **Location**: Bangalore, India
- **GitHub**: [akshaykumarbedre/ak-auto-tool](https://github.com/akshaykumarbedre/ak-auto-tool)

---

## 🔮 Roadmap

### Current Focus
- ✅ MCP document loading and retrieval tools
- ✅ MCP website generator with semantic search
- ✅ Professional corporate website for Ace Tech Solutions

### Future Plans
- 🔄 Development of proj2 and proj3
- 🔄 Enhanced AI automation tools
- 🔄 Additional MCP integrations
- 🔄 Expanded website features

---

**Built with ❤️ for AI automation and modern web development**
