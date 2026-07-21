# CrimeMatrix Frontend

React-based investigation dashboard and AI copilot interface.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Access at `http://localhost:5173`

## Tech Stack

- **Framework:** React 19.2
- **Styling:** Tailwind CSS 4.3
- **Build:** Vite 8.1
- **Charts:** Recharts 3.9
- **Routing:** React Router DOM 7.18
- **Icons:** Lucide React
- **Markdown:** React Markdown

## Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Crime stats, activity feed, quick actions |
| `/copilot` | AI Copilot | Chat with AI investigation assistant |
| `/cases` | Cases | Search and browse crime records |
| `/cases/:id` | Case Detail | Detailed case view with timeline |
| `/intelligence` | Intelligence | Crime intelligence hub |
| `/patterns` | Patterns | Crime pattern discovery |
| `/timeline` | Timeline | Criminal activity timeline |
| `/predictions` | Predictions | Crime forecasting dashboard |
| `/early-warning` | Early Warning | Proactive alerts |
| `/suspect-risk` | Suspect Risk | Risk scoring |
| `/prioritizations` | Priorities | Case prioritization |
| `/knowledge-graph` | Knowledge Graph | Entity relationship visualization |
| `/analytics-dashboard` | Analytics | AI analytics dashboard |
| `/suspects` | Suspects | Suspect management |
| `/suspects/:id` | Suspect Detail | Detailed suspect view |
| `/investigations` | Investigations | Investigation workspace |
| `/stations` | Stations | Geospatial station map |
| `/alerts` | Alerts | System alerts |
| `/bookmarks` | Bookmarks | Saved investigations |
| `/reports` | Reports | Report generation |
| `/settings` | Settings | Application settings |

## Components

46+ components organized by domain:

```
src/components/
├── copilot/           # Chat UI, history, context panel
├── search/            # Search interface
├── suspects/          # Suspect management
├── investigation/     # Investigation workspace
├── graph/             # Knowledge graph visualization
├── analytics/         # Analytics charts
├── predictions/       # Prediction dashboards
├── patterns/          # Pattern discovery
├── hotspots/          # Hotspot maps
├── trends/            # Trend charts
├── intelligence/      # Intelligence feed
├── recommendations/   # Recommendations
├── similar/           # Similar cases
├── alerts/            # Alert management
├── bookmarks/         # Bookmark management
├── reports/           # Report generation
├── map/               # Geospatial maps
├── charts/            # Shared chart components
├── icons/             # Custom icons
└── Layout, Header, Sidebar, RightPanel
```

## API Services

24 service modules in `src/services/`:

| Service | Domain |
|---------|--------|
| `api.js` | Base HTTP client (GET, POST, PUT, DELETE, SSE) |
| `copilot.js` | AI chat, sessions |
| `investigations.js` | Investigation CRUD |
| `graph.js` | Knowledge graph |
| `predictions.js` | Crime predictions |
| `search.js` | Search operations |
| `similarCases.js` | Similar case discovery |
| `voice.js` | Voice/speech integration |
| `trends.js` | Trend analysis |
| `patterns.js` | Pattern detection |
| `hotspots.js` | Hotspot detection |
| `maps.js` | Geospatial data |
| `criminalTimeline.js` | Criminal timelines |
| `behavior.js` | Behavioral profiling |
| `repeatOffenders.js` | Repeat offender tracking |
| `suspectRisk.js` | Risk scoring |
| `mo.js` | Modus operandi |
| `earlyWarning.js` | Early warning alerts |
| `priorities.js` | Case prioritization |
| `recommendations.js` | Recommendations |
| `intelligence.js` | Intelligence feed |
| `analyticsDashboard.js` | Analytics dashboard |
| `bookmarks.js` | Bookmark management |

## Design System

See [DESIGN.md](DESIGN.md) for the complete design system including:
- Brand identity and color tokens
- Typography scale
- Layout structure
- Component specifications
- Animation timings

## Build

```bash
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Lint with oxlint
```
