{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## Build Sequence\
\
### Phase 0: Product framing\
\
#### 1. Lock MVP scope\
\
Decide what is in version one.\
\
Include:\
- Gmail connection\
- LinkedIn job email detection\
- preference capture\
- job parsing\
- deduplication\
- ranking\
- ranked jobs list\
- job detail view\
- digest preview\
- digest history\
- daily or weekday digest delivery\
\
Exclude for MVP:\
- Outlook\
- multi-source parsing beyond LinkedIn\
- browser extension\
- advanced AI personalization\
- application tracking beyond simple status states\
\
#### 2. Define success criteria\
\
Set MVP targets before building.\
\
Examples:\
- user connects Gmail in under 2 minutes\
- onboarding completion above target threshold\
- digest opens show recurring usage\
- users save, dismiss, or apply from ranked jobs\
- duplicate reduction is visibly useful\
\
#### 3. Write product rules\
\
Document simple non-negotiables.\
\
Examples:\
- deduplicate before ranking\
- explain every surfaced job in plain language\
- never use chatbot-style language\
- prefer list patterns over dashboard patterns\
- every action should be reversible when practical\
\
---\
\
## Phase 1: System foundation\
\
### 4. Set up frontend workspace\
\
Create the UI app foundation with:\
- Vite\
- React\
- TypeScript\
- Tailwind CSS\
- shadcn/ui\
\
Output:\
- working app shell\
- routing structure\
- base layout primitives\
- typography and spacing tokens\
- reusable page container and list row patterns\
\
### 5. Set up Supabase project\
\
Create the backend foundation with:\
- Supabase project\
- environment variables\
- Postgres database\
- auth settings\
- row-level security rules\
- edge function structure\
- scheduled job support\
\
Output:\
- secure project baseline\
- local and hosted environment config\
- naming conventions for tables and functions\
\
### 6. Set up Resend\
\
Prepare digest delivery.\
\
Configure:\
- sending domain\
- sender identity\
- email template workflow\
- delivery logging approach\
- failure and retry plan\
\
Output:\
- test email pipeline\
- digest template baseline\
- delivery status capture\
\
---\
\
## Phase 2: Data model and backend plumbing\
\
### 7. Create database schema\
\
Create the MVP tables:\
- `users`\
- `job_preferences`\
- `ingested_job_emails`\
- `jobs`\
- `user_job_rankings`\
- `digests`\
- `digest_items`\
\
Add:\
- timestamps\
- foreign keys\
- status enums\
- indexes for lookups and scheduling\
\
Output:\
- migration files\
- schema documentation\
- seed data plan\
\
### 8. Define canonical job model\
\
Write rules for normalized job records.\
\
Normalize:\
- title\
- company\
- location\
- source URL\
- salary text and extracted salary bounds\
- first seen timestamp\
- source name\
\
Output:\
- canonical field definitions\
- normalization rules\
- fallback rules for missing fields\
\
### 9. Define deduplication rules\
\
Build a clear canonical key strategy.\
\
Use normalized:\
- title\
- company\
- location\
- source URL when available\
\
Also define:\
- duplicate tolerance rules\
- edge cases\
- tie-break behavior\
\
Example:\
- \'93Senior Product Manager\'94 and \'93Sr. Product Manager\'94 at the same company in the same location may collapse into one record.\
\
Output:\
- dedupe specification\
- test cases for duplicate scenarios\
\
### 10. Define ranking model\
\
Create a transparent scoring model.\
\
Rank by:\
- title match\
- location match\
- salary fit\
- work mode fit\
- seniority fit\
- recency\
\
Support user-adjustable weights for:\
- title relevance\
- location fit\
- salary fit\
- work mode fit\
- recency\
\
Output:\
- scoring rubric\
- label thresholds for Top match / Good fit / Lower priority\
- explanation templates in plain language\
\
Example:\
- \'93Strong title match and preferred location.\'94\
- \'93Relevant role, but salary wasn\'92t listed.\'94\
\
---\
\
## Phase 3: Authentication and onboarding\
\
### 11. Build authentication flow\
\
Support:\
- email/password\
- Google OAuth\
\
MVP note:\
- Gmail scanning still assumes Gmail-connected users only\
\
Need:\
- sign in\
- sign up\
- session handling\
- sign out\
- protected routes\
\
Output:\
- auth screens\
- session persistence\
- secure route guard behavior\
\
### 12. Build Gmail connect step\
\
Create the first onboarding action.\
\
User goal:\
- connect Gmail with confidence\
\
Screen needs:\
- simple explanation of what is scanned\
- simple explanation of what is stored\
- privacy reassurance\
- primary action to connect Gmail\
\
Output:\
- Gmail connect screen\
- success state\
- failure state\
- disconnected state\
\
### 13. Build preference collection flow\
\
Create a fast, structured onboarding sequence.\
\
Collect:\
- target job titles\
- preferred locations\
- salary range\
- remote / hybrid / onsite\
- seniority\
- preferred companies\
- preferred industries\
- digest frequency\
\
Rules:\
- use helpful defaults\
- keep each step small\
- avoid long forms\
- show a plain-language summary at the end\
\
Output:\
- multi-step onboarding flow\
- completion state\
- editable saved preferences\
\
### 14. Build onboarding summary step\
\
Show the user what JobSignal will do.\
\
Example:\
- \'93We\'92ll prioritize Senior Product Manager roles in New York or remote above $160k and send a weekday digest.\'94\
\
Output:\
- confirmation screen\
- final save action\
- path into ranked jobs view\
\
---\
\
## Phase 4: Job intake and parsing\
\
### 15. Build job email intake pipeline\
\
Ingest supported Gmail job emails.\
\
MVP source focus:\
- LinkedIn job alerts\
\
Pipeline tasks:\
- identify eligible emails\
- record sender and subject\
- store receipt timestamp\
- attach raw payload safely\
- mark parse status\
\
Output:\
- raw ingestion workflow\
- status logging\
- safe skip behavior for unsupported emails\
\
### 16. Build LinkedIn parser\
\
Extract structured fields from LinkedIn emails.\
\
Target fields:\
- title\
- company\
- location\
- salary text if present\
- source link\
- posted date if present\
\
Output:\
- parsed job extraction flow\
- field confidence rules\
- parse error logging\
\
### 17. Handle malformed or partial emails\
\
Gracefully manage weak inputs.\
\
Rules:\
- skip unreadable payloads\
- store failure reason\
- never block the rest of the workflow\
- never show technical errors to users\
\
User-facing example:\
- \'93We couldn\'92t read this email format, so it was skipped.\'94\
\
Output:\
- resilient fallback behavior\
- internal parse monitoring\
\
---\
\
## Phase 5: Ranking pipeline and digest assembly\
\
### 18. Build deduplication job\
\
Run dedupe before ranking.\
\
Tasks:\
- compare parsed jobs to canonical jobs\
- merge duplicates into one canonical listing\
- retain source traceability\
- preserve first seen timing\
\
Output:\
- canonical jobs records\
- duplicate map\
- duplicate test coverage\
\
### 19. Build user-specific ranking job\
\
Score jobs against each user\'92s preferences.\
\
Tasks:\
- apply weighting rules\
- compute match score\
- assign label\
- generate explanation\
- store user job status defaults\
\
Output:\
- populated `user_job_rankings`\
- ranking reason strings\
- label thresholds validated against sample data\
\
### 20. Build digest section logic\
\
Assemble digest sections with clear rules.\
\
Sections:\
- Top matches\
- Worth considering\
- New today\
\
Rules:\
- only include unique jobs\
- cap section length for readability\
- allow \'93No strong matches today\'94\
- preserve useful jobs without overfilling the digest\
\
Output:\
- digest assembly logic\
- section ordering rules\
- fallback states for quiet days\
\
### 21. Build scheduling workflow\
\
Support:\
- every morning\
- weekday mornings\
\
Workflow:\
- select eligible users\
- pull newly ingested jobs\
- deduplicate\
- rank\
- assemble digest\
- send email\
- store digest record\
- store included jobs\
- record delivery result\
\
Output:\
- scheduled edge function flow\
- retry behavior\
- delivery audit trail\
\
---\
\
## Phase 6: Product UI\
\
### 22. Build homepage\
\
Goals:\
- explain product in one sentence\
- make Connect inbox obvious\
- allow digest preview\
\
Needs:\
- calm hero section\
- low-noise layout\
- strong hierarchy\
- breathing room\
\
Output:\
- public landing page\
- preview digest section\
- trust and privacy cues\
\
### 23. Build ranked jobs page\
\
This is the core product screen.\
\
Use:\
- clean vertical list\
- light separators\
- quiet hover states\
- clear scan hierarchy\
\
Each row shows:\
- title\
- company\
- location\
- salary if available\
- source\
- date found\
- match label\
\
Output:\
- inbox-style job list\
- list filters only if essential\
- empty state for no jobs yet\
\
### 24. Build job detail page\
\
Show:\
- parsed role details\
- original source link\
- ranking explanation\
- save / dismiss / applied / hide similar\
\
Rules:\
- narrow reading width\
- clear section structure\
- forgiving confirmation patterns\
- easy reversal where possible\
\
Output:\
- calm editorial detail view\
- action states\
- confirmation and undo patterns\
\
### 25. Build preferences page\
\
Allow users to adjust:\
- criteria\
- weighting\
- digest schedule\
- enabled sources\
\
Also show:\
- plain-language summary of current logic\
\
Output:\
- editable form sections\
- save confirmation\
- updated ranking summary\
\
### 26. Build digest preview page\
\
Show the exact shape of the outgoing email.\
\
Include:\
- Top matches\
- Worth considering\
- New today\
\
Rules:\
- concise\
- highly legible\
- email-like, not dashboard-like\
\
Output:\
- preview screen\
- no-data state\
- clear alignment with delivered email\
\
### 27. Build digest history page\
\
Create a quiet archive.\
\
Needs:\
- chronological list of past digests\
- access to included jobs\
- patient empty state\
- low clutter\
\
Output:\
- digest archive screen\
- digest detail drill-in\
- delivery status display\
\
---\
\
## Phase 7: Reliability, trust, and polish\
\
### 28. Add action state tracking\
\
Track user job actions:\
- new\
- saved\
- dismissed\
- applied\
- hidden\
\
Rules:\
- changes should feel immediate\
- destructive actions should be recoverable when possible\
- hidden jobs should stay out of primary views\
\
Output:\
- state persistence\
- undo where appropriate\
- status-based filtering behavior\
\
### 29. Add source controls\
\
Support source enable or disable settings.\
\
MVP behavior:\
- LinkedIn enabled by default\
- architecture ready for more sources later\
\
Output:\
- quiet source management module\
- no clutter from future unsupported sources\
\
### 30. Add privacy controls\
\
Users should be able to understand and manage their data.\
\
Need:\
- scan scope explanation\
- delete account path\
- disconnect path\
- simple retention language\
\
Output:\
- privacy settings section\
- trust-building copy\
- internal deletion workflow\
\
### 31. Add QA instrumentation\
\
Track product health.\
\
Monitor:\
- parse success rate\
- duplicate collapse rate\
- ranking coverage\
- digest send success\
- digest open rate\
- common user actions\
\
Output:\
- internal dashboards or logs\
- alerting for failed workflows\
- review routine for parsing failures\
\
### 32. Run usability passes\
\
Test with 3 users for 30 minutes.\
\
Focus questions:\
- Can they explain what JobSignal does after one screen?\
- Can they complete onboarding without hesitation?\
- Can they scan the ranked list like an inbox?\
- Do ranking explanations feel clear and trustworthy?\
\
Output:\
- top 3 confusion points\
- design fixes before broader release\
\
---\
\
## Timeline With Checkpoints\
\
### Week 1: Foundation\
\
Ship:\
- app scaffold\
- Supabase setup\
- auth baseline\
- database schema draft\
- design system primitives\
\
Checkpoint:\
- a signed-in user can reach a protected app shell\
\
### Week 2: Onboarding and preferences\
\
Ship:\
- Gmail connect flow\
- onboarding flow\
- preference storage\
- plain-language preference summary\
\
Checkpoint:\
- a user can connect, finish setup, and save digest timing\
\
### Week 3: Intake and parsing\
\
Ship:\
- LinkedIn email intake\
- parser\
- raw email storage\
- parse status handling\
\
Checkpoint:\
- sample LinkedIn alerts become structured job records\
\
### Week 4: Deduplication and ranking\
\
Ship:\
- canonical jobs table\
- dedupe logic\
- ranking logic\
- explanation generation\
- label assignment\
\
Checkpoint:\
- one parsed dataset produces a ranked unique jobs list per user\
\
### Week 5: Core product views\
\
Ship:\
- homepage\
- ranked jobs page\
- detail view\
- preferences page\
- digest preview\
\
Checkpoint:\
- end-to-end product flow works inside the app\
\
### Week 6: Digest workflow\
\
Ship:\
- digest assembly\
- scheduled workflow\
- Resend integration\
- digest history\
- delivery status logging\
\
Checkpoint:\
- a user receives a realistic test digest and can revisit it in-app\
\
### Week 7: Trust, polish, and QA\
\
Ship:\
- source control\
- undo and confirmation flows\
- privacy settings\
- accessibility pass\
- usability fixes\
\
Checkpoint:\
- MVP is stable enough for small private beta use\
\
---\
\
## Team Roles\
\
### Product lead\
\
Owns:\
- scope decisions\
- user journey clarity\
- ranking trust\
- roadmap tradeoffs\
\
### Product designer\
\
Owns:\
- calm visual system\
- onboarding flow\
- list/detail patterns\
- digest readability\
- accessibility and usability refinement\
\
### Frontend engineer\
\
Owns:\
- React app structure\
- page flows\
- state management\
- reusable UI components\
- accessibility implementation\
\
### Backend engineer\
\
Owns:\
- Supabase schema\
- edge functions\
- ingestion workflow\
- ranking and dedupe pipeline\
- scheduling and delivery orchestration\
\
### QA / product ops\
\
Owns:\
- parser edge cases\
- workflow reliability\
- digest verification\
- manual bug sweeps\
- feedback tracking during beta\
\
### Optional growth or operations support\
\
Owns:\
- onboarding messaging\
- email deliverability review\
- user interview coordination\
- beta feedback synthesis\
\
---\
\
## Recommended Rituals\
\
### Twice-weekly product review\
\
Review:\
- what shipped\
- what felt confusing\
- what should be trimmed\
\
### Weekly reliability check\
\
Inspect:\
- parse failures\
- send failures\
- duplicate issues\
- broken explanations\
\
### Bi-weekly usability session\
\
Run:\
- one 30-minute test with 3 target users\
\
Measure:\
- clarity\
- scan speed\
- trust\
- friction points\
\
### Weekly ranking review\
\
Look at:\
- saved jobs\
- dismissed jobs\
- applied jobs\
- common false positives\
\
Goal:\
- improve ranking rules without making the product feel opaque\
\
### Monthly calmness audit\
\
Ask:\
- Is any screen getting too busy?\
- Did any new feature introduce dashboard energy?\
- Are labels still simpler than the underlying logic?\
\
---\
\
## Optional Integrations\
\
### Near-term additions\
\
- Google Calendar for reminder nudges after saving a role\
- company metadata enrichment for cleaner job cards\
- analytics tooling for funnel and retention tracking\
\
### Later source integrations\
\
- Indeed\
- Greenhouse\
- Lever\
- direct company alerts\
\
### Operational additions\
\
- error monitoring\
- session replay for usability debugging\
- support inbox integration\
\
---\
\
## Stretch Goals\
\
### 1. Adaptive relevance learning\
\
Use behavior to improve ranking quietly.\
\
Signals:\
- saved\
- dismissed\
- applied\
- preference edits\
\
Guardrails:\
- keep users in control\
- never present this as chatbot intelligence\
- never remove plain-language ranking explanations\
\
### 2. Smarter duplicate grouping\
\
Improve grouping for:\
- title variants\
- multi-location postings\
- reposted jobs across close dates\
\
### 3. Digest personalization\
\
Adjust digest density by user behavior.\
\
Example:\
- show fewer lower-priority jobs for users who only engage with top matches\
\
### 4. Company watchlists\
\
Let users explicitly follow companies of interest.\
\
### 5. Hide-similar refinement\
\
Allow users to suppress repeated patterns like:\
- specific titles\
- repeated recruiter blasts\
- noisy location variants\
\
---\
\
## Release Readiness Checklist\
\
### Product\
\
- homepage explains value in one glance\
- onboarding completes without confusion\
- ranked list is scannable like an inbox\
- detail page explains ranking clearly\
- digest preview matches delivered digest\
\
### Data and logic\
\
- LinkedIn emails parse reliably enough for MVP\
- duplicate rules handle common repeats\
- ranking labels feel trustworthy\
- unsupported emails fail safely\
\
### Delivery\
\
- scheduled jobs run correctly\
- digest email sends successfully\
- digest history is stored accurately\
- send failures are logged and visible internally\
\
### Trust and accessibility\
\
- Gmail permissions are explained clearly\
- privacy controls are easy to find\
- keyboard navigation works across key screens\
- color is never the only relevance signal\
- WCAG AA contrast targets are met\
\
---\
\
## Final Implementation Principle\
\
Build JobSignal like a quiet machine.\
\
Small parts.\
Clear rules.\
Reliable output.\
\
The user should feel the product working for them without having to think about how it works.}