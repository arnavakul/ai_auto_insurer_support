from ..state.head_state import HeadState


def route_after_head(state: HeadState) -> str:
    """
    Decide which specialist should execute next.
    """

    if state.next_action == "FILE":
        return "file"

    if state.next_action == "VERIFY":
        return "verification"

    if state.next_action == "COST":
        return "cost"

    if state.next_action == "ORGANIZE":
        return "organization"

    return "end"