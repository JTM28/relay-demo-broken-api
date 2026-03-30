from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache

from app.config import get_settings
from models.agent import AgentProfile
from models.common import CheckpointStatus, Priority, SessionStatus, WorkItemStatus
from models.item import WorkItem
from models.session import NegotiationSession, ProposalPosition, SessionCheckpoint


@dataclass(frozen=True, slots=True)
class DemoState:
    items: dict[str, WorkItem]
    agents: dict[str, AgentProfile]
    sessions: dict[str, NegotiationSession]
    seed_version: str


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(UTC)


@lru_cache
def get_demo_state() -> DemoState:
    settings = get_settings()

    agents = {
        "agt_orchid": AgentProfile(
            id="agt_orchid",
            display_name="Orchid",
            owner="alex",
            specialty="coordination",
            focus_summary="Keeps cross-agent execution aligned when requirements are still moving.",
            strengths=("handoff design", "risk framing", "status clarity"),
            labels=("facilitator", "delivery"),
            active_item_ids=("itm_release-brief", "itm_storage-decision"),
            availability_note="Prefers small review loops and explicit checkpoints.",
            updated_at=_dt("2026-03-29T14:00:00+00:00"),
        ),
        "agt_nova": AgentProfile(
            id="agt_nova",
            display_name="Nova",
            owner="sam",
            specialty="backend",
            focus_summary="Builds service boundaries and pushes for operationally calm defaults.",
            strengths=("service design", "runtime simplicity", "incident response"),
            labels=("backend", "operations"),
            active_item_ids=("itm_agent-roster", "itm_storage-decision"),
            availability_note="Favors contained change sets and strong failure signals.",
            updated_at=_dt("2026-03-29T14:05:00+00:00"),
        ),
        "agt_harbor": AgentProfile(
            id="agt_harbor",
            display_name="Harbor",
            owner="jules",
            specialty="platform",
            focus_summary="Optimizes for change management and how new behavior gets rolled out.",
            strengths=("release planning", "platform conventions", "migration sequencing"),
            labels=("platform", "migration"),
            active_item_ids=("itm_contract-pass", "itm_release-brief"),
            availability_note="Wants extension seams to stay open until workload evidence arrives.",
            updated_at=_dt("2026-03-29T14:10:00+00:00"),
        ),
        "agt_rune": AgentProfile(
            id="agt_rune",
            display_name="Rune",
            owner="mika",
            specialty="analysis",
            focus_summary="Turns ambiguous proposals into comparable tradeoff summaries.",
            strengths=("option scoring", "decision notes", "ambiguity reduction"),
            labels=("analysis", "decision-support"),
            active_item_ids=("itm_conflict-lab", "itm_storage-decision"),
            availability_note="Prefers explicit assumptions and a visible decision lens.",
            updated_at=_dt("2026-03-29T14:20:00+00:00"),
        ),
    }

    items = {
        "itm_storage-decision": WorkItem(
            id="itm_storage-decision",
            title="Prepare the persistence hand-off point",
            summary="Keep the live API believable while leaving storage implementation fully open for later agent experiments.",
            priority=Priority.HIGH,
            status=WorkItemStatus.IN_PROGRESS,
            target_outcome="A realistic service boundary that can later branch toward different persistence designs without changing public contracts.",
            open_questions=(
                "Which access patterns deserve first-class optimization?",
                "How much shape drift should future records tolerate?",
                "What runtime guarantees matter most once writes are introduced?",
            ),
            labels=("storage-neutral", "hand-off", "api"),
            active_agent_ids=("agt_orchid", "agt_nova", "agt_rune"),
            active_session_ids=("ses_storage-path",),
            updated_at=_dt("2026-03-29T16:00:00+00:00"),
        ),
        "itm_conflict-lab": WorkItem(
            id="itm_conflict-lab",
            title="Create a believable conflict-resolution sandbox",
            summary="Expose enough moving parts that future agents can disagree in meaningful ways without needing real production dependencies.",
            priority=Priority.HIGH,
            status=WorkItemStatus.READY,
            target_outcome="An end-to-end demo flow with seeded agents, active items, and negotiation sessions.",
            open_questions=(
                "How much realism is enough before the demo becomes costly to maintain?",
                "Which entities should remain domain-level only until storage exists?",
            ),
            labels=("demo", "negotiation", "testing"),
            active_agent_ids=("agt_rune", "agt_harbor"),
            active_session_ids=("ses_conflict-lab",),
            updated_at=_dt("2026-03-29T16:15:00+00:00"),
        ),
        "itm_release-brief": WorkItem(
            id="itm_release-brief",
            title="Publish a team-facing handoff brief",
            summary="Document how the service is structured today and where future agents are expected to extend it.",
            priority=Priority.MEDIUM,
            status=WorkItemStatus.IN_PROGRESS,
            target_outcome="A concise README plus focused notes that explain the neutral contract boundary.",
            open_questions=("Which examples help future agents extend the service fastest?",),
            labels=("docs", "handoff"),
            active_agent_ids=("agt_orchid", "agt_harbor"),
            active_session_ids=(),
            updated_at=_dt("2026-03-29T15:40:00+00:00"),
        ),
        "itm_agent-roster": WorkItem(
            id="itm_agent-roster",
            title="Model active agent roster and responsibilities",
            summary="Represent who is involved, what they own, and how their current focus overlaps.",
            priority=Priority.MEDIUM,
            status=WorkItemStatus.READY,
            target_outcome="A storage-neutral roster surface that can be backed by multiple persistence styles later.",
            open_questions=("Which ownership signals need stronger typing once persistence is added?",),
            labels=("agents", "ownership"),
            active_agent_ids=("agt_nova",),
            active_session_ids=(),
            updated_at=_dt("2026-03-29T15:05:00+00:00"),
        ),
        "itm_contract-pass": WorkItem(
            id="itm_contract-pass",
            title="Run a contract neutrality pass",
            summary="Review every public contract to make sure it does not imply a preferred storage model.",
            priority=Priority.MEDIUM,
            status=WorkItemStatus.IN_PROGRESS,
            target_outcome="A contract set that can survive either relational or document-oriented persistence work later.",
            open_questions=(
                "Which fields should remain opaque identifiers instead of semantic keys?",
                "Which nested shapes are intrinsic to the API and which should be flattened later by storage adapters?",
            ),
            labels=("contracts", "neutrality", "handoff"),
            active_agent_ids=("agt_harbor", "agt_orchid"),
            active_session_ids=(),
            updated_at=_dt("2026-03-29T15:22:00+00:00"),
        ),
    }

    sessions = {
        "ses_storage-path": NegotiationSession(
            id="ses_storage-path",
            item_id="itm_storage-decision",
            title="Choose the right hand-off posture before persistence",
            summary="The team wants enough structure to feel real without steering later agents toward a specific storage backend.",
            status=SessionStatus.ACTIVE,
            participant_ids=("agt_orchid", "agt_nova", "agt_rune"),
            checkpoints=(
                SessionCheckpoint(
                    label="Contract boundary agreed",
                    status=CheckpointStatus.COMPLETE,
                    note="Public contracts stay in contracts/ and remain storage-neutral.",
                ),
                SessionCheckpoint(
                    label="Persistence schema deferred",
                    status=CheckpointStatus.ACTIVE,
                    note="schemas/ is intentionally reserved for later agent-specific storage work.",
                ),
                SessionCheckpoint(
                    label="Scoring lens captured",
                    status=CheckpointStatus.PENDING,
                    note="Comparison endpoint should explain tradeoffs without assuming a winning storage style.",
                ),
            ),
            positions=(
                ProposalPosition(
                    id="pos_contract-first",
                    label="Contract-first expansion",
                    proposed_by="agt_orchid",
                    summary="Build realistic routes and service behaviors while keeping storage concerns behind a future seam.",
                    strengths=("Stable HTTP surface", "Easy branch point for future agents", "Lower coordination cost today"),
                    risks=("Some internal abstractions may need rework later", "No real persistence feedback yet"),
                    assumptions=("Early experiments care more about agent behavior than write throughput",),
                    consequence_profile=("Public shape hardens early", "Storage work happens in a later pass"),
                ),
                ProposalPosition(
                    id="pos_domain-heavy",
                    label="Domain-heavy foundation",
                    proposed_by="agt_nova",
                    summary="Model richer coordination concepts now so later persistence work has more concrete semantics to target.",
                    strengths=("Better realism", "More meaningful conflict prompts", "Clearer service responsibilities"),
                    risks=("Higher upfront complexity", "Can accidentally imply storage structure"),
                    assumptions=("The demo needs enough moving parts to trigger real disagreement",),
                    consequence_profile=("More code today", "Still avoids persistence wiring"),
                ),
            ),
            next_action="Expand the API to show richer coordination flow while keeping contracts free of storage-specific assumptions.",
            updated_at=_dt("2026-03-29T16:30:00+00:00"),
        ),
        "ses_conflict-lab": NegotiationSession(
            id="ses_conflict-lab",
            item_id="itm_conflict-lab",
            title="Tune the sandbox for divergent implementation prompts",
            summary="Make the repo realistic enough that separate agents can head in different directions and still negotiate back together.",
            status=SessionStatus.ACTIVE,
            participant_ids=("agt_harbor", "agt_rune"),
            checkpoints=(
                SessionCheckpoint(
                    label="Seed entities feel real",
                    status=CheckpointStatus.ACTIVE,
                    note="The service already exposes items, agents, and sessions that look production-adjacent.",
                ),
                SessionCheckpoint(
                    label="Storage language stays neutral",
                    status=CheckpointStatus.ACTIVE,
                    note="Avoid tables, collections, joins, or document-specific wording in public contracts.",
                ),
            ),
            positions=(
                ProposalPosition(
                    id="pos_more-endpoints",
                    label="Broaden the API surface",
                    proposed_by="agt_harbor",
                    summary="Introduce more routes and filters before any persistence work so future branches operate inside a richer app.",
                    strengths=("Feels more real", "Raises integration complexity", "Improves docs and test value"),
                    risks=("More code to reconcile later",),
                    assumptions=("A larger surface creates better negotiation opportunities",),
                    consequence_profile=("Better sandbox", "Higher maintenance"),
                ),
                ProposalPosition(
                    id="pos_decision-tooling",
                    label="Add comparison tooling",
                    proposed_by="agt_rune",
                    summary="Let the service compare competing proposals in a deterministic way using neutral evaluation inputs.",
                    strengths=("Useful immediately", "Reinforces decision workflow", "Does not require persistence"),
                    risks=("Scoring can look arbitrary if not documented",),
                    assumptions=("Visible tradeoff framing matters more than perfect scoring",),
                    consequence_profile=("Richer session flow", "Clear extension seam"),
                ),
            ),
            next_action="Add a comparison route that accepts two proposals and returns a neutral recommendation summary.",
            updated_at=_dt("2026-03-29T16:45:00+00:00"),
        ),
    }

    return DemoState(items=items, agents=agents, sessions=sessions, seed_version=settings.seed_version)
