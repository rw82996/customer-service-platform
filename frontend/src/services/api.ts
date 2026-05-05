import type {
  AnalyticsSummary,
  BusinessSegment,
  Client,
  ClientQuery,
  QueryResponse,
  QueryWithResponses,
  Staff,
  Team,
} from "../types";

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
  getSegments: () => request<BusinessSegment[]>("/api/business-segments/"),
  createSegment: (data: Partial<BusinessSegment>) =>
    request<BusinessSegment>("/api/business-segments/", { method: "POST", body: JSON.stringify(data) }),
  deleteSegment: (id: number) =>
    request<void>(`/api/business-segments/${id}`, { method: "DELETE" }),

  // Teams
  getTeams: () => request<Team[]>("/api/teams/"),
  getTeam: (id: number) => request<Team>(`/api/teams/${id}`),
  createTeam: (data: Partial<Team>) =>
    request<Team>("/api/teams/", { method: "POST", body: JSON.stringify(data) }),
  updateTeam: (id: number, data: Partial<Team>) =>
    request<Team>(`/api/teams/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteTeam: (id: number) =>
    request<void>(`/api/teams/${id}`, { method: "DELETE" }),

  // Staff
  getStaff: (teamId?: number) =>
    request<Staff[]>(`/api/staff/${teamId != null ? `?team_id=${teamId}` : ""}`),
  createStaff: (data: Partial<Staff>) =>
    request<Staff>("/api/staff/", { method: "POST", body: JSON.stringify(data) }),
  updateStaff: (id: number, data: Partial<Staff>) =>
    request<Staff>(`/api/staff/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteStaff: (id: number) =>
    request<void>(`/api/staff/${id}`, { method: "DELETE" }),

  // Clients
  getClients: (segmentId?: number) =>
    request<Client[]>(`/api/clients/${segmentId != null ? `?business_segment_id=${segmentId}` : ""}`),
  createClient: (data: Partial<Client>) =>
    request<Client>("/api/clients/", { method: "POST", body: JSON.stringify(data) }),
  updateClient: (id: number, data: Partial<Client>) =>
    request<Client>(`/api/clients/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteClient: (id: number) =>
    request<void>(`/api/clients/${id}`, { method: "DELETE" }),
  assignClientToTeam: (data: { client_id: number; team_id: number }) =>
    request<{ id: number }>("/api/clients/assignments", { method: "POST", body: JSON.stringify(data) }),
  getClientAssignments: (clientId: number) =>
    request<{ id: number; team_id: number; client_id: number }[]>(`/api/clients/${clientId}/assignments`),

  // Queries
  getQueries: (params?: Record<string, string | number>) => {
    const qs = params
      ? "?" + new URLSearchParams(
          Object.entries(params).map(([k, v]) => [k, String(v)])
        ).toString()
      : "";
    return request<ClientQuery[]>(`/api/queries/${qs}`);
  },
  getQuery: (id: number) => request<QueryWithResponses>(`/api/queries/${id}`),
  createQuery: (data: Partial<ClientQuery>) =>
    request<ClientQuery>("/api/queries/", { method: "POST", body: JSON.stringify(data) }),
  updateQuery: (id: number, data: Partial<ClientQuery>) =>
    request<ClientQuery>(`/api/queries/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  deleteQuery: (id: number) =>
    request<void>(`/api/queries/${id}`, { method: "DELETE" }),
  addResponse: (queryId: number, data: Partial<QueryResponse>) =>
    request<QueryResponse>(`/api/queries/${queryId}/responses`, { method: "POST", body: JSON.stringify(data) }),

  // Analytics
  getAnalytics: (segmentId?: number) =>
    request<AnalyticsSummary>(`/api/analytics/summary${segmentId != null ? `?business_segment_id=${segmentId}` : ""}`),
};
