# Customer Service Platform

A full-stack customer service management platform for logging client queries, recording responses, managing team entitlements, and viewing analytics — designed to support multiple business segments (lending, payments, insurance, etc.).

## Features

### Query Management
- Create, view, update, and delete client queries
- Filter queries by status, priority, client, and business segment
- Add responses to queries (client-facing or internal notes)
- Track query lifecycle: Open → In Progress → Resolved → Closed
- Automatic resolution time tracking

### Entitlement / Team Management
- Create and manage customer service teams
- Add staff members with roles (Agent, Supervisor, Admin)
- Assign staff to teams
- Assign clients to teams for entitlement-based service routing

### Multi-Segment Support
- Define business segments (e.g., Lending, Payments, Insurance, Wealth Management)
- Associate clients and queries with specific segments
- Filter analytics and queries by segment

### Analytics & Insights
- Dashboard with key metrics (total queries, open, resolved, avg resolution time)
- Queries by status (pie chart)
- Queries by priority (bar chart)
- Queries by business segment (bar chart)
- Daily query trend (line chart)
- Staff performance table (responses sent, queries resolved)
- Segment-level filtering for all analytics

## Tech Stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | Python, FastAPI, SQLAlchemy, SQLite |
| Frontend | React, TypeScript, Vite, Recharts  |
| Styling  | Custom CSS (no framework)          |

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# Seed sample data (optional)
python seed.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI is available at `http://localhost:5173`.

## API Endpoints

### Business Segments
- `GET /api/business-segments/` – List segments
- `POST /api/business-segments/` – Create segment
- `GET /api/business-segments/{id}` – Get segment
- `PATCH /api/business-segments/{id}` – Update segment
- `DELETE /api/business-segments/{id}` – Delete segment

### Teams
- `GET /api/teams/` – List teams
- `POST /api/teams/` – Create team
- `GET /api/teams/{id}` – Get team with members
- `PATCH /api/teams/{id}` – Update team
- `DELETE /api/teams/{id}` – Delete team

### Staff
- `GET /api/staff/` – List staff (optional `?team_id=`)
- `POST /api/staff/` – Create staff
- `GET /api/staff/{id}` – Get staff
- `PATCH /api/staff/{id}` – Update staff
- `DELETE /api/staff/{id}` – Delete staff

### Clients
- `GET /api/clients/` – List clients (optional `?business_segment_id=`)
- `POST /api/clients/` – Create client
- `GET /api/clients/{id}` – Get client
- `PATCH /api/clients/{id}` – Update client
- `DELETE /api/clients/{id}` – Delete client
- `POST /api/clients/assignments` – Assign client to team
- `GET /api/clients/{id}/assignments` – Get client's team assignments

### Queries
- `GET /api/queries/` – List queries (filters: `status`, `priority`, `client_id`, `business_segment_id`, `assigned_staff_id`)
- `POST /api/queries/` – Create query
- `GET /api/queries/{id}` – Get query with responses
- `PATCH /api/queries/{id}` – Update query
- `DELETE /api/queries/{id}` – Delete query
- `POST /api/queries/{id}/responses` – Add response to query
- `GET /api/queries/{id}/responses` – List responses

### Analytics
- `GET /api/analytics/summary` – Full analytics summary (optional `?business_segment_id=`)

## Project Structure

```
customer-service-platform/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── database.py      # Database configuration
│   │   └── main.py          # FastAPI application
│   ├── seed.py              # Sample data seeder
│   └── pyproject.toml       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main app with routing
│   │   └── index.css        # Global styles
│   └── package.json
└── README.md
```

## License

MIT
