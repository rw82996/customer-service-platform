import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import { api } from "../services/api";
import type { Staff, Team } from "../types";

export default function StaffPage() {
  const [staffList, setStaffList] = useState<Staff[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", role: "agent", team_id: "" });

  const load = () => {
    api.getStaff().then(setStaffList);
    api.getTeams().then(setTeams);
  };

  useEffect(load, []);

  const handleCreate = async () => {
    await api.createStaff({
      ...form,
      team_id: form.team_id ? Number(form.team_id) : null,
    });
    setShowModal(false);
    setForm({ name: "", email: "", role: "agent", team_id: "" });
    load();
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this staff member?")) {
      await api.deleteStaff(id);
      load();
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Staff</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Add Staff
        </button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Team</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {staffList.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.email}</td>
                  <td><span className={`badge badge-${s.role}`}>{s.role}</span></td>
                  <td>{teams.find((t) => t.id === s.team_id)?.name ?? "Unassigned"}</td>
                  <td><span className={`badge ${s.is_active ? "badge-resolved" : "badge-closed"}`}>{s.is_active ? "Active" : "Inactive"}</span></td>
                  <td>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.id)}>
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))}
              {staffList.length === 0 && (
                <tr><td colSpan={6} className="empty-state">No staff found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add Staff</h2>
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
                <label>Role</label>
                <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
                  <option value="agent">Agent</option>
                  <option value="supervisor">Supervisor</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="form-group">
                <label>Team</label>
                <select value={form.team_id} onChange={(e) => setForm({ ...form, team_id: e.target.value })}>
                  <option value="">No team</option>
                  {teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleCreate} disabled={!form.name || !form.email}>Create</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
