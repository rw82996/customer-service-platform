from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.business_segment import BusinessSegment
from app.models.client import Client
from app.models.query import ClientQuery, QueryResponse
from app.models.staff import Staff
from app.models.team import Team
from app.schemas.analytics import (
    AnalyticsSummary,
    DailyQueryCount,
    QueryPriorityCount,
    QueryStatusCount,
    SegmentQueryCount,
    StaffPerformance,
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    business_segment_id: int | None = None,
    db: Session = Depends(get_db),
):
    base_q = db.query(ClientQuery)
    if business_segment_id is not None:
        base_q = base_q.filter(ClientQuery.business_segment_id == business_segment_id)

    total = base_q.count()
    open_q = base_q.filter(ClientQuery.status == "open").count()
    in_progress = base_q.filter(ClientQuery.status == "in_progress").count()
    resolved = base_q.filter(ClientQuery.status == "resolved").count()
    closed = base_q.filter(ClientQuery.status == "closed").count()

    total_clients = db.query(Client).count()
    total_staff = db.query(Staff).count()
    total_teams = db.query(Team).count()

    # Average resolution time
    resolved_queries = base_q.filter(
        ClientQuery.resolved_at.isnot(None),
        ClientQuery.created_at.isnot(None),
    ).all()
    avg_hours = None
    if resolved_queries:
        total_hours = 0.0
        count = 0
        for q in resolved_queries:
            if q.resolved_at and q.created_at:
                delta = q.resolved_at - q.created_at
                total_hours += delta.total_seconds() / 3600
                count += 1
        if count > 0:
            avg_hours = round(total_hours / count, 2)

    # Queries by status
    status_counts = (
        db.query(ClientQuery.status, func.count(ClientQuery.id))
        .group_by(ClientQuery.status)
        .all()
    )
    queries_by_status = [QueryStatusCount(status=s, count=c) for s, c in status_counts]

    # Queries by priority
    priority_counts = (
        db.query(ClientQuery.priority, func.count(ClientQuery.id))
        .group_by(ClientQuery.priority)
        .all()
    )
    queries_by_priority = [
        QueryPriorityCount(priority=p, count=c) for p, c in priority_counts
    ]

    # Queries by segment
    segment_counts = (
        db.query(BusinessSegment.name, func.count(ClientQuery.id))
        .join(ClientQuery, ClientQuery.business_segment_id == BusinessSegment.id)
        .group_by(BusinessSegment.name)
        .all()
    )
    queries_by_segment = [
        SegmentQueryCount(segment_name=name, count=c) for name, c in segment_counts
    ]

    # Staff performance
    staff_response_counts = (
        db.query(
            Staff.id,
            Staff.name,
            func.count(QueryResponse.id).label("total_responses"),
        )
        .join(QueryResponse, QueryResponse.staff_id == Staff.id)
        .group_by(Staff.id, Staff.name)
        .all()
    )
    staff_resolved = (
        db.query(
            ClientQuery.assigned_staff_id,
            func.count(ClientQuery.id),
        )
        .filter(ClientQuery.status.in_(["resolved", "closed"]))
        .group_by(ClientQuery.assigned_staff_id)
        .all()
    )
    resolved_map = {sid: cnt for sid, cnt in staff_resolved if sid is not None}
    staff_performance = [
        StaffPerformance(
            staff_id=sid,
            staff_name=sname,
            total_responses=resp_count,
            queries_resolved=resolved_map.get(sid, 0),
        )
        for sid, sname, resp_count in staff_response_counts
    ]

    # Daily query trend (last 30 days)
    daily_counts = (
        db.query(
            func.date(ClientQuery.created_at).label("day"),
            func.count(ClientQuery.id),
        )
        .group_by(func.date(ClientQuery.created_at))
        .order_by(func.date(ClientQuery.created_at))
        .limit(30)
        .all()
    )
    daily_query_trend = [
        DailyQueryCount(date=str(day), count=c) for day, c in daily_counts
    ]

    return AnalyticsSummary(
        total_queries=total,
        open_queries=open_q,
        in_progress_queries=in_progress,
        resolved_queries=resolved,
        closed_queries=closed,
        total_clients=total_clients,
        total_staff=total_staff,
        total_teams=total_teams,
        avg_resolution_time_hours=avg_hours,
        queries_by_status=queries_by_status,
        queries_by_priority=queries_by_priority,
        queries_by_segment=queries_by_segment,
        staff_performance=staff_performance,
        daily_query_trend=daily_query_trend,
    )
