import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { api } from "../services/api";
import type { Client, BusinessSegment, Team } from "../types";

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([]);
  const [segments, setSegments] = useState<BusinessSegment[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [selectedClient, setSelectedClient] = useState<number | null>(null);
  const [assignTeamId, setAssignTeamId] = useState("");

  const [form, setForm] = useState({
    name: "",
    email: "",
    company: "",
    phone: "",
    business_segment_id: "",
  });

  const load = () => {
    api.getClients().then(setClients);
    api.getSegments().then(setSegments);
    api.getTeams().then(setTeams);
  };

  useEffect(load, []);

  const handleCreate = async () => {
    await api.createClient({
      ...form,
      business_segment_id: form.business_segment_id ? Number(form.business_segment_id) : null,
    });
    setShowModal(false);
    setForm({ name: "", email: "", company: "", phone: "", business_segment_id: "" });
    load();
  };

  const handleAssign = async () => {
    if (selectedClient && assignTeamId) {
      await api.assignClientToTeam({ client_id: selectedClient, team_id: Number(assignTeamId) });
      setShowAssignModal(false);
      setAssignTeamId("");
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Clients</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Add Client
        </button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Company</th>
                <th>Phone</th>
                <th>Segment</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((c) => (
                <tr key={c.id}>
                  <td>{c.name}</td>
                  <td>{c.email}</td>
                  <td>{c.company ?? "—"}</td>
                  <td>{c.phone ?? "—"}</td>
                  <td>{segments.find((s) => s.id === c.business_segment_id)?.name ?? "—"}</td>
                  <td>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => { setSelectedClient(c.id); setShowAssignModal(true); }}
                    >
                      Assign Team
                    </button>
                  </td>
                </tr>
              ))}
              {clients.length === 0 && (
                <tr><td colSpan={6} className="empty-state">No clients found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add Client</h2>
            <div className="form-row">
              <div className="form-group">
                <label>Name</label>
                <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Company</label>
                <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              </div>
            </div>
            <div className="form-group">
              <label>Business Segment</label>
              <select value={form.business_segment_id} onChange={(e) => setForm({ ...form, business_segment_id: e.target.value })}>
                <option value="">Select segment</option>
                {segments.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={!form.name || !form.email}>Create</button>
            </div>
          </div>
        </div>
      )}

      {showAssignModal && (
        <div className="modal-overlay" onClick={() => setShowAssignModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Assign Client to Team</h2>
            <div className="form-group">
              <label>Team</label>
              <select value={assignTeamId} onChange={(e) => setAssignTeamId(e.target.value)}>
                <option value="">Select team</option>
                {teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowAssignModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleAssign} disabled={!assignTeamId}>Assign</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
