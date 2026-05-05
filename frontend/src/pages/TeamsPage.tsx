import { useEffect, useState } from "react";
import { Plus, Trash2, Eye } from "lucide-react";
import { api } from "../services/api";
import type { Team, Staff } from "../types";

export default function TeamsPage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState<(Team & { members: Staff[] }) | null>(null);
  const [form, setForm] = useState({ name: "", description: "" });

  const load = () => { api.getTeams().then(setTeams); };
  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await api.createTeam(form);
    setShowModal(false);
    setForm({ name: "", description: "" });
    load();
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this team?")) {
      await api.deleteTeam(id);
      load();
    }
  };

  const handleViewTeam = async (id: number) => {
    const team = await api.getTeam(id);
    setSelectedTeam({ ...team, members: team.members ?? [] });
    setShowDetailModal(true);
  };

  return (
    <div>
      <div className="page-header">
        <h1>Teams</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> New Team
        </button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((t) => (
                <tr key={t.id}>
                  <td>{t.name}</td>
                  <td>{t.description ?? "—"}</td>
                  <td><span className={`badge ${t.is_active ? "badge-resolved" : "badge-closed"}`}>{t.is_active ? "Active" : "Inactive"}</span></td>
                  <td>{new Date(t.created_at).toLocaleDateString()}</td>
                  <td style={{ display: "flex", gap: 6 }}>
                    <button className="btn btn-secondary btn-sm" onClick={() => handleViewTeam(t.id)}>
                      <Eye size={14} /> View
                    </button>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(t.id)}>
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))}
              {teams.length === 0 && (
                <tr><td colSpan={5} className="empty-state">No teams found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>New Team</h2>
            <div className="form-group">
              <label>Name</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea rows={2} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={!form.name}>Create</button>
            </div>
          </div>
        </div>
      )}

      {showDetailModal && selectedTeam && (
        <div className="modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{selectedTeam.name}</h2>
            <p style={{ color: "var(--gray-500)", marginBottom: 16 }}>{selectedTeam.description}</p>
            <h3 style={{ marginBottom: 8 }}>Members ({selectedTeam.members.length})</h3>
            {selectedTeam.members.length > 0 ? (
              <table>
                <thead>
                  <tr><th>Name</th><th>Email</th><th>Role</th></tr>
                </thead>
                <tbody>
                  {selectedTeam.members.map((m) => (
                    <tr key={m.id}>
                      <td>{m.name}</td>
                      <td>{m.email}</td>
                      <td><span className={`badge badge-${m.role}`}>{m.role}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-state">No members in this team</p>
            )}
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowDetailModal(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
