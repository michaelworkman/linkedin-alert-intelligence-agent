{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## 30-Second Elevator Pitch\
\
JobSignal turns noisy job alert emails into one calm daily shortlist.\
\
Users connect Gmail, set simple job preferences, and receive a clean morning digest of the best unique roles. The app removes duplicates, ranks jobs against what matters most, and explains each match in plain language.\
\
## Problem & Mission\
\
### Problem\
\
Job seekers often receive too many job emails.\
\
Common pain points:\
- Duplicate roles across alerts\
- Weak filtering from job platforms\
- Too much scanning, too little signal\
- Missed opportunities buried in inbox noise\
- Stress from having to check constantly\
\
### Mission\
\
Help people feel less overwhelmed during a job search.\
\
JobSignal should:\
- quietly monitor incoming job emails\
- remove repeated listings\
- rank roles against personal criteria\
- deliver one useful summary at the right time\
- feel calm, clear, and dependable\
\
## Target Audience\
\
### Primary audience\
\
Professionals actively job searching and already receiving LinkedIn job alerts.\
\
### Secondary audiences\
\
- Passive candidates who want low-effort monitoring\
- Career changers who need stricter filters\
- Busy professionals who prefer a digest over constant checking\
\
### User mindset\
\
These users are often tired, distracted, or anxious.\
\
The product must reduce thought, not add it.\
\
## Core Features\
\
### 1) Homepage\
\
Purpose:\
- explain the product in one glance\
- get users to connect Gmail\
- offer a digest preview before signup\
\
Key elements:\
- one-sentence value proposition\
- primary CTA: Connect inbox\
- secondary CTA: Preview digest\
- calm, minimal structure\
- strong spacing and hierarchy\
\
### 2) Onboarding\
\
Purpose:\
- connect Gmail\
- collect ranking preferences fast\
- schedule digest delivery\
\
Inputs:\
- target job titles\
- preferred locations\
- salary range\
- remote / hybrid / onsite\
- seniority\
- optional companies\
- optional industries\
- digest frequency\
\
Principles:\
- fast\
- structured\
- default-friendly\
- low friction\
\
### 3) Preferences Page\
\
Purpose:\
- let users update filters anytime\
- make ranking logic understandable\
\
Controls:\
- editable criteria\
- adjustable ranking weights\
- digest timing\
- source toggles\
\
Plain-language summary example:\
- \'93Prioritizing Senior Product Manager roles in New York or remote above $160k.\'94\
\
### 4) Inbox Scan & Source Control\
\
Purpose:\
- ingest supported job emails\
- parse relevant details\
- allow source management\
\
MVP source:\
- Gmail inbox with LinkedIn job alert detection first\
\
Later expansion:\
- Indeed\
- Greenhouse\
- Lever\
- company alerts\
\
Behavior:\
- identify job emails\
- extract listing details\
- store raw payloads safely\
- support source enable/disable settings\
\
### 5) Ranked Jobs View\
\
Purpose:\
- act like the user\'92s clean job inbox\
\
Row content:\
- job title\
- company\
- location\
- salary if available\
- source\
- date found\
- match label\
\
Labels:\
- Top match\
- Good fit\
- Lower priority\
\
Interaction pattern:\
- quiet vertical list\
- subtle separators\
- restrained hover\
- obvious scan hierarchy\
\
### 6) Job Detail View\
\
Purpose:\
- show full parsed role details\
- explain ranking clearly\
- support simple actions\
\
Actions:\
- Save\
- Dismiss\
- Applied\
- Hide similar roles\
\
Content:\
- job details\
- source link\
- plain-language ranking explanation\
- forgiving confirmations\
- easy recovery from mistakes\
\
### 7) Digest Preview\
\
Purpose:\
- show the exact digest before delivery\
\
Digest sections:\
- Top matches\
- Worth considering\
- New today\
\
Tone:\
- concise\
- editorial\
- legible\
- useful at a glance\
\
### 8) Digest History\
\
Purpose:\
- let users revisit prior digests without clutter\
\
Needs:\
- quiet archive pattern\
- readable summaries\
- patient empty states\
- fast access to missed roles\
\
### 9) Lightweight Relevance Learning\
\
Purpose:\
- improve ranking silently over time\
\
Signals:\
- saved jobs\
- dismissed jobs\
- applied jobs\
- repeated preference edits\
\
Rule:\
- never feel like a chatbot\
- never become the product personality\
- only improve sorting and explanations\
\
## High-Level Tech Stack\
\
### Frontend\
\
- **Vite**\
  - fast local development\
  - low setup friction for MVP\
\
- **TypeScript**\
  - safer product iteration\
  - clearer contracts across UI and backend\
\
- **React**\
  - strong fit for list/detail workflows\
  - flexible component model for onboarding, preferences, and digest views\
\
- **Tailwind CSS**\
  - fast layout control\
  - supports a restrained, spacing-driven interface\
\
- **shadcn/ui**\
  - accessible building blocks\
  - good fit for calm, modern, low-noise product UI\
\
### Backend & Database\
\
- **Supabase**\
  - combines auth, Postgres, storage, edge logic, and scheduling\
  - keeps MVP architecture focused\
  - reduces integration overhead\
\
### Authentication\
\
- **Supabase Auth**\
  - email/password or Google OAuth\
  - clean path for Gmail-connected workflows\
\
### Server Logic\
\
- **Supabase Edge Functions**\
  - good fit for parsing, ranking, dedupe, digest assembly, and scheduled workflows\
\
### Email Delivery\
\
- **Resend**\
  - strong fit for digest delivery\
  - supports email templates, logs, and reliable sending\
\
### Scheduling\
\
- **Supabase scheduled jobs / cron-triggered Edge Functions**\
  - simple daily or weekday digest workflow\
  - keeps automation inside the same backend stack\
\
## Conceptual Data Model\
\
Think of the system as five layers.\
\
### 1) User layer\
\
Stores:\
- account identity\
- auth provider\
- timezone\
- digest frequency\
\
Main entity:\
- `users`\
\
### 2) Preference layer\
\
Stores:\
- target titles\
- preferred locations\
- salary range\
- work mode\
- seniority\
- preferred companies\
- preferred industries\
- ranking weights\
\
Main entity:\
- `job_preferences`\
\
Relationship:\
- one user has one active preference profile\
\
### 3) Intake layer\
\
Stores:\
- raw job emails detected from Gmail\
- sender\
- subject\
- receive time\
- raw parsed payload\
\
Main entity:\
- `ingested_job_emails`\
\
Relationship:\
- one user has many ingested emails\
\
### 4) Canonical jobs layer\
\
Stores:\
- deduplicated job listings\
- normalized title, company, location\
- optional salary range\
- source link\
- first seen date\
- canonical key\
\
Main entity:\
- `jobs`\
\
Relationship:\
- many raw emails may map to one canonical job\
\
### 5) Per-user ranking and digest layer\
\
Stores:\
- job score for a specific user\
- match label\
- explanation\
- status\
- digest delivery records\
- digest contents\
\
Main entities:\
- `user_job_rankings`\
- `digests`\
- `digest_items`\
\
Relationship:\
- one user sees many ranked jobs\
- one digest contains many digest items\
- one job may appear in many users\'92 digests\
\
### ERD sketch in words\
\
- `users` \uc0\u8594  has one `job_preferences`\
- `users` \uc0\u8594  has many `ingested_job_emails`\
- `ingested_job_emails` \uc0\u8594  may create or reference one `jobs` record\
- `users` + `jobs` \uc0\u8594  join through `user_job_rankings`\
- `users` \uc0\u8594  has many `digests`\
- `digests` \uc0\u8594  has many `digest_items`\
- `digest_items` \uc0\u8594  references `jobs`\
\
## UI Design Principles\
\
### Calm first\
\
Every screen should feel quieter after it loads.\
\
### Scan before read\
\
Users should understand the screen structure in seconds.\
\
Example:\
- list rows should reveal title, company, location, and match level without opening details\
\
### One primary action\
\
Each screen should have one obvious next step.\
\
Example:\
- homepage: Connect inbox\
- job detail: Save, Dismiss, or Applied\
\
### Plain-language logic\
\
Explain ranking without sounding robotic.\
\
Example:\
- \'93Strong title match and preferred location.\'94\
\
Not:\
- \'93Confidence score generated from multi-factor relevance model.\'94\
\
### List patterns over dashboards\
\
Use inbox-like flows instead of analytics-heavy layouts.\
\
### Gentle recovery\
\
Mistakes must be reversible.\
\
Example:\
- dismissing a role should be undoable\
- hiding similar roles should be confirmed clearly\
\
### Restraint over delight\
\
Use subtle feedback, not theatrical motion.\
\
### Consistent emotional logic\
\
Every page should share:\
- quiet hierarchy\
- thin dividers\
- generous whitespace\
- narrow readable content\
- simple labels\
\
## Security & Compliance Notes\
\
### User data sensitivity\
\
JobSignal handles personal job preferences and email-derived job data.\
\
Protect:\
- email addresses\
- inbox-derived content\
- application intent signals\
- preferences tied to career goals\
\
### Core security needs\
\
- secure OAuth handling for Gmail connection\
- least-privilege access to user data\
- encrypted transport everywhere\
- row-level protection in database\
- audit-friendly delivery logs\
- secure secret handling for email and auth providers\
\
### Compliance mindset for MVP\
\
MVP should be privacy-conscious from day one.\
\
Include:\
- clear consent for Gmail access\
- simple explanation of what is scanned\
- simple explanation of what is stored\
- source controls users can disable\
- deletion path for account and stored data\
\
### Data retention principle\
\
Keep only what improves product usefulness.\
\
Do not store unnecessary email content long term.\
\
### Abuse and trust safeguards\
\
- skip malformed or unsupported emails safely\
- avoid false certainty in ranking explanations\
- provide clear source links back to original listings\
- let users dismiss or hide noisy patterns quickly\
\
## Phased Roadmap\
\
### MVP\
\
Goal:\
- prove users want quiet, ranked job digests from Gmail alerts\
\
Scope:\
- Gmail connection\
- LinkedIn email detection\
- raw email ingestion\
- parsing of key job fields\
- deduplication\
- user preferences\
- adjustable ranking weights\
- ranked jobs list\
- job detail page\
- digest preview\
- digest history\
- every morning or weekday morning scheduling\
- Resend delivery\
- plain-language match explanations\
\
### V1\
\
Goal:\
- improve relevance and trust\
\
Add:\
- stronger parsing coverage\
- better duplicate grouping\
- company and industry prioritization\
- more ranking explanation clarity\
- undo flows and bulk actions\
- source management improvements\
- better delivery status visibility\
\
### V2\
\
Goal:\
- expand coverage and personalization\
\
Add:\
- Indeed support\
- Greenhouse support\
- Lever support\
- company alert support\
- lightweight adaptive relevance learning\
- smarter hide-similar controls\
- richer digest personalization\
- cross-source canonical job intelligence\
\
## Risks & Mitigations\
\
### Risk: email parsing is inconsistent\
\
Why it matters:\
- job emails vary in structure\
- missing fields reduce ranking quality\
\
Mitigation:\
- start with LinkedIn only\
- design tolerant parsers\
- skip safely when confidence is low\
- show clear fallback copy like \'93salary wasn\'92t listed\'94\
\
### Risk: duplicate detection is messy\
\
Why it matters:\
- the same role may appear with small title or location differences\
\
Mitigation:\
- use normalized canonical keys\
- combine title, company, location, and source URL when available\
- review duplicate edge cases during testing\
\
### Risk: ranking feels arbitrary\
\
Why it matters:\
- users lose trust fast if results feel random\
\
Mitigation:\
- show plain-language explanations\
- expose editable ranking weights\
- keep labels simple and restrained\
- avoid black-box AI language\
\
### Risk: Gmail access feels invasive\
\
Why it matters:\
- users may hesitate to connect inboxes\
\
Mitigation:\
- explain the scope clearly\
- scan only supported job emails\
- give source controls\
- make privacy language simple and specific\
\
### Risk: digest quality is uneven on quiet days\
\
Why it matters:\
- users may expect strong matches every day\
\
Mitigation:\
- allow \'93No strong matches today\'94\
- separate \'93Top matches\'94 from \'93Worth considering\'94\
- avoid forcing weak results into high-confidence sections\
\
### Risk: product drifts into recruiting-tool complexity\
\
Why it matters:\
- dashboards, filters, and status systems can overwhelm the core promise\
\
Mitigation:\
- keep list-first UI\
- favor defaults over configuration\
- protect the calm editorial feel on every release\
\
## Future Expansion Ideas\
\
- Outlook support\
- company watchlists\
- salary insight enrichment\
- job application tracker\
- duplicate clusters with \'93why grouped\'94 explanation\
- digest personalization by user behavior\
- weekly trend summaries\
- team or coach sharing for career advisors\
- role-based search presets for career changers\
- browser extension for saving external job links\
- confidence flags for incomplete or weakly parsed listings\
\
## Product Success Signals\
\
### Early success looks like\
\
- users complete Gmail connection and onboarding quickly\
- users open digests regularly\
- users save or apply from surfaced roles\
- users report lower noise and better relevance\
- users rarely need to edit too many settings to get value\
\
### Core MVP metrics\
\
- onboarding completion rate\
- Gmail connect conversion rate\
- digest open rate\
- save / dismiss / applied action rates\
- duplicate reduction rate\
- percentage of digests with at least one strong match\
- preference edit frequency after first week\
\
## Final Product Principle\
\
JobSignal should feel like a trusted filter.\
\
Not louder.\
Not smarter-looking.\
Just clearer.\
\
The product wins when it quietly turns inbox clutter into a short list a user can trust before their day begins.}