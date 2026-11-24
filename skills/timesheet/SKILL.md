---
name: timesheet
description: Use when asked to log time, fill in or check a timesheet, or record work or meetings in Productive.
---

# Timesheet

Use the Productive app in Executor, and read the app's own skill before the first call. It covers the API's fields, filters, and lookups. This skill covers how the user wants time logged.

## Authority

A request to log time authorises creating the user's time entries and updating the user's unapproved entries for the dates in the request. Deleting, submitting, or approving entries, and changing approved entries or anyone else's, each need their own request.

## Gather the work

1. Resolve each date in the user's timezone, not UTC, and find the user's person record.
2. Read the user's existing entries for those dates, including their notes, services, start times, approval state, and calendar event IDs.
3. For each meeting, keep any start, end, or duration the user gave, and fill the rest from the calendar. "Meetings I had" means events the user accepted that have ended, not declined, all-day, focus, working-location, or personal events. Ask when no event matches or several do.
4. For each Jira issue involved, read only its summary, project, and parent epic with "jira".
5. Choose a service for each piece of work, as below.
6. Ask in one question for the time spent on each piece of non-meeting work the user gave no duration for, showing the service you propose for it, along with any other question this skill raises. Never estimate a duration.

## Choose the service

- **Precedent picks the budget.** Look for the user's entries from the last month for the same issue, its epic, or the same client and stream of work, reading only the fields you need. The issue's project, epic, and scope point to that stream of work. Treat Productive's service suggestions as candidates to check against the work, not answers.
- **The user's role picks the service within it.** When that budget offers a service for the user's role, such as Lead Developer, use it. Otherwise use the service the user's comparable work in that budget used. The same service name recurs across budgets at different rates, so always use the chosen budget's service ID.
- **Only live services.** Consider services the user can track time on, with time tracking enabled, on open budgets, and ignore any marked as no longer used.
- **Ask when precedent doesn't decide.** When two budgets, or two services within one budget, fit equally well, ask instead of guessing, and recommend one with your reason.

## Write the entries

- **One entry per service per day.** Put each piece of work in a bullet. When an unapproved, non-meeting entry for that service and day already exists, update it: add the minutes, append the bullets it doesn't carry, and send the whole note. When its note isn't a list, turn the existing text into the first bullet.
- **Check for work already logged.** When an existing bullet already covers the same issue or work, ask whether the new time is already in that entry's total or extra. Add extra time without repeating the bullet.
- **Meetings stand alone.** Give each meeting its own entry with its date, its start time with the timezone offset, its duration, and its calendar event ID when there is one. Its note is one bullet: `Meeting:` and the calendar title or a short description. Before creating one, match it against the day's existing entries by calendar event ID, then by start time in the user's timezone, duration, and a similar title, and skip it when it's already logged.
- **Notes are HTML bullet lists.** Write `<ul><li><p>…</p></li></ul>`, one past-tense sentence per item, describing what the user said they did. When they gave only an issue, write "Worked on" and the issue's summary instead of claiming an outcome. When an item belongs to a Jira issue, start it with the key linked to the issue: `<a href="https://<site>/browse/ABC-123" target="_blank">ABC-123</a>: Upgraded the API to Node.js 26.`

When a write's outcome is unclear, read the day's entries again before retrying. Read back each entry you wrote with its service, budget, and project included. Report a table with the date, start and end times for meetings, minutes, project, service, and note text, and flag any entry whose readback doesn't match what you sent.
