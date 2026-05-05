import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  MessageSquare,
  Users,
  Building2,
  UserCog,
  BarChart3,
  Layers,
} from "lucide-react";
import DashboardPage from "./pages/DashboardPage";
import QueriesPage from "./pages/QueriesPage";
import QueryDetailPage from "./pages/QueryDetailPage";
import ClientsPage from "./pages/ClientsPage";
import TeamsPage from "./pages/TeamsPage";
import StaffPage from "./pages/StaffPage";
import SegmentsPage from "./pages/SegmentsPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <aside className="sidebar">
          <div className="sidebar-brand">
            <h2>CS Platform</h2>
            <p>Customer Service Management</p>
          </div>
          <nav>
            <NavLink to="/" end>
              <LayoutDashboard size={18} /> Dashboard
            </NavLink>
            <NavLink to="/queries">
              <MessageSquare size={18} /> Queries
            </NavLink>
            <NavLink to="/clients">
              <Building2 size={18} /> Clients
            </NavLink>
            <NavLink to="/teams">
              <Users size={18} /> Teams
            </NavLink>
            <NavLink to="/staff">
              <UserCog size={18} /> Staff
            </NavLink>
            <NavLink to="/segments">
              <Layers size={18} /> Business Segments
            </NavLink>
            <NavLink to="/analytics">
              <BarChart3 size={18} /> Analytics
            </NavLink>
          </nav>
        </aside>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/queries" element={<QueriesPage />} />
            <Route path="/queries/:id" element={<QueryDetailPage />} />
            <Route path="/clients" element={<ClientsPage />} />
            <Route path="/teams" element={<TeamsPage />} />
            <Route path="/staff" element={<StaffPage />} />
            <Route path="/segments" element={<SegmentsPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
