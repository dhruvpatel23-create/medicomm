# MediComm UI/UX audit — pre-redesign

Audit date: 2026-06-28  
Baseline checkpoint: `dda1452`

## Executive summary

The current product proves the main workflows—authentication, practice, leaderboards, communities, profiles, and duels—but presents them as a prototype rather than a cohesive medical learning workspace. The largest usability problem is not color or decoration: every surface has nearly the same visual weight, so students must read the entire page to understand what matters next. Navigation, system feedback, and learning-state feedback need a shared hierarchy.

The redesign should preserve the existing backend behaviors and question bank while introducing a calmer application shell, stronger page hierarchy, clearer status semantics, responsive navigation, accessible controls, and reusable primitives.

## Global issues

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Logged-out users see an account form instead of a useful landing experience | Students cannot understand the value or inspect the product before committing | Combine a credible product introduction with a focused authentication card and guest access |
| Flat top navigation treats every destination as equally important | Seven peer links increase scan time and do not distinguish study, community, and account jobs | Use grouped desktop sidebar navigation, compact mobile bottom navigation, and contextual page headers |
| Nearly every block uses the same white card treatment | Primary actions, supporting information, and passive metadata compete for attention | Introduce clear surface levels, fewer borders, restrained shadows, and intentional emphasis |
| Typography relies on small sizes and weak hierarchy | Dense medical content becomes tiring and headings do not orient the user quickly | Use a consistent type scale, 16px base reading size, tighter heading line-height, and readable measure |
| Spacing is inconsistent and not visibly based on a system | Pages feel assembled rather than designed; related controls do not always read as groups | Apply an 8px spacing grid with consistent page, section, card, and control gaps |
| Text abbreviations are used as icons | Labels such as `MCQ`, `ACT`, `HUB`, and `VS` add interpretation cost and feel unfinished | Replace with familiar Lucide icons plus accessible labels |
| Several strings show encoding corruption | Broken symbols reduce trust and can obscure feedback | Remove emoji/content glyph dependencies and use SVG icons or plain text |
| Loading is mostly a sentence in a card | The page jumps after data arrives and appears stalled | Add dimensionally stable skeletons for cards, lists, and question content |
| Errors are visually similar to ordinary copy | Students can miss failures and do not always get a clear recovery action | Add dedicated error states with icon, explanation, retry, and safe navigation |
| Empty states are generic | They explain absence but rarely guide the next useful action | Add contextual next steps and lightweight illustrations/icons |
| Destructive or consequential actions lack confirmation | Leaving a duel, logging out, or discarding progress can happen accidentally | Add accessible confirmation dialogs for consequential actions |
| Theme controls communicate with words only | The control consumes space and is slower to parse | Use sun/moon icons, persistent preference, system-aware default, and visible focus states |
| Focus and keyboard behavior are inconsistent | Keyboard and assistive-technology users can lose position or miss state | Standardize `:focus-visible`, labels, live regions, dialog focus, and keyboard shortcuts |
| Motion is not governed by a policy | Some animated areas can distract while most transitions feel abrupt | Use short purposeful motion and honor `prefers-reduced-motion` |
| The client is concentrated in one very large component | Repeated patterns drift and changes become risky | Introduce reusable primitives and modular page components incrementally |

## Authentication and onboarding

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| No guest login | Curious students must create an account before evaluating the product | Add a clearly scoped guest session with local-only progress and upgrade prompts |
| Login and signup have no inline field validation | Errors arrive late and are not attached to the field that needs attention | Validate on blur/submit, show concise inline guidance, and retain entered values |
| Signup asks for all details in one undifferentiated form | The form feels heavier than it is | Group identity and academic details, mark optional fields, and explain why college is requested |
| No password recovery or trust cues | Users may assume a missing production capability | Provide a future-ready recovery affordance and clear privacy/security copy |
| No onboarding after first entry | New users land on a dense dashboard without an obvious first win | Add a three-step checklist: choose exam, select weak subjects, complete a short diagnostic |

## Landing page and marketing

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Hero language emphasizes “gamified” learning | It can make a serious medical platform feel recreational | Lead with focused exam preparation, evidence, and measurable progress |
| No product preview or workflow explanation | Benefits remain abstract | Show a compact dashboard/MCQ preview and a three-step learning loop |
| No pricing surface | Students cannot understand future plan boundaries | Add transparent plan comparison and a payment-gateway-ready checkout section |
| Footer is missing | Legal, support, product, and contact destinations have no stable home | Add a responsive structured footer |

## Dashboard and analytics

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Dashboard is a set of independent cards without a dominant next action | Students must decide what to do from scratch every visit | Lead with “continue studying,” then show weekly goal and actionable recommendations |
| Statistics lack timeframe and trend context | A number alone does not tell the learner whether performance is improving | Add periods, deltas, sparklines/progress, and accessible trend descriptions |
| No weekly graph or study heatmap | Habit formation and consistency are invisible | Add weekly activity chart and 12-week study heatmap |
| Activity feed reports platform totals rather than personal learning events | It is not useful for the student’s next decision | Prefer personal recent practice, battles, milestones, and review items |
| Recommended topics and upcoming exams are absent | The dashboard does not support planning | Add prioritized recommendations and exam countdowns |
| Analytics has no dedicated page | Deeper subject and accuracy analysis cannot be explored | Add an analytics surface with subject mastery, accuracy trend, and time distribution |

