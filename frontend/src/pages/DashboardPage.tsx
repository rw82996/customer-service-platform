import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import type { AnalyticsSummary, ClientQuery } from "../types";

export default function DashboardPage() {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [recentQueries, setRecentQueries] = useState<ClientQuery[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.getAnalytics().then(setAnalytics);
    api.getQueries().then((q) => setRecentQueries(q.slice(0, 5)));
  }, []);

  if (!analytics) return <div className="empty-state">Loading...</div>;

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Queries</div>
          <div className="stat-value primary">{analytics.total_queries}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Open</div>
          <div className="stat-value warning">{analytics.open_queries}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">In Progress</div>
          <div className="stat-value">{analytics.in_progress_queries}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Resolved</div>
          <div className="stat-value success">{analytics.resolved_queries}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Clients</div>
          <div className="stat-value">{analytics.total_clients}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Staff</div>
          <div className="stat-value">{analytics.total_staff}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Teams</div>
          <div className="stat-value">{analytics.total_teams}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Avg Resolution (hrs)</div>
          <div className="stat-value">{analytics.avg_resolution_time_hours ?? "N/A"}</div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3>Recent Queries</h3>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate("/queries")}>
            View All
          </button>
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Subject</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {recentQueries.map((q) => (
                <tr key={q.id} className="clickable-row" onClick={() => navigate(`/queries/${q.id}`)}>
                  <td>#{q.id}</td>
                  <td>{q.subject}</td>
                  <td><span className={`badge badge-${q.status}`}>{q.status}</span></td>
                  <td><span className={`badge badge-${q.priority}`}>{q.priority}</span></td>
                  <td>{new Date(q.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
