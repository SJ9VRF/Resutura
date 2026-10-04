from .schemas import Action, RiskLevel

HIGH_RISK = {"submit_payment", "delete_file", "send_email", "publish", "retract_publication", "overwrite_file"}
MODERATE = {"save_file", "submit_form", "rename_file", "close_tab"}


def classify_action(action: Action) -> RiskLevel:
    if action.type in HIGH_RISK: return RiskLevel.HIGH
    if action.type in MODERATE: return RiskLevel.MODERATE
    return RiskLevel.SAFE


def requires_checkpoint(action: Action) -> bool:
    return classify_action(action) in {RiskLevel.MODERATE, RiskLevel.HIGH}
