{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\froman\fcharset0 Times-Bold;\f2\froman\fcharset0 Times-Roman;
}
{\colortbl;\red255\green255\blue255;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c100000\c100000\c99971;\cssrgb\c0\c0\c0;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat0\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## Emotional Tone\
\
**Feels like Apple Mail for job discovery \'97 calm, airy, orderly, and quietly competent, with kindness expressed through clarity, restraint, and forgiving interactions.**\
\
This follows the core design guidance from `design-tips.md`:\
- start with feeling, not features\
- design emotional moments, not just static screens\
- make technology feel kind, not loud\
- favor invisible help over attention-seeking behavior\
- build trust through patience, forgiveness, and calm defaults\
\
## Emotional Design Intent\
\
JobSignal is not trying to excite users.\
\
It is trying to relieve them.\
\
The interface should feel:\
- calm\
- clear\
- supportive\
- capable\
- neutral\
- lightly editorial\
\
It should never feel:\
- gamified\
- salesy\
- urgent\
- chatty\
- over-personalized\
- dashboard-heavy\
\
### Emotional promise\
\
JobSignal should feel like a trusted filter between a messy inbox and a calmer morning.\
\
### Key emotional moments\
\
#### First visit\
\
The homepage should feel instantly understandable.\
\
The user should think:\
- \'93This is simple.\'94\
- \'93This will save me time.\'94\
- \'93This won\'92t add more noise.\'94\
\
#### Onboarding\
\
The setup flow should feel like a calm welcome.\
\
Not a questionnaire.\
Not a funnel.\
\
Each step should feel short, obvious, and reversible.\
\
#### Ranked jobs view\
\
This is the emotional center of the product.\
\
It should feel like opening a well-organized inbox:\
- light\
- quiet\
- legible\
- easy to scan\
\
#### Error and empty states\
\
These should feel patient and respectful.\
\
Example:\
- \'93We couldn\'92t read this email format, so it was skipped.\'94\
\
Not:\
- \'93Parsing failed.\'94\
- \'93Invalid input.\'94\
- \'93Action unsuccessful.\'94\
\
#### Destructive actions\
\
Dismiss, hide, and similar actions should feel forgiving.\
\
Kindness in design means second chances.\
\
Use:\
- undo\
- soft confirmations\
- clear recovery paths\
\
## Visual System\
\
### Style anchors\
\
Use these as aesthetic references:\
- **Apple Mail** for calm list hierarchy\
- **shadcn/ui** for clean, accessible building blocks\
- **Linear** for precision and restraint\
- **Apple Human Interface** for quiet confidence and forgiving interactions\
\
### Visual metaphor\
\
JobSignal should feel like:\
- a well-organized inbox\
- a clean editorial workspace\
- a productivity tool that respects attention\
\
It should not feel like:\
- a recruiting CRM\
- a sales dashboard\
- a noisy AI assistant\
\
---\
\
## Typography\
\
Use a neutral sans-serif with strong readability and restrained personality.\
\
Recommended direction:\
- **Inter** for primary UI text\
- fallback: `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`\
\
Why this fits:\
- neutral and highly legible\
- works well for list-heavy interfaces\
- feels modern without feeling expressive\
- supports a quiet, capable tone\
\
### Typography rules\
\
- prioritize readability over style\
- keep headings understated\
- let body text carry meaning\
- avoid decorative display typography\
- maintain at least **1.5 line-height**\
- preserve strong contrast in all text contexts\
\
### Typographic hierarchy\
\
#### H1\
- Size: **32px**\
- Weight: **600**\
- Line height: **40px**\
- Use: page titles and hero headline\
- Tone: calm authority\
\
Example:\
- \'93A cleaner way to track job opportunities\'94\
\
#### H2\
- Size: **24px**\
- Weight: **600**\
- Line height: **32px**\
- Use: section headers and page sections\
\
Example:\
- \'93Top matches for today\'94\
\
#### H3\
- Size: **20px**\
- Weight: **600**\
- Line height: **28px**\
- Use: card headers, digest section titles, detail section titles\
\
#### H4\
- Size: **16px**\
- Weight: **600**\
- Line height: **24px**\
- Use: compact labels within detail screens\
\
#### Body Large\
- Size: **16px**\
- Weight: **400**\
- Line height: **24px**\
- Use: primary reading text, onboarding prompts, ranking explanations\
\
#### Body\
- Size: **14px**\
- Weight: **400**\
- Line height: **22px**\
- Use: row metadata, settings descriptions, helper text\
\
#### Caption\
- Size: **12px**\
- Weight: **500**\
- Line height: **18px**\
- Use: timestamps, secondary metadata, restrained labels\
\
### Typographic rhythm\
\
Use a modular scale that feels stable, not dramatic.\
\
Rules:\
- step sizes should be modest\
- use consistent spacing above and below headings\
- avoid large jumps between body and heading sizes\
- preserve visual breathing room in lists and forms\
\
### Accessibility notes for type\
\
- body text should not go below **14px** in app UI\
- maintain contrast of at least **4.5:1**\
- avoid low-contrast gray on white for core reading text\
- left-align most text for scanning speed\
\
---\
\
## Color System\
\
The palette should feel muted, stable, and lightly polished.\
\
Accent exists to guide action, not to energize the screen.\
\
### Core palette\
\
#### Primary text\
- Hex: `#111827`\
- RGB: `17, 24, 39`\
\
Use for:\
- headings\
- primary labels\
- job titles\
- key UI text\
\
#### Secondary text\
- Hex: `#6B7280`\
- RGB: `107, 114, 128`\
\
Use for:\
- metadata\
- helper copy\
- supporting descriptions\
\
#### Background\
- Hex: `#F9FAFB`\
- RGB: `249, 250, 251`\
\
Use for:\
- page background\
- app shell\
- quiet surfaces\
\
#### Surface\
- Hex: `#FFFFFF`\
- RGB: `255, 255, 255`\
\
Use for:\
- cards\
- list surfaces\
- modal panels\
- digest preview surfaces\
\
#### Divider\
- Hex: `#E5E7EB`\
- RGB: `229, 231, 235`\
\
Use for:\
- thin row separators\
- section dividers\
- form boundaries\
\
#### Accent\
- Hex: `#4F46E5`\
- RGB: `79, 70, 229`\
\
Use for:\
- primary actions\
- selected controls\
- links\
- focused emphasis\
\
Use sparingly.\
\
#### Success\
- Hex: `#16A34A`\
- RGB: `22, 163, 74`\
\
Use for:\
- successful scheduling\
- saved confirmations\
- digest sent indicators\
\
#### Warning\
- Hex: `#D97706`\
- RGB: `217, 119, 6`\
\
Use for:\
- partial data warnings\
- missing salary or limited parse confidence\
\
#### Error\
- Hex: `#DC2626`\
- RGB: `220, 38, 38`\
\
Use for:\
- broken connections\
- failed sends\
- action problems that need attention\
\
### Match labels\
\
Labels should remain restrained.\
\
Do not rely on color alone.\
\
Use both text and subtle visual treatment.\
\
#### Top match\
- text label first\
- optional soft tinted badge\
- never bright or celebratory\
\
#### Good fit\
- neutral badge with slight emphasis\
\
#### Lower priority\
- low-contrast neutral label, still readable\
\
### Light and dark mode guidance\
\
Primary requirement:\
- preserve emotional calm in both modes\
\
Dark mode rules:\
- avoid pure black backgrounds\
- avoid electric accent glow\
- keep contrast strong but soft\
- maintain list clarity with thin dividers and surface separation\
\
### Contrast requirements\
\
- text contrast must meet **WCAG AA**\
- body text should target **4.5:1** or higher\
- interactive controls must remain clear in hover, focus, and disabled states\
- never encode meaning by color alone\
\
---\
\
## Spacing & Layout\
\
Use an **8pt grid** across the full product.\
\
The layout should feel measured, breathable, and stable.\
\
### Core spacing scale\
\
- `4px` for micro-adjustments only\
- `8px` for tight spacing\
- `16px` for default component spacing\
- `24px` for grouped content spacing\
- `32px` for section spacing\
- `48px` for page-level breathing room\
- `64px` for hero and major content separation\
\
### Layout rules\
\
- prefer single-column reading patterns\
- avoid dense multi-panel dashboards\
- use whitespace as a structural tool\
- separate rows with dividers before using cards\
- keep content width narrow enough for easy scanning\
\
### Max widths\
\
#### Homepage and onboarding\
- max content width: **720px**\
- centered\
- generous top and bottom spacing\
\
#### Ranked jobs list\
- max content width: **960px**\
- list-centered layout\
- no unnecessary sidebars in MVP\
\
#### Job detail view\
- max reading width: **720px**\
- narrow editorial column\
- metadata grouped cleanly above content\
\
#### Preferences and digest history\
- max content width: **800px**\
- section-based layout\
- simple stacked controls\
\
### Responsive behavior\
\
#### Mobile-first logic\
\
Start from the smallest screen.\
\
On mobile:\
- single column only\
- stacked action controls\
- row metadata collapses cleanly\
- no hover-dependent interactions\
- digest preview remains highly readable\
\
#### Tablet\
- preserve single-column content rhythm\
- allow slightly wider list rows\
- keep controls visually grouped\
\
#### Desktop\
- maintain restraint\
- use added width for breathing room, not for more UI\
- keep the ranked jobs list readable in one scan\
\
### Component padding rules\
\
#### Cards and panels\
- internal padding: **16px** or **24px**\
\
#### List rows\
- vertical padding: **12px\'9616px**\
- horizontal padding: **16px**\
\
#### Forms\
- field group spacing: **16px**\
- section spacing: **24px\'9632px**\
\
---\
\
## Motion & Interaction\
\
The product should acknowledge action without drawing attention to itself.\
\
This follows the kindness principle from `design-tips.md`:\
- motion should support understanding\
- transitions should reduce stress\
- feedback should feel patient, not flashy\
\
### Motion tone\
\
Use motion that feels:\
- gentle\
- confident\
- nearly invisible\
\
Avoid motion that feels:\
- bouncy\
- playful\
- exaggerated\
- cinematic\
\
### Motion standards\
\
- hover transitions: **150\'96200ms**\
- panel and modal transitions: **180\'96240ms**\
- state fades: **150\'96220ms**\
- standard easing: soft ease-out\
- no elastic or spring-heavy motion in MVP\
\
### Interaction behaviors\
\
#### Hover\
\
Use subtle feedback only.\
\
Examples:\
- light background tint\
- slight accent on title or border\
- no scaling\
- no glow\
\
#### Tap and click\
\
Actions should feel immediate and calm.\
\
Use:\
- soft pressed states\
- clear focus transitions\
- concise confirmations\
\
#### Empty states\
\
Empty states should feel patient.\
\
Example:\
- \'93No strong matches today.\'94\
- \'93Your next digest will appear here.\'94\
\
#### Undo patterns\
\
Use undo for recoverable actions like:\
- dismiss\
- hide similar\
- archive-like changes\
\
#### Loading states\
\
Loading should feel quiet.\
\
Use:\
- skeleton rows\
- soft shimmer or static placeholders\
- no spinner-centered experience unless unavoidable\
\
#### Notifications\
\
Keep toast usage minimal.\
\
Good use:\
- \'93Weekday digest scheduled\'94\
- \'93Job saved\'94\
- \'93Hidden roles updated\'94\
\
Bad use:\
- repeated celebratory banners\
- stacked alerts\
- interruptive modals for small confirmations\
\
---\
\
## Voice & Tone\
\
Copy should be plain, calm, and direct.\
\
It should feel like a competent assistant, not a cheerful brand mascot.\
\
### Personality keywords\
\
- clear\
- calm\
- restrained\
- supportive\
- editorial\
- trustworthy\
\
### Voice rules\
\
- prefer short sentences\
- lead with the outcome\
- avoid hype language\
- avoid AI theater\
- avoid exclamation points unless truly necessary\
- explain ranking in plain English\
\
### Copy examples\
\
#### Onboarding\
- \'93Connect Gmail to start scanning job alerts.\'94\
- \'93Choose the roles and locations you want to prioritize.\'94\
- \'93Pick when you want your digest.\'94\
\
#### Success\
- \'93Weekday digest scheduled.\'94\
- \'93Preferences updated.\'94\
- \'93Duplicates removed.\'94\
\
#### Error\
- \'93We couldn\'92t read this email format, so it was skipped.\'94\
- \'93We couldn\'92t send today\'92s digest. We\'92ll try again at the next scheduled window.\'94\
- \'93Gmail access expired. Reconnect to keep scanning new job alerts.\'94\
\
#### Empty state\
- \'93No strong matches today.\'94\
- \'93You haven\'92t saved any roles yet.\'94\
- \'93Your first digest will appear here after new job alerts are processed.\'94\
\
### Ranking explanation style\
\
Good:\
- \'93Strong title match and preferred location.\'94\
- \'93Relevant role, but salary wasn\'92t listed.\'94\
- \'93Good fit, though outside your preferred seniority.\'94\
\
Avoid:\
- \'93Our AI believes this opportunity aligns with your profile.\'94\
- \'93Confidence score derived from behavioral weighting.\'94\
\
---\
\
## System Consistency\
\
JobSignal should obey one emotional logic across every screen:\
- quiet hierarchy\
- low visual noise\
- simple labels\
- forgiving actions\
- stable patterns\
\
### Repeating UI patterns\
\
#### List rows\
\
Use the same row anatomy across:\
- ranked jobs\
- digest history\
- preview sections where relevant\
\
Suggested row order:\
- title first\
- company second\
- supporting metadata third\
- match label aligned consistently\
- action affordance quiet but visible\
\
#### Detail sections\
\
Keep the same structure for:\
- role summary\
- why it matched\
- source link\
- user actions\
\
#### Forms\
\
Use the same component rhythm across:\
- onboarding\
- preferences\
- source control\
- digest settings\
\
#### Labels\
\
Use the same status language everywhere:\
- Top match\
- Good fit\
- Lower priority\
- Saved\
- Dismissed\
- Applied\
- Hidden\
\
### Structural consistency rule\
\
Think systems before screens.\
\
If a row pattern works, reuse it.\
If a spacing rule works, repeat it.\
If a label is clear once, do not rename it elsewhere.\
\
---\
\
## Accessibility\
\
Accessibility is part of calmness.\
\
An interface is not calm if it excludes users or makes interaction harder under stress.\
\
### Semantic structure\
\
Use:\
- one clear H1 per page\
- ordered heading hierarchy\
- semantic landmarks for header, main, nav, and footer\
- descriptive labels for settings and controls\
\
### Keyboard navigation\
\
Must support:\
- visible tab order\
- clear focus indicators on rows and controls\
- full operation of list, detail, and settings pages without a mouse\
- no hover-only disclosure of essential actions\
\
### Focus indicators\
\
Focus should be:\
- visible\
- high contrast\
- consistent across components\
- restrained but unmistakable\
\
Good example:\
- a 2px accent ring with sufficient contrast and offset\
\
### ARIA and assistive support\
\
Include:\
- descriptive labels for ranking explanations\
- semantic grouping for digest settings\
- status messaging for updates\
- clear button labels for save, dismiss, applied, and hide similar\
\
### Inclusive interaction rules\
\
- never rely only on color for status or priority\
- maintain readable tap targets\
- support zoom without layout breakage\
- ensure skeleton and loading states do not hide structure from screen reader users\
\
### Comfort audit\
\
For every major screen, ask:\
- Can this be used when the user is tired?\
- Is the next step obvious without guesswork?\
- Can the screen be scanned without visual strain?\
- Do errors guide instead of blame?\
\
---\
\
## Page-Specific Design Notes\
\
### Homepage\
\
Should feel:\
- quiet\
- spacious\
- self-explanatory\
\
Use:\
- one clear headline\
- one sentence of value\
- two CTAs only\
- visual breathing room\
- restrained trust cues\
\
Do not use:\
- crowded feature grids\
- aggressive proof sections\
- animated hero gimmicks\
\
### Onboarding\
\
Should feel:\
- structured\
- quick\
- supportive\
\
Use:\
- one task per step\
- clear defaults\
- progress indicator if it reduces uncertainty\
- summary language before completion\
\
### Preferences\
\
Should feel:\
- understandable\
- adjustable\
- low-friction\
\
Use:\
- grouped settings\
- plain-language summary\
- weight controls with clear effect\
- calm save confirmation\
\
### Ranked Jobs View\
\
This should feel closest to Apple Mail.\
\
Use:\
- clean vertical list\
- subtle row hover\
- thin separators\
- quiet metadata\
- obvious hierarchy between title and secondary info\
\
Do not use:\
- dense chips everywhere\
- analytics panels\
- chart widgets\
- overdesigned cards\
\
### Job Detail View\
\
Should feel:\
- narrow\
- readable\
- editorial\
\
Use:\
- clear title block\
- why-this-matched section\
- source link\
- simple action row\
- generous spacing between sections\
\
### Digest Preview\
\
Should feel:\
- concise\
- trustworthy\
- polished enough to send\
\
Use:\
- section headers\
- clear grouping\
- digest-like width\
- calm email rhythm\
\
### Digest History\
\
Should feel:\
- archival\
- clean\
- easy to revisit\
\
Use:\
- chronological order\
- lightweight summaries\
- patient empty state\
\
---\
\
## Emotional Audit Checklist\
\
Review every major screen against these questions:\
\
- Does this screen evoke calm and competence?\
- Can the user understand the main purpose in seconds?\
- Are motion and copy supporting the intended emotion?\
- Would a tired or stressed user feel supported here?\
- Did we remove noise instead of adding interface energy?\
- Are important actions obvious without being loud?\
- Is the product capable without feeling cold?\
\
---\
\
## Technical QA Checklist\
\
- Typography follows the defined hierarchy and spacing rhythm\
- Body text is at least 14px in core app screens\
- Line-height stays at or above 1.5 for primary reading text\
- Color contrast meets WCAG AA or better\
- Interactive states are visually distinct\
- Focus states are visible and consistent\
- Motion stays within 150\'96300ms unless there is a strong reason otherwise\
- Layout uses the 8pt grid consistently\
- Rows, sections, and forms preserve reusable patterns\
- Labels remain plain and consistent across screens\
- Meaning is never conveyed by color alone\
\
---\
\
## Adaptive System Memory\
\
If future JobSignal design files exist, preserve continuity in these areas first:\
- calm neutral palette\
- quiet inbox-style list pattern\
- understated typography\
- restrained action treatment\
- editorial detail view width\
\
Suggested reuse prompt for future iterations:\
- \'93Retain the calm inbox rhythm, thin dividers, and soft neutral palette so the product keeps its trusted morning feel.\'94\
\
If later brand evolution is needed, change only one layer at a time:\
- copy tone first\
- then accent usage\
- then layout density\
- typography last\
\
This prevents emotional drift.\
\
---\
\
## Design Snapshot Output\
\
### Color palette preview\
\
```txt\
Primary Text   #111827   rgb(17, 24, 39)\
Secondary Text #6B7280   rgb(107, 114, 128)\
Background     #F9FAFB   rgb(249, 250, 251)\
Surface        #FFFFFF   rgb(255, 255, 255)\
Divider        #E5E7EB   rgb(229, 231, 235)\
Accent         #4F46E5   rgb(79, 70, 229)\
Success        #16A34A   rgb(22, 163, 74)\
Warning        #D97706   rgb(217, 119, 6)\
Error          #DC2626   rgb(220, 38, 38)\
\
\pard\pardeftab720\sa280\partightenfactor0

\f1\b\fs28 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 Typographic scale\

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrt\brdrnil \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0

\fs24 \cf0 \strokec3 Style\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Size\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Weight\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Line Height\cell 
\pard\intbl\itap1\pardeftab720\qc\partightenfactor0
\cf0 Use\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0

\f2\b0 \cf0 H1\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 32px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 600\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 40px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Page titles, hero\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 H2\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 24px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 600\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 32px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Section titles\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 H3\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 20px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 600\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 28px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Card and detail titles\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 H4\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 16px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 600\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 24px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Compact headers\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Body Large\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 16px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 400\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 24px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Primary reading text\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Body\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 14px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 400\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 22px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Metadata, settings\cell \row

\itap1\trowd \taflags0 \trgaph108\trleft-108 \trbrdrl\brdrnil \trbrdrt\brdrnil \trbrdrr\brdrnil 
\clvertalc \clshdrawnil \clwWidth1135\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx1728
\clvertalc \clshdrawnil \clwWidth480\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx3456
\clvertalc \clshdrawnil \clwWidth733\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx5184
\clvertalc \clshdrawnil \clwWidth1220\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx6912
\clvertalc \clshdrawnil \clwWidth1992\clftsWidth3 \clmart10 \clmarl10 \clmarb10 \clmarr10 \clbrdrt\brdrnil \clbrdrl\brdrnil \clbrdrb\brdrnil \clbrdrr\brdrnil \clpadt20 \clpadl20 \clpadb20 \clpadr20 \gaph\cellx8640
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Caption\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 12px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 500\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 18px\cell 
\pard\intbl\itap1\pardeftab720\partightenfactor0
\cf0 Timestamps, labels\cell \lastrow\row
\pard\pardeftab720\sa280\partightenfactor0

\f1\b\fs28 \cf0 \strokec2 Spacing & layout summary\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\f2\b0\fs24 \cf0 \kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 8pt grid across the product\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 single-column first\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 ranked jobs list max width: 960px\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 reading and onboarding max width: 720px\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 section spacing: 24px to 48px\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 list row padding: 12px to 16px vertical, 16px horizontal\
\ls1\ilvl0\kerning1\expnd0\expndtw0 \outl0\strokewidth0 {\listtext	\uc0\u8226 	}\expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 use dividers before adding card chrome\
\pard\pardeftab720\sa280\partightenfactor0

\f1\b\fs28 \cf0 \strokec2 One-sentence emotional thesis\
\pard\pardeftab720\sa240\partightenfactor0

\fs24 \cf0 \strokec2 JobSignal should feel like a quiet morning inbox that reduces tension, surfaces only what matters, and earns trust through clarity.
\f2\b0 \strokec2 \
\pard\pardeftab720\sa298\partightenfactor0

\f1\b\fs36 \cf0 \strokec2 Design Integrity Review\
\pard\pardeftab720\sa240\partightenfactor0

\f2\b0\fs24 \cf0 \strokec2 The emotional and technical intent align well. The muted palette, restrained typography, inbox-style structure, and forgiving interaction rules all support the central promise of relief over excitement. The biggest opportunity for even stronger harmony is to protect the ranked jobs view from feature creep. If that screen stays simple, narrow in purpose, and highly scannable, the entire product will keep its calm identity.\
}