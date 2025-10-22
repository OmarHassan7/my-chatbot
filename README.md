# AI Chatbot - Next.js Frontend

This is a modern Next.js frontend for the AI Chatbot application, built with TypeScript and Tailwind CSS.

## Features

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Responsive Design** with modern UI/UX
- **Real-time Chat Interface** with loading states
- **API Integration** with FastAPI backend

## Project Structure

```
├── components/           # React components
│   ├── ChatbotInterface.tsx  # Main chat interface
│   ├── Message.tsx          # Individual message component
│   ├── LoadingMessage.tsx   # Loading state component
│   └── Icons.tsx           # SVG icon components
├── pages/               # Next.js pages
│   ├── _app.tsx         # App wrapper
│   └── index.tsx        # Home page
├── styles/              # Global styles
│   └── globals.css      # Tailwind CSS imports
├── utils/               # Utility functions
│   └── api.ts           # API integration
├── api/                 # FastAPI backend (unchanged)
└── package.json         # Dependencies
```

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:

```bash
npm install
```

2. Run the development server:

```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## API Integration

The frontend communicates with the FastAPI backend through:

- **Chat Endpoint**: `/api/chat` - Send messages and receive responses
- **Status Endpoint**: `/api` - Check API health

## Deployment

This project is configured for Vercel deployment with:

- Next.js frontend
- FastAPI backend (Python)
- Automatic builds and deployments

## Migration from HTML

This Next.js version replaces the previous HTML-based frontend with:

- ✅ Modern React components with TypeScript
- ✅ Better performance and SEO
- ✅ Improved developer experience
- ✅ Server-side rendering capabilities
- ✅ Better code organization and maintainability
