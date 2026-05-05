import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import { api } from "../services/api";
import type { BusinessSegment } from "../types";

export default function SegmentsPage() {
  const [segments, setSegments] = useState<BusinessSegment[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: "", description: "" });

  const load = () => { api.getSegments().then(setSegments); };
  useEffect(load, []);

  const handleCreate = async () => {
    await api.createSegment(form);
    setShowModal(false);
    setForm({ name: "", description: "" });
    load();
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this segment?")) {
      await api.deleteSegment(id);
      load();
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Business Segments</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Add Segment
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
              {segments.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.description ?? "—"}</td>
                  <td><span className={`badge ${s.is_active ? "badge-resolved" : "badge-closed"}`}>{s.is_active ? "Active" : "Inactive"}</span></td>
                  <td>{new Date(s.created_at).toLocaleDateString()}</td>
                  <td>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.id)}>
                      <Trash2 size={14} />
                    </button>
                  </td>
                </tr>
              ))}
              {segments.length === 0 && (
                <tr><td colSpan={5} className="empty-state">No segments found</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Add Business Segment</h2>
            <div className="form-group">
              <label>Name</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="e.g. Lending, Payments" />
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
    </div>
  );
}
