from pydantic import BaseModel, ConfigDict
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Findings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    issue_type:str

    category: str
    severity: Severity
    line: int
    issues: list[str]
    suggestion: str 


class CodeReviewReport(BaseModel):
    file_name:str
    model_config = ConfigDict(extra="forbid")

    overall_status: str
    summary: str
    findings: list[Findings]

