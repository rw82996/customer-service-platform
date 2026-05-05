import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Send } from "lucide-react";
import { api } from "../services/api";
import type { QueryWithResponses, Client, Staff } from "../types";

export default function QueryDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [query, setQuery] = useState<QueryWithResponses | null>(null);
  const [clients, setClients] = useState<Client[]>([]);
  const [staffList, setStaffList] = useState<Staff[]>([]);
  const [responseText, setResponseText] = useState("");
  const [isInternal, setIsInternal] = useState(false);
  const [responderId, setResponderId] = useState("");
  const [statusUpdate, setStatusUpdate] = useState("");

  const load = () => {
    if (id) api.getQuery(Number(id)).then(setQuery);
  };

  useEffect(() => {
    load();
    api.getClients().then(setClients);
    api.getStaff().then(setStaffList);
  }, [id]);

  useEffect(() => {
    if (query) setStatusUpdate(query.status);
  }, [query]);

  const handleAddResponse = async () => {
    if (!id || !responseText || !responderId) return;
    await api.addResponse(Number(id), {
      message: responseText,
      is_internal_note: isInternal,
      staff_id: Number(responderId),
    });
    setResponseText("");
    load();
  };

  const handleStatusChange = async (newStatus: string) => {
    if (!id) return;
    await api.updateQuery(Number(id), { status: newStatus });
    setStatusUpdate(newStatus);
    load();
  };

  if (!query) return <div className="empty-state">Loading...</div>;

  const client = clients.find((c) => c.id === query.client_id);
  const assignedStaff = staffList.find((s) => s.id === query.assigned_staff_id);

  return (
    <div>
      <div className="page-header">
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate("/queries")}>
            <ArrowLeft size={16} />
          </button>
          <h1>Query #{query.id}</h1>
          <span className={`badge badge-${query.status}`}>{query.status}</span>
          <span className={`badge badge-${query.priority}`}>{query.priority}</span>
        </div>
      </div>

      <div className="detail-grid">
        <div>
          <div className="card">
            <h3 style={{ marginBottom: 8 }}>{query.subject}</h3>
            <p style={{ color: "var(--gray-600)", fontSize: 14 }}>{query.description}</p>
          </div>

          <div className="card">
            <div className="card-header">
              <h3>Responses ({query.responses.length})</h3>
            </div>
            <div className="response-thread">
              {query.responses.map((r) => (
                <div key={r.id} className={`response-item ${r.is_internal_note ? "internal-note" : ""}`}>
                  <div className="response-meta">
                    {staffList.find((s) => s.id === r.staff_id)?.name ?? `Staff #${r.staff_id}`}
                    {" · "}
                    {new Date(r.created_at).toLocaleString()}
                    {r.is_internal_note ? " · Internal Note" : ""}
                  </div>
                  <div className="response-message">{r.message}</div>
                </div>
              ))}
              {query.responses.length === 0 && (
                <div className="empty-state">No responses yet</div>
              )}
            </div>

            <div style={{ marginTop: 16, borderTop: "1px solid var(--gray-200)", paddingTop: 16 }}>
              <div className="form-group">
                <label>Add Response</label>
                <textarea
                  rows={3}
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  placeholder="Type your response..."
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Responder</label>
                  <select value={responderId} onChange={(e) => setResponderId(e.target.value)}>
                    <option value="">Select staff</option>
                    {staffList.map((s) => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>
                <div className="form-group" style={{ display: "flex", alignItems: "flex-end", gap: 12 }}>
                  <label style={{ display: "flex", alignItems: "center", gap: 6, cursor: "pointer" }}>
                    <input type="checkbox" checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} />
                    Internal Note
                  </label>
                  <button
                    className="btn btn-primary"
                    onClick={handleAddResponse}
                    disabled={!responseText || !responderId}
                  >
                    <Send size={14} /> Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className="card">
            <h3 style={{ marginBottom: 12 }}>Details</h3>
            <div className="detail-field">
              <div className="label">Client</div>
              <div className="value">{client?.name ?? query.client_id}</div>
            </div>
            <div className="detail-field">
              <div className="label">Company</div>
              <div className="value">{client?.company ?? "—"}</div>
            </div>
            <div className="detail-field">
              <div className="label">Assigned To</div>
              <div className="value">{assignedStaff?.name ?? "Unassigned"}</div>
            </div>
            <div className="detail-field">
              <div className="label">Category</div>
              <div className="value">{query.category ?? "—"}</div>
            </div>
            <div className="detail-field">
              <div className="label">Created</div>
              <div className="value">{new Date(query.created_at).toLocaleString()}</div>
            </div>
            {query.resolved_at && (
              <div className="detail-field">
                <div className="label">Resolved</div>
                <div className="value">{new Date(query.resolved_at).toLocaleString()}</div>
              </div>
            )}
          </div>

          <div className="card">
            <h3 style={{ marginBottom: 12 }}>Update Status</h3>
            <div className="form-group">
              <select value={statusUpdate} onChange={(e) => handleStatusChange(e.target.value)}>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
