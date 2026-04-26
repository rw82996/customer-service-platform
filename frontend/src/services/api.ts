const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  // Business Segments
  getSegments: () => request<any[]>("/api/business-segments/"),
  createSegment: (data: any) =>
    request<any>("/api/business-segments/", { method: "POST", body: JSON.stringify(data) }),
  deleteSegment: (id: number) =>
    request<void>(`/api/business-segments/${id}`, { method: "DELETE" }),

  // Teams
  getTeams: () => request<any[]>("/api/teams/"),
  getTeam: (id: number) => request<any>(`/api/teams/${id}`),
  createTeam: (data: any) =>
    request<any>("/api/teams/", { method: "POST", body: JSON.stringify(data) }),
  updateTeam: (id: number, data: any) =>
    request<any>(`/api/teams/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteTeam: (id: number) =>
    request<void>(`/api/teams/${id}`, { method: "DELETE" }),

  // Staff
  getStaff: (teamId?: number) =>
    request<any[]>(`/api/staff/${teamId != null ? `?team_id=${teamId}` : ""}`),
  createStaff: (data: any) =>
    request<any>("/api/staff/", { method: "POST", body: JSON.stringify(data) }),
  updateStaff: (id: number, data: any) =>
    request<any>(`/api/staff/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteStaff: (id: number) =>
    request<void>(`/api/staff/${id}`, { method: "DELETE" }),

  // Clients
  getClients: (segmentId?: number) =>
    request<any[]>(`/api/clients/${segmentId != null ? `?business_segment_id=${segmentId}` : ""}`),
  createClient: (data: any) =>
    request<any>("/api/clients/", { method: "POST", body: JSON.stringify(data) }),
  updateClient: (id: number, data: any) =>
    request<any>(`/api/clients/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteClient: (id: number) =>
    request<void>(`/api/clients/${id}`, { method: "DELETE" }),
  assignClientToTeam: (data: any) =>
    request<any>("/api/clients/assignments", { method: "POST", body: JSON.stringify(data) }),
  getClientAssignments: (clientId: number) =>
    request<any[]>(`/api/clients/${clientId}/assignments`),

  // Queries
  getQueries: (params?: Record<string, string | number>) => {
    const qs = params
      ? "?" + new URLSearchParams(
          Object.entries(params).map(([k, v]) => [k, String(v)])
        ).toString()
      : "";
    return request<any[]>(`/api/queries/${qs}`);
  },
  getQuery: (id: number) => request<any>(`/api/queries/${id}`),
  createQuery: (data: any) =>
    request<any>("/api/queries/", { method: "POST", body: JSON.stringify(data) }),
  updateQuery: (id: number, data: any) =>
    request<any>(`/api/queries/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteQuery: (id: number) =>
    request<void>(`/api/queries/${id}`, { method: "DELETE" }),
  addResponse: (queryId: number, data: any) =>
    request<any>(`/api/queries/${queryId}/responses`, { method: "POST", body: JSON.stringify(data) }),

  // Analytics
  getAnalytics: (segmentId?: number) =>
    request<any>(`/api/analytics/summary${segmentId != null ? `?business_segment_id=${segmentId}` : ""}`),
};
