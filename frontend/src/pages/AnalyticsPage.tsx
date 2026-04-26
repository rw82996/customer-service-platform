import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend,
} from "recharts";
import { api } from "../services/api";
import type { AnalyticsSummary, BusinessSegment } from "../types";

const STATUS_COLORS: Record<string, string> = {
  open: "#3b82f6",
  in_progress: "#f59e0b",
  resolved: "#10b981",
  closed: "#6b7280",
};

const PRIORITY_COLORS: Record<string, string> = {
  low: "#10b981",
  medium: "#f59e0b",
  high: "#ef4444",
  critical: "#dc2626",
};

const SEGMENT_COLORS = ["#3b82f6", "#8b5cf6", "#ec4899", "#f97316", "#14b8a6"];

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [segments, setSegments] = useState<BusinessSegment[]>([]);
  const [selectedSegment, setSelectedSegment] = useState("");

  useEffect(() => {
    api.getSegments().then(setSegments);
  }, []);

  useEffect(() => {
    const segmentId = selectedSegment ? Number(selectedSegment) : undefined;
    api.getAnalytics(segmentId).then(setAnalytics);
  }, [selectedSegment]);

  if (!analytics) return <div className="empty-state">Loading analytics...</div>;

  return (
    <div>
      <div className="page-header">
        <h1>Analytics & Insights</h1>
        <select
          value={selectedSegment}
          onChange={(e) => setSelectedSegment(e.target.value)}
          style={{ padding: "8px 12px", borderRadius: 8, border: "1px solid #d1d5db" }}
        >
          <option value="">All Segments</option>
          {segments.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
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
          <div className="stat-label">Resolved</div>
          <div className="stat-value success">{analytics.resolved_queries}</div>
        </div>
        <div className="stat-card">
          <div className="stat-label">Avg Resolution (hrs)</div>
          <div className="stat-value">{analytics.avg_resolution_time_hours ?? "N/A"}</div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="card">
          <div className="card-header"><h3>Queries by Status</h3></div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={analytics.queries_by_status}
                dataKey="count"
                nameKey="status"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(props) => `${props.name ?? ""} (${props.value})`}
              >
                {analytics.queries_by_status.map((entry) => (
                  <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || "#6b7280"} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header"><h3>Queries by Priority</h3></div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics.queries_by_priority}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="priority" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count">
                {analytics.queries_by_priority.map((entry) => (
                  <Cell key={entry.priority} fill={PRIORITY_COLORS[entry.priority] || "#6b7280"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header"><h3>Queries by Business Segment</h3></div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={analytics.queries_by_segment}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="segment_name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count">
                {analytics.queries_by_segment.map((_, index) => (
                  <Cell key={index} fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header"><h3>Daily Query Trend</h3></div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analytics.daily_query_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} name="Queries" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <div className="card-header"><h3>Staff Performance</h3></div>
        {analytics.staff_performance.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Staff</th>
                  <th>Total Responses</th>
                  <th>Queries Resolved</th>
                </tr>
              </thead>
              <tbody>
                {analytics.staff_performance.map((sp) => (
                  <tr key={sp.staff_id}>
                    <td>{sp.staff_name}</td>
                    <td>{sp.total_responses}</td>
                    <td>{sp.queries_resolved}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">No performance data available</div>
        )}
      </div>
    </div>
  );
}
