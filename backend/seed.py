"""Seed the database with sample data for demonstration."""

from datetime import datetime, timedelta, timezone
import random

from app.database import SessionLocal, Base, engine
from app.models.business_segment import BusinessSegment
from app.models.client import Client, ClientTeamAssignment
from app.models.query import ClientQuery, QueryResponse
from app.models.staff import Staff
from app.models.team import Team

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    # Business Segments
    segments = [
        BusinessSegment(name="Lending", description="Consumer and commercial lending products"),
        BusinessSegment(name="Payments", description="Payment processing and digital wallets"),
        BusinessSegment(name="Insurance", description="Insurance products and claims"),
        BusinessSegment(name="Wealth Management", description="Investment and advisory services"),
    ]
    db.add_all(segments)
    db.flush()

    # Teams
    teams = [
        Team(name="Lending Support", description="Handles lending-related client queries"),
        Team(name="Payments Support", description="Handles payment-related client queries"),
        Team(name="General Support", description="Handles general customer inquiries"),
        Team(name="Escalation Team", description="Handles escalated and critical queries"),
    ]
    db.add_all(teams)
    db.flush()

    # Staff
    staff_members = [
        Staff(name="Alice Johnson", email="alice@example.com", role="agent", team_id=teams[0].id),
        Staff(name="Bob Smith", email="bob@example.com", role="agent", team_id=teams[0].id),
        Staff(name="Carol White", email="carol@example.com", role="agent", team_id=teams[1].id),
        Staff(name="David Brown", email="david@example.com", role="supervisor", team_id=teams[1].id),
        Staff(name="Eve Davis", email="eve@example.com", role="agent", team_id=teams[2].id),
        Staff(name="Frank Miller", email="frank@example.com", role="agent", team_id=teams[2].id),
        Staff(name="Grace Wilson", email="grace@example.com", role="supervisor", team_id=teams[3].id),
        Staff(name="Henry Taylor", email="henry@example.com", role="admin", team_id=teams[3].id),
    ]
    db.add_all(staff_members)
    db.flush()

    # Clients
    clients = [
        Client(name="Acme Corp", email="contact@acme.com", company="Acme Corporation", phone="+1-555-0101", business_segment_id=segments[0].id),
        Client(name="TechStart Inc", email="info@techstart.com", company="TechStart Inc", phone="+1-555-0102", business_segment_id=segments[1].id),
        Client(name="Global Trading", email="support@globaltrading.com", company="Global Trading LLC", phone="+1-555-0103", business_segment_id=segments[0].id),
        Client(name="SafeGuard Insurance", email="help@safeguard.com", company="SafeGuard Insurance Co", phone="+1-555-0104", business_segment_id=segments[2].id),
        Client(name="WealthBridge", email="clients@wealthbridge.com", company="WealthBridge Advisors", phone="+1-555-0105", business_segment_id=segments[3].id),
        Client(name="PayQuick Solutions", email="support@payquick.com", company="PayQuick Solutions", phone="+1-555-0106", business_segment_id=segments[1].id),
        Client(name="HomeFirst Lending", email="info@homefirst.com", company="HomeFirst Lending", phone="+1-555-0107", business_segment_id=segments[0].id),
        Client(name="SecurePay Ltd", email="help@securepay.com", company="SecurePay Ltd", phone="+1-555-0108", business_segment_id=segments[1].id),
    ]
    db.add_all(clients)
    db.flush()

    # Client-Team Assignments
    assignments = [
        ClientTeamAssignment(client_id=clients[0].id, team_id=teams[0].id),
        ClientTeamAssignment(client_id=clients[1].id, team_id=teams[1].id),
        ClientTeamAssignment(client_id=clients[2].id, team_id=teams[0].id),
        ClientTeamAssignment(client_id=clients[3].id, team_id=teams[2].id),
        ClientTeamAssignment(client_id=clients[4].id, team_id=teams[2].id),
        ClientTeamAssignment(client_id=clients[5].id, team_id=teams[1].id),
        ClientTeamAssignment(client_id=clients[6].id, team_id=teams[0].id),
        ClientTeamAssignment(client_id=clients[7].id, team_id=teams[1].id),
    ]
    db.add_all(assignments)
    db.flush()

    # Queries
    now = datetime.now(timezone.utc)
    subjects = [
        ("Loan application status", "I submitted my loan application 5 days ago and haven't received any update.", "medium", "application"),
        ("Payment failed", "My payment of $500 failed with error code E-4012. Please help.", "high", "transaction"),
        ("Interest rate inquiry", "Can you provide details on current interest rates for a 30-year fixed mortgage?", "low", "inquiry"),
        ("Disputed transaction", "I see an unauthorized charge of $299 on my statement. Please investigate.", "critical", "dispute"),
        ("Account access issue", "I'm unable to log into my account since yesterday.", "high", "access"),
        ("Refund request", "I need a refund for the duplicate payment made on March 15.", "medium", "refund"),
        ("Insurance claim follow-up", "Following up on claim #CLM-2024-1234 submitted last week.", "medium", "claim"),
        ("Portfolio rebalancing", "I'd like to discuss rebalancing my investment portfolio.", "low", "consultation"),
        ("Late payment fee waiver", "Requesting waiver of late payment fee due to system outage.", "medium", "fee"),
        ("Card replacement", "My debit card was lost. Please issue a replacement.", "high", "card"),
        ("Loan pre-approval", "I'd like to get pre-approved for a home loan.", "medium", "application"),
        ("Wire transfer delay", "Wire transfer initiated 3 days ago still not received by beneficiary.", "high", "transaction"),
    ]

    statuses = ["open", "in_progress", "resolved", "closed"]
    queries_list = []
    for i, (subject, desc, priority, category) in enumerate(subjects):
        client = clients[i % len(clients)]
        status = statuses[i % len(statuses)]
        days_ago = random.randint(1, 20)
        created = now - timedelta(days=days_ago)
        resolved_at = None
        if status in ("resolved", "closed"):
            resolved_at = created + timedelta(hours=random.randint(2, 48))

        q = ClientQuery(
            subject=subject,
            description=desc,
            status=status,
            priority=priority,
            category=category,
            client_id=client.id,
            business_segment_id=client.business_segment_id,
            assigned_staff_id=staff_members[i % len(staff_members)].id,
            created_at=created,
            resolved_at=resolved_at,
        )
        queries_list.append(q)

    db.add_all(queries_list)
    db.flush()

    # Responses
    response_messages = [
        "Thank you for reaching out. We are looking into this.",
        "Your request has been escalated to the appropriate team.",
        "We have resolved the issue. Please confirm on your end.",
        "Could you please provide additional details?",
        "The matter has been addressed. Here is a summary of actions taken.",
    ]
    for q in queries_list:
        num_responses = random.randint(1, 3)
        for j in range(num_responses):
            resp = QueryResponse(
                message=random.choice(response_messages),
                is_internal_note=1 if j == 0 and random.random() > 0.7 else 0,
                query_id=q.id,
                staff_id=staff_members[random.randint(0, len(staff_members) - 1)].id,
            )
            db.add(resp)

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