## Practice and MCQ solving

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Subject discovery is visually dense for a large bank | Scanning many subjects and years becomes slow | Add search, exam/year filters, progress sorting, and clearer subject cards |
| Question progress can become a very long horizontal strip | It is difficult on mobile and for large sets | Use compact paged/scrollable progress with answered, flagged, and current semantics |
| Question and supporting metadata compete for attention | The core task is not distraction-free | Constrain reading width and separate session controls from question content |
| No sticky timer/session header | Students lose pacing information while scrolling | Add a sticky, low-noise session bar with time and progress |
| No confidence selector or flag-for-review | Students cannot capture uncertainty for later revision | Add confidence and review controls before advancing |
| Explanation is embedded rather than an optional drawer | Long explanations push the next action below the fold | Use an accessible explanation drawer/panel after submission |
| No keyboard shortcuts | High-volume practice requires unnecessary pointer work | Support 1–4 answer selection, Enter submit/next, F flag, and ? help |
| Correctness is communicated heavily through color | Color-vision users may miss meaning | Add icons and explicit labels in addition to semantic colors |

## Leaderboard

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Top performers are rendered like the rest of the list | The main competitive story has no focal point | Add an accessible top-three podium on wide screens and ranked cards on mobile |
| Filters focus on state search only | Students cannot compare by college, period, or cohort | Add period, college/state, and scope filters with clear reset behavior |
| Rating lacks level/badge context | The number has little emotional or educational meaning | Add XP level, badge, and progress-to-next-level |
| Rank changes are not visible | Users cannot tell whether recent effort mattered | Show directional deltas with subtle motion and text equivalents |

## Communities and discussion

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Community creation, discovery, inbox, chat, and members compete on one dense surface | The page becomes cognitively expensive and especially difficult on smaller screens | Separate directory and room states with clear tabs and responsive panels |
| Polling can update content without obvious status | Users may not understand freshness or network failures | Show connection state, last update, skeletons, and non-blocking retry |
| Search is scoped to direct messages and is visually buried | Finding peers or discussions is slower than necessary | Provide a unified search entry with scoped result groups |
| Empty chat/community states are passive | New communities can feel broken | Offer prompts, suggested discussion starters, and direct creation actions |

## 1v1 battles

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Lobby does not clearly explain rated vs bot consequences | Students may enter a rating-changing match unintentionally | Present mode cards with duration, rating impact, and question count before starting |
| Leaving/ending a match has no confirmation | Accidental forfeits are high-cost | Add a confirmation dialog with explicit rating impact |
| Live match layout is card-like rather than task-focused | Timer, score, and answer options compete visually | Use a dedicated arena layout with sticky scoreboard and calm answer controls |
| Result state gives scores but little learning value | The student cannot identify what to review | Add accuracy, pacing, missed-topic summary, and rematch/review actions |

## Profile, settings, pricing, and payments

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Profile mixes public identity, editable details, and account actions | It is unclear what other users see and what is private | Separate public profile summary from personal/account settings |
| Settings page is absent | Theme, notifications, privacy, exam target, and accessibility lack a home | Add grouped settings with explicit save states |
| Pricing page and billing state are absent | Future monetization would require invasive UI changes | Add plan cards, billing summary, and a provider-neutral payment gateway boundary |
| Payment UI could tempt premature card handling | Storing raw payment details would create security risk | Keep only plan/order/provider/status contracts; redirect sensitive entry to a PCI-compliant provider later |

## Responsive and performance concerns

| Issue | Why it hurts usability | Redesign response |
| --- | --- | --- |
| Mobile navigation repeats every desktop destination | Small screens become crowded and labels lose meaning | Keep four primary mobile destinations plus a “More” sheet |
| Dense multi-column community and practice layouts collapse late | Intermediate tablet widths can become cramped | Use content-driven breakpoints and single-purpose mobile panels |
| Large question-bank payload and monolithic app delay interaction | Users pay for code/data they may not need | Lazy-load heavy pages/data, split reusable modules, and keep stable skeleton dimensions |
| Images do not consistently reserve dimensions | Content can shift when clinical images load | Add explicit aspect ratios, lazy loading, decoding hints, and bounded containers |
| No dedicated reduced-motion treatment | Motion-sensitive users may experience discomfort | Disable nonessential transforms and shorten transitions under reduced-motion preference |

## Implementation priorities

1. Shared tokens, accessible primitives, typography, and responsive shell.
2. Authentication/guest entry and onboarding.
3. Dashboard and practice/MCQ workflow.
4. Leaderboard, battles, communities, profile, and settings.
5. Pricing/payment boundary, landing page, and footer.
6. Loading/empty/error/confirmation coverage, keyboard behavior, and performance polish.
