{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## Site Map\
\
Top-level pages only.\
\
- Homepage\
- Sign in / Sign up\
- Onboarding\
- Ranked Jobs\
- Job Detail\
- Preferences\
- Digest Preview\
- Digest History\
- Account / Privacy\
\
---\
\
## Purpose of Each Page\
\
### Homepage\
\
Purpose:\
- explain JobSignal in one sentence\
- help users connect Gmail\
- let visitors preview the digest experience\
\
### Sign in / Sign up\
\
Purpose:\
- create or access an account\
- support email/password or Google sign-in\
- route Gmail-based users into onboarding\
\
### Onboarding\
\
Purpose:\
- connect Gmail\
- collect job preferences\
- set digest schedule\
- confirm how JobSignal will work\
\
### Ranked Jobs\
\
Purpose:\
- show the user\'92s clean, deduplicated, ranked job list\
- act like the core inbox-style workspace\
\
### Job Detail\
\
Purpose:\
- show parsed job details\
- explain why the role ranked where it did\
- let users take simple status actions\
\
### Preferences\
\
Purpose:\
- let users edit filtering and ranking criteria\
- manage digest timing\
- manage source settings\
\
### Digest Preview\
\
Purpose:\
- show the exact digest format the user will receive\
- build trust in the daily summary\
\
### Digest History\
\
Purpose:\
- archive past digests\
- let users revisit missed roles without clutter\
\
### Account / Privacy\
\
Purpose:\
- manage account settings\
- review Gmail connection status\
- explain scan scope and data handling\
- support disconnect or deletion flows\
\
---\
\
## User Roles and Access Levels\
\
### Visitor\
\
Can:\
- view homepage\
- preview product value\
- start signup or sign-in flow\
\
Cannot:\
- connect Gmail\
- view jobs\
- edit preferences\
- access digests\
\
### Authenticated User\
\
Can:\
- complete onboarding\
- connect Gmail\
- edit job preferences\
- view ranked jobs\
- open job details\
- save, dismiss, apply, or hide roles\
- preview digests\
- access digest history\
- manage account and privacy settings\
\
Cannot:\
- access another user\'92s data\
- view internal parsing logs\
- change system-level settings\
\
### System Role: Scheduled Workflow\
\
This is not a human user, but it is an important product role.\
\
Can:\
- process newly ingested job emails\
- deduplicate job records\
- rank jobs against user preferences\
- assemble daily digests\
- trigger digest sending\
- write digest history and delivery status\
\
Cannot:\
- bypass data protections beyond approved backend logic\
- expose internal logic directly to users\
\
### System Role: Admin / Internal Operator\
\
Internal only.\
\
Can:\
- monitor workflow health\
- review parse failures\
- inspect send failures\
- support debugging and reliability work\
\
Should not:\
- manually change user-facing rankings without traceability\
- access user data outside approved support and operations policies\
\
---\
\
## Primary User Journeys\
\
Keep each journey to 3 steps max.\
\
### Journey 1: First-time setup\
\
1. User lands on Homepage and clicks **Connect inbox**\
2. User signs in, connects Gmail, and sets job preferences\
3. User confirms digest schedule and enters Ranked Jobs\
\
### Journey 2: Review today\'92s best roles\
\
1. User opens Ranked Jobs\
2. User scans the list and selects a role\
3. User opens Job Detail and marks it saved, dismissed, or applied\
\
### Journey 3: Adjust ranking logic\
\
1. User opens Preferences\
2. User edits criteria or weighting\
3. User saves changes and returns to Ranked Jobs\
\
### Journey 4: Check why a job appeared\
\
1. User selects a role from Ranked Jobs\
2. User opens Job Detail\
3. User reads the plain-language ranking explanation and source link\
\
### Journey 5: Preview the daily digest\
\
1. User opens Digest Preview\
2. User reviews Top matches, Worth considering, and New today\
3. User returns to Preferences if they want to refine results\
\
### Journey 6: Revisit a past digest\
\
1. User opens Digest History\
2. User selects a previous digest\
3. User reviews the included roles and opens a Job Detail page\
\
### Journey 7: Recover from a mistaken action\
\
1. User dismisses or hides a role\
2. User sees a calm confirmation with undo\
3. User restores the role if the action was accidental\
\
### Journey 8: Manage trust and privacy\
\
1. User opens Account / Privacy\
2. User reviews Gmail connection and data settings\
3. User disconnects Gmail or requests account deletion if needed\
\
---\
\
## Page-Level Flow Notes\
\
### Homepage \uc0\u8594  Sign in / Sign up \u8594  Onboarding\
\
This should feel like one continuous path.\
\
Rules:\
- no detours\
- no extra feature tours\
- no crowded marketing sections\
- keep the main action obvious\
\
### Onboarding \uc0\u8594  Ranked Jobs\
\
The transition should feel immediate and reassuring.\
\
The user should leave onboarding with:\
- connected inbox\
- saved preferences\
- a clear understanding of digest timing\
\
### Ranked Jobs \uc0\u8596  Job Detail\
\
This is the core product loop.\
\
Rules:\
- moving from list to detail should feel fast\
- the user should always know how to return to the list\
- status changes should reflect clearly in both places\
\
### Preferences \uc0\u8596  Ranked Jobs\
\
This loop supports trust.\
\
Rules:\
- preference changes should feel understandable\
- updated logic should be summarized in plain language\
- users should feel in control of results\
\
### Digest Preview / Digest History \uc0\u8596  Job Detail\
\
Digest pages should act like alternate entry points into the same calm job review flow.\
\
Rules:\
- use the same job language\
- use the same labels\
- preserve list/detail consistency\
\
---\
\
## Access Rules by Page\
\
### Public pages\
\
- Homepage\
- Sign in / Sign up\
\
### Protected pages\
\
- Onboarding\
- Ranked Jobs\
- Job Detail\
- Preferences\
- Digest Preview\
- Digest History\
- Account / Privacy\
\
### Conditional access\
\
#### Ranked Jobs\
Accessible after authentication.\
Most useful after onboarding is complete.\
\
#### Job Detail\
Accessible only for jobs associated with the signed-in user.\
\
#### Digest Preview\
Accessible after preferences are saved.\
\
#### Digest History\
Accessible after at least one digest exists, otherwise show a patient empty state.\
\
---\
\
## Navigation Model\
\
Keep navigation quiet and minimal.\
\
Primary authenticated navigation:\
- Ranked Jobs\
- Digest Preview\
- Digest History\
- Preferences\
- Account\
\
Rules:\
- keep top-level navigation short\
- do not expose internal workflow concepts\
- avoid clutter from future sources before they exist\
- keep \'93Ranked Jobs\'94 as the obvious home inside the product\
\
---\
\
## Empty State Logic\
\
### Ranked Jobs empty state\
\
Use when:\
- no parsed roles yet\
- no ranked roles yet\
- no strong matches yet\
\
Tone:\
- calm\
- patient\
- informative\
\
Example:\
- \'93No strong matches today.\'94\
\
### Digest History empty state\
\
Use when:\
- no digests have been sent yet\
\
Example:\
- \'93Your first digest will appear here after new job alerts are processed.\'94\
\
### Preferences empty or incomplete state\
\
Use when:\
- onboarding is unfinished\
- required fields are missing\
\
Example:\
- \'93Finish your preferences to start ranking jobs.\'94\
\
---\
\
## Status Model Across Pages\
\
User-visible statuses should stay consistent everywhere.\
\
### Job match labels\
\
- Top match\
- Good fit\
- Lower priority\
\
### User job statuses\
\
- New\
- Saved\
- Dismissed\
- Applied\
- Hidden\
\
### Digest statuses\
\
- Scheduled\
- Sent\
- Failed\
\
Rules:\
- use the same wording in list, detail, and digest views\
- never rename the same concept on different pages\
- never rely on color alone to distinguish status\
\
---\
\
## Future Role Expansion\
\
Not in MVP, but the structure should allow later roles such as:\
- career coach or advisor\
- team admin for managed job search support\
- recruiter-block or source moderation tools\
- analytics-only operator views\
\
For now, keep the product single-user and personal.\
\
That supports the core emotional promise:\
a quiet, trusted tool for one person\'92s job search.}