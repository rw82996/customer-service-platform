import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus } from "lucide-react";
import { api } from "../services/api";
import type { ClientQuery, Client, Staff, BusinessSegment } from "../types";

export default function QueriesPage() {
  const [queries, setQueries] = useState<ClientQuery[]>([]);
  const [clients, setClients] = useState<Client[]>([]);
  const [staffList, setStaffList] = useState<Staff[]>([]);
  const [segments, setSegments] = useState<BusinessSegment[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [statusFilter, setStatusFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const navigate = useNavigate();

  const [form, setForm] = useState({
    subject: "",
    description: "",
    priority: "medium",
    category: "",
    client_id: "",
    business_segment_id: "",
    assigned_staff_id: "",
  });

  const load = () => {
    const params: Record<string, string> = {};
    if (statusFilter) params.status = statusFilter;
    if (priorityFilter) params.priority = priorityFilter;
    api.getQueries(params).then(setQueries);
  };

  useEffect(() => {
    load();
    api.getClients().then(setClients);
    api.getStaff().then(setStaffList);
    api.getSegments().then(setSegments);
  }, [statusFilter, priorityFilter]);

  const handleCreate = async () => {
    await api.createQuery({
      ...form,
      client_id: Number(form.client_id),
      business_segment_id: form.business_segment_id ? Number(form.business_segment_id) : null,
      assigned_staff_id: form.assigned_staff_id ? Number(form.assigned_staff_id) : null,
    });
    setShowModal(false);
    setForm({ subject: "", description: "", priority: "medium", category: "", client_id: "", business_segment_id: "", assigned_staff_id: "" });
    load();
  };

  return (
    <div>
      <div className="page-header">
        <h1>Queries</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> New Query
        </button>
      </div>

      <div className="filters">
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
        <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Subject</th>
                <th>Client</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Category</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {queries.map((q) => (
                <tr key={q.id} className="clickable-row" onClick={() => navigate(`/queries/${q.id}`)}>
                  <td>#{q.id}</td>
                  <td>{q.subject}</td>
                  <td>{clients.find((c) => c.id === q.client_id)?.name ?? q.client_id}</td>
                  <td><span className={`badge badge-${q.status}`}>{q.status}</span></td>
                  <td><span className={`badge badge-${q.priority}`}>{q.priority}</span></td>
                  <td>{q.category || "—"}</td>
                  <td>{new Date(q.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
              {queries.length === 0 && (
                <tr><td colSpan={7} className="empty-state">No queries found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>New Query</h2>
            <div className="form-group">
              <label>Subject</label>
              <input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Client</label>
                <select value={form.client_id} onChange={(e) => setForm({ ...form, client_id: e.target.value })}>
                  <option value="">Select client</option>
                  {clients.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Business Segment</label>
                <select value={form.business_segment_id} onChange={(e) => setForm({ ...form, business_segment_id: e.target.value })}>
                  <option value="">Select segment</option>
                  {segments.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Assign to Staff</label>
                <select value={form.assigned_staff_id} onChange={(e) => setForm({ ...form, assigned_staff_id: e.target.value })}>
                  <option value="">Unassigned</option>
                  {staffList.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Category</label>
              <input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="e.g. application, dispute, refund" />
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={!form.subject || !form.description || !form.client_id}>Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
