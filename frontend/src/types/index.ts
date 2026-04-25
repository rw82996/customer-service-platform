export interface BusinessSegment {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
}

export interface Staff {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  team_id: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface Team {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
  members?: Staff[];
}

export interface Client {
  id: number;
  name: string;
  email: string;
  company: string | null;
  phone: string | null;
  is_active: boolean;
  business_segment_id: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface ClientQuery {
  id: number;
  subject: string;
  description: string;
  status: string;
  priority: string;
  category: string | null;
  created_at: string;
  updated_at: string | null;
  resolved_at: string | null;
  client_id: number;
  business_segment_id: number | null;
  assigned_staff_id: number | null;
}

export interface QueryResponse {
  id: number;
  message: string;
  is_internal_note: number;
  created_at: string;
  query_id: number;
  staff_id: number;
}

export interface QueryWithResponses extends ClientQuery {
  responses: QueryResponse[];
}

export interface StaffPerformance {
  staff_id: number;
  staff_name: string;
  total_responses: number;
  queries_resolved: number;
}

export interface AnalyticsSummary {
  total_queries: number;
  open_queries: number;
  in_progress_queries: number;
  resolved_queries: number;
  closed_queries: number;
  total_clients: number;
  total_staff: number;
  total_teams: number;
  avg_resolution_time_hours: number | null;
  queries_by_status: { status: string; count: number }[];
  queries_by_priority: { priority: string; count: number }[];
  queries_by_segment: { segment_name: string; count: number }[];
  staff_performance: StaffPerformance[];
  daily_query_trend: { date: string; count: number }[];
}
