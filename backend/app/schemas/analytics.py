from pydantic import BaseModel


class QueryStatusCount(BaseModel):
    status: str
    count: int


class QueryPriorityCount(BaseModel):
    priority: str
    count: int


class SegmentQueryCount(BaseModel):
    segment_name: str
    count: int


class StaffPerformance(BaseModel):
    staff_id: int
    staff_name: str
    total_responses: int
    queries_resolved: int


class DailyQueryCount(BaseModel):
    date: str
    count: int


class AnalyticsSummary(BaseModel):
    total_queries: int
    open_queries: int
    in_progress_queries: int
    resolved_queries: int
    closed_queries: int
    total_clients: int
    total_staff: int
    total_teams: int
    avg_resolution_time_hours: float | None
    queries_by_status: list[QueryStatusCount]
    queries_by_priority: list[QueryPriorityCount]
    queries_by_segment: list[SegmentQueryCount]
    staff_performance: list[StaffPerformance]
    daily_query_trend: list[DailyQueryCount]
