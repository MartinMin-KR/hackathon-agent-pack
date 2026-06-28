# Design

## Source of truth
- Status: Active
- Last refreshed: 2026-06-27
- Primary product surfaces: member-6 peer check-in prototype, elder side, worker side, leader dashboard.
- Evidence reviewed: `docs/final-design-spec.md`, `docs/implementation-plan.md`, `team-work/member-6/src/peer-checkin-platform/README.md`, current HTML/CSS/JS.

## Brand
- Personality: warm, plain, calm, trustworthy.
- Trust signals: clear names, visible privacy boundaries, large touch targets, simple next actions.
- Avoid: technical labels, ID-like profile names, dense dashboards on elder-facing screens, medical/emergency overpromising.

## Product goals
- Goals: help older adults exchange small check-ins, choose safe replies, and request help without confusion.
- Non-goals: real matching, diagnosis, emergency dispatch, backend workflows.
- Success signals: users can pick a person, send a reply, understand privacy, and find help in one or two taps.

## Personas and jobs
- Primary personas: older adult user, social worker/operator.
- User jobs: check in with a known neighbor, reply comfortably, ask for help, review recent activity.
- Key contexts of use: mobile first, low confidence with apps, short repeated sessions.

## Information architecture
- Primary navigation: four large actions, with the current action visually selected.
- Core routes/screens: elder prototype home, one-to-one chat, connection list, group chat, help request, worker side.
- Content hierarchy: current status first, primary action second, details only after selection.

## Design principles
- Principle 1: People before system identifiers.
- Principle 2: Every action should explain what happens next.
- Tradeoffs: privacy copy stays visible, but labels use real names in the prototype because the requested demo needs human-readable profiles.

## Visual language
- Color: soft green for primary care actions, blue for support/navigation, coral for help.
- Typography: large Korean-readable labels, no negative letter spacing.
- Spacing/layout rhythm: 8px radius, consistent 12-24px spacing, mobile-safe single-column fallbacks.
- Shape/radius/elevation: restrained panels and cards, no nested decorative cards.
- Motion: no required motion.
- Imagery/iconography: emoji avatars for prototype profiles; no numeric avatars.

## Components
- Existing components to reuse: action buttons, contact cards, network cards, chat messages, quick reply buttons.
- New/changed components: hero status strip, profile summary cards, larger avatar treatment.
- Variants and states: active contact, recent activity, help result, disabled voice input.
- Token/component ownership: CSS variables in `team-work/member-6/src/peer-checkin-platform/styles.css`.

## Accessibility
- Target standard: practical mobile accessibility for hackathon prototype.
- Keyboard/focus behavior: visible focus rings for buttons and links.
- Contrast/readability: avoid pale text for primary labels; keep body text at readable sizes.
- Screen-reader semantics: buttons remain buttons, navigation keeps labels.
- Reduced motion and sensory considerations: no animation required for core use.

## Responsive behavior
- Supported breakpoints/devices: mobile phone first, desktop demo second.
- Layout adaptations: four actions collapse to two then one column; content cards stack.
- Touch/hover differences: touch targets should remain at least 44px high.

## Interaction states
- Loading: not applicable for static prototype.
- Empty: not applicable; seed data is present.
- Error: voice/microphone errors use plain Korean.
- Success: recent activity updates after sends/help selection.
- Disabled: voice input disabled when browser support is missing.
- Offline/slow network, if applicable: static prototype can load without backend.

## Content voice
- Tone: short, respectful, non-technical.
- Terminology: use "이웃", "이름", "도움" rather than "ID", "유저", or "데이터".
- Microcopy rules: one sentence per action where possible; explain boundaries without legal tone.

## Implementation constraints
- Framework/styling system: static HTML, CSS, vanilla JavaScript.
- Design-token constraints: extend existing CSS variables before adding new visual systems.
- Performance constraints: no new dependencies or remote assets.
- Compatibility constraints: browser speech APIs are optional.
- Test/screenshot expectations: run JS syntax check and harness verification after UI changes.

## Open questions
- [ ] Should real names remain in the demo, or should future production return to pseudonyms? Owner: leader. Impact: privacy model.
