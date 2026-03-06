# Traffic Light Template Orchestration - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Concepts](#concepts)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Templates](#templates)
6. [API Reference](#api-reference)
7. [CLI Usage](#cli-usage)
8. [Integration Examples](#integration-examples)
9. [Best Practices](#best-practices)

## Overview

The Traffic Light Template Orchestration system provides a standardized, visual way to track work status using the familiar traffic light metaphor:

- 🔴 **RedLight**: Critical issues, blockers, failures requiring immediate action
- 🟡 **YellowLight**: In progress, warnings, situations needing monitoring
- 🟢 **GreenLight**: Success, completion, approval to proceed

This system integrates seamlessly with the existing BlackRoad Prism orchestrator and bot framework.

## Concepts

### Status Levels

**RedLight (🔴)** - Critical States
- Deployment failures
- Critical blockers
- Security vulnerabilities
- Production outages
- Data integrity issues

**YellowLight (🟡)** - Warning States
- Work in progress
- Performance warnings
- Resource constraints
- Pending approvals
- Minor issues

**GreenLight (🟢)** - Success States
- Completed work
- All tests passing
- Approvals granted
- Ready for production
- Deployments successful

### Status Meters

Visual progress indicators using emoji:

```
🔴🔴🔴🔴🔴 - Critical severity level 5
🔴🔴🔴🔴⚪️ - High severity level 4
🔴🔴🔴⚪️⚪️ - Medium severity level 3
🔴🔴⚪️⚪️⚪️ - Low severity level 2
🔴⚪️⚪️⚪️⚪️ - Minimal severity level 1
```

Same pattern applies to YELLOW and GREEN statuses.

### Criteria-Based Routing

The system automatically routes to the appropriate template based on criteria:

**Priority Order:**
1. RED criteria (highest priority)
2. YELLOW criteria (medium priority)
3. GREEN criteria (default if no issues)

## Installation

The traffic light system is part of the BlackRoad Prism orchestrator:

```bash
# Already installed with the orchestrator
cd /path/to/blackroad-os-prism-enterprise

# Verify installation
python -c "from orchestrator.traffic_light import get_orchestrator; print('✅ Installed')"
```

## Quick Start

### Python API

```python
from orchestrator.traffic_light import get_orchestrator, LightStatus

# Get orchestrator instance
orchestrator = get_orchestrator()

# Select a template by status and name
template = orchestrator.select_template(LightStatus.RED, "blocked_task")

# Route based on criteria
criteria = ["Critical blocker identified", "Dependencies unavailable"]
template = orchestrator.route_by_criteria(criteria)

# Render status meter
meter = orchestrator.render_status_meter(LightStatus.YELLOW, level=3)
print(meter)  # 🟡🟡🟡⚪️⚪️

# Get summary
summary = orchestrator.get_status_summary()
print(summary)  # {'red': 2, 'yellow': 2, 'green': 2}
```

### CLI Usage

```bash
# List all templates
brc traffic-light list

# List templates by status
brc traffic-light list --status red

# Select a specific template
brc traffic-light select --status green --name completed

# Route by criteria
brc traffic-light route \
  --criteria "Critical blocker identified" \
  --criteria "System failure"

# Render status meter
brc traffic-light meter --status yellow --level 4

# Show summary
brc traffic-light summary
```

## Templates

### RedLight Templates

#### 1. blocked_task
**Use when:** Critical blocker prevents progress  
**File:** `templates/traffic_light/redlight_blocked.md`  
**Criteria:**
- Critical blocker identified
- Dependencies unavailable
- Security vulnerability detected
- System failure or outage

**Sections:**
- Blocker details
- Impact assessment
- Diagnosis checklist
- Immediate actions
- Unblocking plan
- Status updates
- Resolution criteria

#### 2. failed_deployment
**Use when:** Deployment fails and needs rollback  
**File:** `templates/traffic_light/redlight_failed_deploy.md`  
**Criteria:**
- Deployment failed validation
- Breaking changes detected
- Rollback required

**Sections:**
- Failure summary
- Impact assessment
- Failure details
- Rollback decision
- Live status updates
- Diagnostics checklist
- Recovery plan

### YellowLight Templates

#### 1. in_progress
**Use when:** Task is actively being worked on  
**File:** `templates/traffic_light/yellowlight_progress.md`  
**Criteria:**
- Task is actively being worked on
- Partial completion
- Waiting for review or approval
- Minor issues detected

**Sections:**
- Work summary
- Progress tracking
- Status details
- Health check
- Warnings & concerns
- Next steps
- Collaboration needs

#### 2. warning_state
**Use when:** System metrics show warnings  
**File:** `templates/traffic_light/yellowlight_warning.md`  
**Criteria:**
- Performance degradation
- Approaching resource limits
- Non-critical issues found

**Sections:**
- Warning summary
- Metrics monitoring
- Investigation
- Action plan
- Escalation thresholds
- Impact analysis

### GreenLight Templates

#### 1. completed
**Use when:** All work is done and verified  
**File:** `templates/traffic_light/greenlight_complete.md`  
**Criteria:**
- All checks passed
- Deployment successful
- Tests passing
- Ready to proceed

**Sections:**
- Completion summary
- Success criteria
- Verification checklist
- Deployment details
- Documentation
- Learnings

#### 2. approved
**Use when:** Work is reviewed and approved  
**File:** `templates/traffic_light/greenlight_approved.md`  
**Criteria:**
- Code review approved
- Security scan passed
- Quality gates met

**Sections:**
- Approval summary
- Review results
- Quality gates
- Sign-offs
- Next stage authorization
- Compliance

## API Reference

### TrafficLightOrchestrator

Main class for template orchestration.

**Methods:**

```python
def __init__(self, templates_dir: Optional[Path] = None)
    """Initialize the orchestrator."""

def register_template(self, template: TrafficLightTemplate)
    """Register a new template."""

def get_templates(self, status: LightStatus) -> List[TrafficLightTemplate]
    """Get all templates for a status."""

def select_template(
    self, 
    status: LightStatus, 
    name: Optional[str] = None
) -> Optional[TrafficLightTemplate]
    """Select a template by status and optional name."""

def route_by_criteria(
    self, 
    criteria_met: List[str]
) -> Optional[TrafficLightTemplate]
    """Route to template based on criteria."""

def get_status_summary(self) -> Dict[str, int]
    """Get count of templates by status."""

def render_status_meter(
    self, 
    status: LightStatus, 
    level: int = 3
) -> str
    """Render emoji-based status meter."""
```

### LightStatus Enum

```python
class LightStatus(str, Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
```

### TrafficLightTemplate Dataclass

```python
@dataclass
class TrafficLightTemplate:
    name: str
    status: LightStatus
    template_path: Path
    description: str
    emoji: str
    criteria: List[str]
```

## CLI Usage

### Command Reference

#### list
List available templates.

```bash
# List all templates
brc traffic-light list

# Filter by status
brc traffic-light list --status red
brc traffic-light list -s yellow
```

#### select
Select and output a specific template.

```bash
# By status and name
brc traffic-light select --status red --name blocked_task

# Output to file
brc traffic-light select -s green -n completed -o /tmp/output.md

# First template for status (no name)
brc traffic-light select --status yellow
```

#### route
Route to appropriate template based on criteria.

```bash
# Single criterion
brc traffic-light route --criteria "Critical blocker identified"

# Multiple criteria
brc traffic-light route \
  -c "Critical blocker identified" \
  -c "System failure" \
  -c "Dependencies unavailable"

# Output to file
brc traffic-light route -c "Tests passing" -o /tmp/result.md
```

#### summary
Show summary of available templates.

```bash
brc traffic-light summary
```

#### meter
Render a status meter.

```bash
# Default level (3)
brc traffic-light meter --status red

# Custom level
brc traffic-light meter -s yellow -l 4
```

#### info
Show detailed information about a template.

```bash
brc traffic-light info --status red --name blocked_task
brc traffic-light info -s green -n approved
```

#### register
Register a custom template.

```bash
brc traffic-light register \
  --name custom_security \
  --status red \
  --path templates/custom.md \
  --description "Custom security template" \
  --criteria "Security issue" \
  --criteria "CVE detected"
```

## Integration Examples

### With Bot Orchestrator

```python
from orchestrator.traffic_light import get_orchestrator, LightStatus
from orchestrator.orchestrator import route

# Route task to bot
response = route(task, "Treasury-BOT")

# Determine traffic light status
if response.risks and any("critical" in r.lower() for r in response.risks):
    status = LightStatus.RED
elif response.elapsed_ms and response.elapsed_ms > response.p95_target:
    status = LightStatus.YELLOW
else:
    status = LightStatus.GREEN

# Get appropriate template
template = get_orchestrator().select_template(status)
```

### With GitHub Actions

`.github/workflows/traffic-light.yml`:

```yaml
name: Traffic Light Status
on:
  issues:
    types: [labeled]

jobs:
  apply-template:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Apply Template
        run: |
          case "${{ github.event.label.name }}" in
            blocked)
              brc traffic-light select -s red -n blocked_task
              ;;
            in-progress)
              brc traffic-light select -s yellow -n in_progress
              ;;
            approved)
              brc traffic-light select -s green -n approved
              ;;
          esac
```

### With ClickUp

Automation rules:
- **Status → Blocked**: Apply RedLight template + notify
- **Status → In Progress**: Apply YellowLight template + start timer
- **Status → Complete**: Apply GreenLight template + close

### With Slack

Slash commands:
```
/traffic-light red blocked_task
/traffic-light yellow warning_state
/traffic-light green completed
```

## Best Practices

### 1. Use RedLight Sparingly
Only use RED status for truly critical issues that require immediate attention.

### 2. Update YellowLight Regularly
Keep in-progress statuses current so stakeholders know what's happening.

### 3. Celebrate GreenLight
Make completions visible to recognize achievements.

### 4. Automate Transitions
Use CI/CD, webhooks, and triggers to update status automatically.

### 5. Document Criteria
Make routing rules explicit so everyone knows what triggers each status.

### 6. Monitor Patterns
Track how often each status is used to identify systemic issues.

### 7. Customize Templates
Add organization-specific sections to templates as needed.

### 8. Maintain Consistency
Use the same status meanings across all projects and teams.

## Examples

See `examples/traffic_light_examples.py` for comprehensive examples including:
- Basic usage
- Criteria-based routing
- Status meter rendering
- Custom template registration
- Real-world integration scenarios

Run examples:
```bash
python examples/traffic_light_examples.py
```

## Support

For questions or issues:
- Create an issue with label `traffic-light`
- Contact DevOps in #ops-support
- See main orchestrator docs

## Version History

- **1.0.0** (2025-12-24): Initial release
  - Core orchestration engine
  - 6 default templates (2 per status)
  - CLI commands
  - Integration hooks
  - Full documentation

---

**Maintainer:** BlackRoad OS Team  
**License:** See LICENSE file  
**Repository:** BlackRoad-OS/blackroad-os-prism-enterprise
