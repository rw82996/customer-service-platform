import enum


class QueryStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class QueryPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StaffRole(str, enum.Enum):
    AGENT = "agent"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"
