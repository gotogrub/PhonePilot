# Scenarios Guide

Scenarios let you record, save, and replay sequences of actions on your Android device.

## Creating a Scenario

### Via API

```bash
curl -X POST http://localhost:8000/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "morning_routine",
    "description": "Check weather and calendar every morning",
    "steps": [
      {"action": "open", "target": "com.weather.app"},
      {"action": "wait", "wait": 2.0},
      {"action": "tap", "target": "today_forecast", "value": "540,800"},
      {"action": "open", "target": "com.google.calendar"},
      {"action": "wait", "wait": 1.0}
    ]
  }'
```

### Via UI

1. Open the Scenario Editor in the web interface
2. Name your scenario
3. Add steps using the visual builder
4. Save

## Step Types

| Action | Description | Parameters |
|--------|-------------|------------|
| `tap` | Tap screen coordinates | `value`: "x,y" |
| `swipe` | Swipe in a direction | `value`: direction (up/down/left/right) |
| `type` | Input text | `value`: text to type |
| `open` | Open an app | `target`: package name or app name |
| `wait` | Pause execution | `wait`: seconds |
| `back` | Press back button | — |
| `home` | Press home button | — |

## Conditional Steps

Scenarios support conditions that check screen state before executing:

```json
{
  "action": "tap",
  "target": "confirm_button",
  "value": "540,1200",
  "condition": "screen_contains:Are you sure?"
}
```

The step only executes if the condition is met.

## Scheduling

Scenarios can be scheduled to run automatically:

```json
{
  "name": "daily_backup",
  "schedule": "0 2 * * *",
  "steps": [...]
}
```

The `schedule` field uses cron syntax.

## Managing Scenarios

```bash
# List all
curl http://localhost:8000/scenarios

# Get one
curl http://localhost:8000/scenarios/morning_routine

# Update
curl -X PUT http://localhost:8000/scenarios/morning_routine \
  -H "Content-Type: application/json" \
  -d '{"name": "morning_routine", "steps": [...]}'

# Delete
curl -X DELETE http://localhost:8000/scenarios/morning_routine

# Run
curl -X POST http://localhost:8000/scenarios/morning_routine/run
```

## Example Scenarios

### Send Daily Message

```json
{
  "name": "send_good_morning",
  "steps": [
    {"action": "open", "target": "org.telegram.messenger"},
    {"action": "wait", "wait": 2.0},
    {"action": "tap", "value": "540,300"},
    {"action": "type", "value": "Good morning!"},
    {"action": "tap", "target": "send_button"}
  ]
}
```

### Clear Notifications

```json
{
  "name": "clear_notifications",
  "steps": [
    {"action": "swipe", "value": "down"},
    {"action": "wait", "wait": 0.5},
    {"action": "tap", "target": "clear_all"}
  ]
}
```
