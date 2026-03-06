# Traffic Light Quick Reference

## 🚦 Status Guide

| Status | Emoji | Meaning | Use When |
|--------|-------|---------|----------|
| RED | 🔴 | Critical/Blocked | Deployment failed, blocker, security issue, outage |
| YELLOW | 🟡 | Warning/In Progress | Active work, performance warning, pending approval |
| GREEN | 🟢 | Success/Complete | Tests pass, approved, deployed, complete |

## 📊 Status Meters

```
Level 1: 🔴⚪️⚪️⚪️⚪️   Minimal
Level 2: 🔴🔴⚪️⚪️⚪️   Low
Level 3: 🔴🔴🔴⚪️⚪️   Medium
Level 4: 🔴🔴🔴🔴⚪️   High
Level 5: 🔴🔴🔴🔴🔴   Critical/Complete
```

## 🎯 Quick Commands

### CLI
```bash
# List all templates
brc traffic-light list

# Select template
brc traffic-light select -s red -n blocked_task

# Route by criteria
brc traffic-light route -c "Critical blocker identified"

# Show summary
brc traffic-light summary

# Render meter
brc traffic-light meter -s yellow -l 3
```

### Python
```python
from orchestrator.traffic_light import get_orchestrator, LightStatus

o = get_orchestrator()

# Select template
t = o.select_template(LightStatus.RED, "blocked_task")

# Route by criteria
t = o.route_by_criteria(["Critical blocker identified"])

# Render meter
m = o.render_status_meter(LightStatus.YELLOW, 3)
```

## 📋 Templates

### RED (🔴) Templates
- **blocked_task** - Critical blocker preventing progress
- **failed_deployment** - Deployment failure requiring rollback

### YELLOW (🟡) Templates
- **in_progress** - Active work being done
- **warning_state** - Performance/resource warning

### GREEN (🟢) Templates
- **completed** - Task successfully completed
- **approved** - Work reviewed and approved

## 🔀 Routing Priority

```
1. RED    (Highest - Critical issues)
2. YELLOW (Medium - Warnings)
3. GREEN  (Default - Success)
```

## 🎨 Common Criteria

### RED Criteria
- "Critical blocker identified"
- "Dependencies unavailable"
- "Security vulnerability detected"
- "System failure or outage"
- "Deployment failed validation"
- "Breaking changes detected"

### YELLOW Criteria
- "Task is actively being worked on"
- "Partial completion"
- "Waiting for review or approval"
- "Performance degradation"
- "Approaching resource limits"

### GREEN Criteria
- "All checks passed"
- "Deployment successful"
- "Tests passing"
- "Ready to proceed"
- "Code review approved"
- "Security scan passed"

## 🔗 Integration Examples

### GitHub Actions
```yaml
- name: Apply Template
  run: |
    brc traffic-light select --status red --name blocked_task
```

### ClickUp Automation
```
Status = Blocked → Apply RedLight template
Status = In Progress → Apply YellowLight template
Status = Complete → Apply GreenLight template
```

### Slack
```
/traffic-light red blocked_task
/traffic-light yellow warning_state
/traffic-light green completed
```

## 📖 Key Files

| File | Purpose |
|------|---------|
| `orchestrator/traffic_light.py` | Core orchestration engine |
| `templates/traffic_light/*.md` | Template files |
| `cli/traffic_light_cli.py` | CLI commands |
| `tests/test_traffic_light.py` | Test suite |
| `docs/TRAFFIC_LIGHT_GUIDE.md` | Full documentation |
| `examples/traffic_light_examples.py` | Usage examples |

## 💡 Best Practices

1. **RED = Critical Only** - Reserve for truly urgent issues
2. **Update YELLOW Often** - Keep progress visible
3. **Celebrate GREEN** - Mark successes clearly
4. **Automate Transitions** - Use CI/CD to update status
5. **Document Criteria** - Make routing rules explicit
6. **Monitor Patterns** - Track usage to identify issues

## 🆘 Common Tasks

### Check Status
```bash
brc traffic-light summary
```

### Apply Template to Issue
```bash
# Get template content
brc traffic-light select -s red -n blocked_task > issue_comment.md

# Post to GitHub (requires gh CLI)
gh issue comment 123 --body-file issue_comment.md
```

### Custom Template
```bash
brc traffic-light register \
  --name my_template \
  --status yellow \
  --path my_template.md \
  --description "My custom template" \
  --criteria "My condition"
```

### Get Template Info
```bash
brc traffic-light info -s red -n blocked_task
```

## 🔍 Troubleshooting

### Import Error
```python
# Make sure you're in the project directory
cd /path/to/blackroad-os-prism-enterprise
python -c "from orchestrator.traffic_light import get_orchestrator"
```

### Template Not Found
```bash
# List available templates
brc traffic-light list

# Check specific status
brc traffic-light list --status red
```

### No Match for Criteria
```bash
# Check your criteria against registered templates
brc traffic-light info -s red -n blocked_task
# Look at the "Criteria" section
```

## 📚 Learn More

- Full Guide: `docs/TRAFFIC_LIGHT_GUIDE.md`
- Architecture: `docs/traffic_light_architecture.md`
- Examples: `examples/traffic_light_examples.py`
- Tests: `tests/test_traffic_light.py`
- Templates: `templates/traffic_light/README.md`

---

**Quick Start:** `brc traffic-light list` to see all available templates  
**Support:** Create issue with label `traffic-light`  
**Version:** 1.0.0
