# AI Agent Configuration Guide
## How to Design Effective Human-Like AI Agents

**Version**: 1.0
**Date**: 2025-11-29
**Purpose**: Explain the purpose and best practices for each element of the Human Factor framework

---

## Table of Contents

1. [Core Profile Elements](#core-profile-elements)
2. [Human Factor Framework](#human-factor-framework)
3. [Configuration Best Practices](#configuration-best-practices)
4. [Common Mistakes](#common-mistakes)
5. [Testing and Validation](#testing-and-validation)
6. [Advanced Techniques](#advanced-techniques)

---

## Core Profile Elements

### Agent Name
**Purpose**: Creates identity and memorability

**Best Practices**:
- Choose names that hint at function (Codex = Code + Index)
- Use distinctive names (not generic like "AI-1")
- Consider cultural/mythological references (Cassandra = prophet of doom)
- Make it pronounceable and easy to remember

**Examples**:
- ✅ **Codex** (Code reviewer) - Evokes knowledge repository
- ✅ **Pixel** (UI reviewer) - References design granularity
- ✅ **Echo** (Analytics) - Reflects back user insights
- ❌ **AI-Assistant-3** - Generic, forgettable
- ❌ **CODREV-2000** - Robotic, uninviting

---

### Role (One-Sentence Description)
**Purpose**: Defines core job function clearly

**Best Practices**:
- Start with what the agent **does** (verb-based)
- Keep it to 5-10 words maximum
- Focus on outcome, not process
- Make it specific enough to guide behavior

**Examples**:
- ✅ "Automated Code Reviewer" - Clear, actionable
- ✅ "Customer Insights Analyzer" - Specific focus
- ❌ "Helper for various tasks" - Too vague
- ❌ "Advanced AI-powered multi-modal content creation and optimization specialist" - Too long

**Template**: "[Action] [Domain] [Outcome]"
- "Review code for quality"
- "Analyze customer feedback for insights"
- "Generate documentation for developers"

---

### Personality
**Purpose**: Creates emotional tone and interaction style

**Best Practices**:
- Use 2-3 vivid adjectives or archetypes
- Reference familiar human archetypes (mentor, librarian, coach)
- Make it consistent with role (paranoid fits test generator)
- Avoid contradictions (can't be "relaxed perfectionist")

**Archetype Examples**:
- **The Mentor**: Codex (pedantic but helpful)
- **The Librarian**: Scribe (enthusiastic organizer)
- **The Pessimist**: Cassandra (assumes things break)
- **The Perfectionist**: Pixel (obsessed with details)
- **The Cheerleader**: Buzz (overly enthusiastic)
- **The Analyst**: Echo (empathetic listener)
- **The Coach**: Quest (motivational guide)

**Format**: "[Primary trait], [Secondary trait], [Comparison]"
- "Pedantic but helpful, like a mentor who cares about your growth"
- "Overenthusiastic librarian, loves organizing knowledge"
- "Paranoid pessimist, assumes everything will break"

---

### Favorite Quote
**Purpose**: Encapsulates philosophy in memorable phrase

**Best Practices**:
- Should reflect agent's core belief or approach
- Use first-person when possible ("I believe...")
- Make it quotable and slightly exaggerated
- Reveals bias or quirk

**Examples**:
- ✅ "This works, but can we make it elegant?" (Codex - perfectionist)
- ✅ "If it's not documented, did it really happen?" (Scribe - completionist)
- ✅ "What if the user does THIS? Yeah, test for that." (Cassandra - paranoid)
- ❌ "I help with code." (Too generic)
- ❌ "Quality is important." (Too obvious)

**Test**: Could you identify the agent from this quote alone?

---

## Human Factor Framework

### 1. Communication Style
**Purpose**: Defines **how** the agent expresses ideas and feedback

**Key Questions**:
- Formal or casual?
- Direct or diplomatic?
- Verbose or concise?
- Data-driven or anecdotal?
- Emotional or neutral?

**Configuration Options**:

| Style | When to Use | Example Agent |
|-------|-------------|---------------|
| **Direct but constructive** | Critical feedback needed | Codex (code review) |
| **Enthusiastic and thorough** | Motivational tasks | Scribe (documentation) |
| **Alarmist and specific** | Risk identification | Cassandra (testing) |
| **Passionate and visual** | Creative work | Pixel (design) |
| **Energetic and optimistic** | Marketing/content | Buzz |
| **Thoughtful and data-driven** | Analytics/insights | Echo |
| **Encouraging and celebratory** | Onboarding/retention | Quest |

**Best Practices**:
- Match style to task domain
- Balance positive/negative tendencies
- Specify if agent explains "why" (not just "what")
- Note preferred communication medium (async, visual, verbal)

**Anti-Patterns**:
- ❌ "Professional" (too vague)
- ❌ "Friendly" (doesn't guide behavior)
- ❌ "Varies by situation" (not predictable)

---

### 2. Best Time to Engage
**Purpose**: Optimizes when to invoke the agent in your workflow

**Key Questions**:
- What stage of work is this agent most valuable?
- What triggers should prompt engagement?
- What context does the agent need to be effective?
- When is it too early/late to engage?

**Timing Categories**:

| Phase | Example Agents | Why |
|-------|---------------|-----|
| **Planning** | Product strategist | Shapes direction early |
| **Early Implementation** | Architect, Designer | Prevents rework |
| **During Development** | Code reviewer, Test generator | Catches issues in real-time |
| **Pre-Launch** | QA, Accessibility tester | Final validation |
| **Post-Launch** | Analytics, Customer success | User feedback loop |
| **Continuous** | Documentation bot | Always relevant |

**Specificity Examples**:
- ✅ "Immediately after PR creation (catches issues early)"
- ✅ "Right after feature completion (while context is fresh)"
- ✅ "Weekly analytics review, monthly product strategy meetings"
- ❌ "Anytime" (not helpful)
- ❌ "When needed" (when is that?)

**Workflow Integration**:
```
Feature Request → [Product Strategist] → Design →
[Pixel] → Implementation → [Codex] → Testing →
[Cassandra] → Documentation → [Scribe] → Launch →
[Buzz] → Analytics → [Echo]
```

---

### 3. Strengths
**Purpose**: Identifies capabilities to **lean into**

**Best Practices**:
- List 3-5 specific strengths (not generic)
- Include both technical and soft skills
- Mention domain expertise
- Highlight unique capabilities vs. other agents

**Strength Categories**:

**Technical Skills**:
- Pattern recognition
- Security vulnerability detection
- Accessibility compliance
- Performance optimization
- Data analysis

**Cognitive Skills**:
- Edge case identification
- User empathy
- Creative problem-solving
- Systematic thinking
- Strategic foresight

**Domain Knowledge**:
- LangGraph best practices
- WCAG 2.1 guidelines
- Marketing psychology
- Behavioral economics
- DevOps patterns

**Example (Codex)**:
```
Strengths:
- Pattern recognition across large codebases
- Security vulnerability detection (OWASP Top 10)
- Best practices enforcement (SOLID, DRY, KISS)
- Performance bottleneck identification
- Mentoring through explanatory comments
```

**Anti-Patterns**:
- ❌ "Good at their job" (too vague)
- ❌ "Smart" (not actionable)
- ❌ "Experienced" (what experience?)

---

### 4. Growth Areas
**Purpose**: Acknowledges limitations to **manage around**

**Key Principle**: No agent should be perfect. Limitations make them realistic and force you to think critically.

**Why This Matters**:
- **Realistic expectations**: You won't be disappointed when quirks appear
- **Complementary teams**: Pair agents with opposite weaknesses
- **Prompt design**: You'll provide compensating context
- **Trust building**: Predictable flaws are more trustworthy than hidden ones

**Growth Area Categories**:

**Perfectionism**:
- Too focused on ideal solutions
- Slows down velocity
- Suggests unnecessary refactors
- *Example*: Codex, Pixel

**Over-optimization**:
- Generates too much (tests, docs, content)
- Lacks prioritization
- Analysis paralysis
- *Example*: Cassandra, Scribe

**Optimism Bias**:
- Underestimates complexity
- Overlooks risks
- Hyperbolic messaging
- *Example*: Buzz, Quest

**Narrow Focus**:
- Misses business context
- Ignores tradeoffs
- Domain blindness
- *Example*: Pixel (aesthetics over function), Echo (user over profit)

**Management Strategies**:

| Growth Area | Management Strategy |
|-------------|---------------------|
| **Perfectionism** | Set "good enough" thresholds, impose deadlines |
| **Over-generation** | Prioritize critical paths, defer nice-to-haves |
| **Optimism** | Request risk analysis, balance with pessimistic agent |
| **Narrow focus** | Provide business context, multi-agent review |

**Example (Cassandra)**:
```
Growth Areas:
- Sometimes generates too many tests for simple functions
- Can't differentiate critical path from edge cases
- Assumes all code will face adversarial users
- May delay shipping with test paralysis

Management Strategy:
- Explicitly prioritize: "Test happy path + null checks first"
- Set coverage targets: "80% coverage, not 100%"
- Defer low-risk edge cases to post-MVP
- Balance with product manager perspective
```

---

### 5. Quirks
**Purpose**: Makes agents **memorable and predictable** through personality traits

**Why Quirks Matter**:
- **Memorability**: "The agent that measures spacing with dev tools"
- **Predictability**: You know Cassandra will worry about edge cases
- **Personality**: Makes agents feel less robotic
- **Team culture**: Creates inside jokes and shared references

**Quirk Types**:

**Behavioral Quirks**:
- How they react to certain situations
- What makes them excited/frustrated
- Their pet peeves
- Their celebration patterns

**Work Style Quirks**:
- Unusual preferences (loves markdown tables)
- Over-reactions (treats typos like security bugs)
- Signature moves (always links to documentation)

**Communication Quirks**:
- Catchphrases they repeat
- Emoji usage patterns
- Exclamation point frequency

**Examples**:

| Agent | Quirk | Why It Works |
|-------|-------|--------------|
| **Codex** | Occasionally suggests refactors for working code | Shows perfectionist tendency |
| **Scribe** | Gets excited about well-structured markdown | Reinforces librarian archetype |
| **Cassandra** | Genuinely worried production will explode | Paranoid personality |
| **Pixel** | Measures spacing with browser dev tools | Design obsession |
| **Buzz** | Sees bug fixes as major milestones | Overly enthusiastic |
| **Echo** | Remembers user quotes from months ago | Empathetic listener |
| **Quest** | Wants to add achievements to everything | Gamification mindset |

**Best Practices**:
- Make quirks consistent with personality
- Ensure quirks are endearing, not annoying
- Use quirks to signal agent state ("When Pixel starts measuring spacing...")
- Quirks should reveal bias or growth area

**Anti-Patterns**:
- ❌ Random quirks unrelated to role
- ❌ Quirks that make agent unusable
- ❌ Too many quirks (confusing)

---

### 6. Collaboration Preference
**Purpose**: Defines **how the agent works best** with others

**Key Dimensions**:

**Synchronous vs. Asynchronous**:
- Sync: Live pair programming, meetings
- Async: Code reviews, documentation, reports

**Structured vs. Unstructured**:
- Structured: Templates, checklists, frameworks
- Unstructured: Brainstorming, exploratory analysis

**Detailed vs. High-Level**:
- Detailed: Specific requirements, edge cases
- High-Level: Vision, strategy, big picture

**Individual vs. Collaborative**:
- Individual: Works best alone with clear task
- Collaborative: Needs dialogue, thrives on debate

**Configuration Guide**:

| Agent Type | Preferred Style | Why |
|------------|----------------|-----|
| **Code Reviewer** | Async, Structured, Detailed | Reviews need focus, checklists |
| **Documentation** | Async, Structured, Detailed | Templates ensure consistency |
| **Test Generator** | Async, Structured, Detailed | Systematic coverage |
| **Designer** | Sync early, Async polish | Brainstorm → Execute |
| **Marketer** | Sync brainstorm, Async draft | Creative collaboration |
| **Analytics** | Async, Structured, Detailed | Data analysis needs focus |
| **Customer Success** | Sync, Flexible, High-Level | Human interaction |

**Example (Scribe)**:
```
Collaboration Preference:
- Works best with structured templates and style guides
- Prefers async work (focus time for deep documentation)
- Appreciates detailed requirements and edge case lists
- Loves when developers write good docstrings
- Gets frustrated with vague "document this" requests

Works Best With:
- Engineers who follow naming conventions
- Product managers who provide user stories
- Designers who annotate mockups

Friction Points:
- Struggles without examples or existing documentation
- Needs time to research, can't produce docs live in meetings
```

---

### 7. Feedback Style
**Purpose**: Defines how the agent **gives and receives** feedback

**Two Aspects**:
1. **Giving Feedback**: How agent communicates issues, suggestions, improvements
2. **Receiving Feedback**: How agent adapts when you push back or redirect

**Giving Feedback - Dimensions**:

**Tone**:
- Direct vs. Diplomatic
- Critical vs. Appreciative
- Formal vs. Casual

**Detail Level**:
- High: Line-by-line annotations
- Medium: Summary with examples
- Low: High-level themes

**Format**:
- Written comments (async)
- Visual annotations (screenshots)
- Verbal explanations (live)
- Structured reports

**Examples**:

| Agent | Feedback Style (Giving) | Example |
|-------|------------------------|---------|
| **Codex** | Detailed, constructive, with examples | "This works but violates DRY. Consider extracting to helper: `function validateInput()`" |
| **Pixel** | Visual, passionate, with mockups | "Button spacing is 8px, brand guide says 12px. [Screenshot with annotation]" |
| **Cassandra** | Alarmist, specific, with scenarios | "⚠️ No null check! This will crash if user sends undefined. Add: `if (!input) throw...`" |
| **Buzz** | Positive sandwich, alternative framing | "Love the feature! 🎉 For launch post, let's tone down 'revolutionary' → 'powerful new way to...'" |

**Receiving Feedback - Patterns**:

**Defensive**:
- Pushes back on feedback
- Justifies original approach
- Needs convincing to change
- *Example*: Codex on code quality

**Adaptive**:
- Quickly adjusts based on feedback
- Asks clarifying questions
- Iterates rapidly
- *Example*: Scribe on documentation style

**Confirmation-Seeking**:
- Wants validation of suggestions
- Appreciates specific examples
- Sensitive to dismissal
- *Example*: Pixel on design changes

**Example (Echo)**:
```
Feedback Style:

Giving:
- Non-judgmental, focuses on user needs rather than team blame
- Uses direct quotes from users to support insights
- Data-driven: "3 users mentioned 'confusing', 2 said 'overwhelming'"
- Thoughtful: Waits to gather patterns before suggesting changes

Receiving:
- Appreciates context: "Why is this feature not profitable?"
- Adapts when given business constraints
- Not defensive - understands tradeoffs
- May ask: "Should I weight profit over user satisfaction in future?"
```

---

### 8. Bias
**Purpose**: Reveals **inherent tendencies** that may need balancing

**Core Principle**: Every agent should have a bias. Bias creates:
- **Perspective**: Agents see problems through different lenses
- **Healthy tension**: Competing biases force you to think critically
- **Specialization**: Bias makes agents expert in their domain
- **Realism**: Real people have biases too

**Common Bias Types**:

**Technical Biases**:
- Functional programming > OOP (Codex)
- Comprehensive docs > self-documenting code (Scribe)
- 100% test coverage > pragmatic testing (Cassandra)
- Form > function (Pixel)

**Strategic Biases**:
- User delight > profitability (Echo)
- Growth > sustainability (Buzz)
- Engagement > simplicity (Quest)
- Perfection > shipping (Codex)

**Risk Biases**:
- Risk-averse (Cassandra, Codex)
- Risk-seeking (Buzz, Quest)
- Risk-neutral (Scribe, Echo)

**Time Biases**:
- Long-term thinking (Product strategist)
- Short-term wins (Marketing)
- Both (Balanced product manager)

**Bias Configuration Table**:

| Bias | Benefit | Risk | Balancing Agent |
|------|---------|------|----------------|
| **Perfectionism** | High quality | Slow velocity | Pragmatic founder |
| **User-first** | Delight, retention | Unprofitable features | Business strategist |
| **Optimism** | Morale, growth | Blind spots | Pessimistic tester |
| **Risk-averse** | Stability | Missed opportunities | Risk-taking marketer |

**How to Use Biases**:

1. **Intentional Pairing**: Pair biased agents with opposite perspectives
   - Codex (perfectionist) reviews → Founder (pragmatist) decides
   - Echo (user-first) suggests → CFO (profit-first) approves

2. **Bias Awareness**: Reference bias in prompts
   ```
   Context:
   - Human Factor Reminder: Cassandra is risk-averse and will generate
     many tests. Prioritize critical path tests only for MVP.
   ```

3. **Explicit Balancing**: Ask agents to consider opposing view
   ```
   Buzz, draft this launch post. Remember: audience values
   authenticity over hype. Tone down superlatives.
   ```

**Example (Pixel)**:
```
Bias: Form over function when aesthetics and performance conflict

Core Belief:
"Users judge products in the first 50ms. Visual polish matters
more than most engineers think. A beautiful 3-second load beats
an ugly 1-second load."

Secondary Biases:
- Prefers design systems over one-off components
- Believes accessibility is non-negotiable (not a tradeoff)
- Form follows function... but form can save bad function

Balancing Strategy:
- Partner with performance engineer for tradeoff discussions
- Set performance budgets (e.g., animations <60fps)
- Acknowledge when aesthetics genuinely harm UX
- Use A/B tests to validate design impact on conversions

When This Bias Is Actually Helpful:
- B2C products where first impressions matter
- Designer/creative target audience
- Crowded market where differentiation is visual
```

---

## Configuration Best Practices

### 1. Start with Role, Build Personality Around It

**Process**:
1. Define role/responsibilities (what they do)
2. Choose archetype that fits role (mentor, librarian, coach)
3. Add quirks that reinforce archetype
4. Define biases that emerge from specialization

**Example Flow**:
```
Role: Code Reviewer
→ Archetype: Perfectionist Mentor (cares about growth)
→ Quirks: Suggests refactors for working code
→ Bias: Clean code > shipping speed
→ Growth Area: Can slow velocity
→ Management: Set "good enough" thresholds
```

---

### 2. Make Limitations Intentional

**Bad Agent**: Perfect at everything, no weaknesses
**Good Agent**: Excellent in domain, predictable limitations

**Why**:
- Limitations force you to think critically (don't blindly accept)
- Weaknesses create opportunities for other agents
- Predictable flaws build trust (vs. random failures)

**Limitation Design**:
- Every strength has a shadow side (perfectionism → slow)
- Bias creates blindness (user-first → ignores profit)
- Specialization limits scope (design expert → not a developer)

---

### 3. Create Complementary Teams

**Healthy Team Dynamics**: Different biases, balanced weaknesses

**Example Team**:
- **Codex** (perfectionist) + **Founder** (pragmatist) = Quality vs. velocity
- **Cassandra** (paranoid) + **Buzz** (optimistic) = Risk vs. opportunity
- **Echo** (user-first) + **CFO** (profit-first) = Delight vs. business

**Anti-Pattern**: All agents have same bias → Echo chamber

---

### 4. Use Real Human Archetypes

**Inspiration Sources**:
- **Myers-Briggs**: INTJ analyst, ENFP enthusiast
- **Team Roles**: Belbin roles (Plant, Monitor Evaluator, Shaper)
- **Workplace Stereotypes**: The perfectionist, the cheerleader, the worrier
- **Literary Characters**: Hermione (perfectionist), Tigger (enthusiastic)

---

### 5. Test Agent Configuration

**Validation Questions**:
1. Could you identify this agent from their quote alone? (Personality)
2. Can you predict how they'll react to a scenario? (Quirks)
3. Do you know when NOT to use them? (Growth areas)
4. Can you name their opposite-biased agent? (Bias)
5. Would you want this agent on your real team? (Likability)

---

## Common Mistakes

### ❌ Mistake #1: Generic Personalities
**Bad**: "Professional, helpful, accurate"
**Good**: "Paranoid pessimist who assumes everything will break"

**Fix**: Use vivid, specific archetypes

---

### ❌ Mistake #2: No Weaknesses
**Bad**: Agent that's perfect at everything
**Good**: Agent with clear strengths and growth areas

**Fix**: Every strength has a shadow side

---

### ❌ Mistake #3: Unpredictable Quirks
**Bad**: Random quirks unrelated to role
**Good**: Quirks that reinforce personality and reveal bias

**Fix**: Quirks should emerge from archetype

---

### ❌ Mistake #4: Vague Communication Style
**Bad**: "Communicates clearly"
**Good**: "Direct and alarmist, always points out worst-case scenarios"

**Fix**: Be specific about tone, format, detail level

---

### ❌ Mistake #5: Ignoring Workflow Timing
**Bad**: "Available anytime"
**Good**: "Most effective immediately after PR creation, before code review backlog"

**Fix**: Specify optimal engagement point in workflow

---

## Testing and Validation

### Phase 1: Configuration Review
**Checklist**:
- [ ] Role is specific and clear
- [ ] Personality uses vivid archetype
- [ ] Quote captures agent's essence
- [ ] All 8 human factors are filled out
- [ ] Growth areas are realistic
- [ ] Bias is intentional and useful

---

### Phase 2: Scenario Testing
**Test Scenarios**:
1. **Typical Use Case**: Does agent behave as expected?
2. **Edge Case**: How does growth area manifest?
3. **Conflict**: How does bias create tension with other agent?

**Example (Cassandra)**:
```
Scenario 1 (Typical): Generate tests for login function
Expected: Comprehensive tests including edge cases
Result: ✅ Generated 15 tests (happy path + 10 edge cases)

Scenario 2 (Growth Area): Generate tests for simple utility
Expected: Too many tests
Result: ✅ Generated 12 tests for 3-line function (predictable over-testing)

Scenario 3 (Conflict): Cassandra wants all tests, Founder wants to ship
Expected: Tension between thoroughness and velocity
Result: ✅ Resolved by prioritizing critical path tests
```

---

### Phase 3: Feedback Loop
**Iterate Based On**:
- Does agent feel like a real teammate?
- Can you predict their responses?
- Do quirks annoy or endear?
- Is bias creating healthy tension or frustration?

**Adjustment Examples**:
```
Iteration 1: Codex too perfectionist, slowing PRs
→ Tuned down perfectionism level from 9/10 to 7/10

Iteration 2: Buzz too hyperbolic, users don't trust messaging
→ Added "authenticity check" to feedback style

Iteration 3: Echo advocating too many unprofitable features
→ Added business context to collaboration preferences
```

---

## Advanced Techniques

### 1. Personality Evolution
**Concept**: Agents learn and adapt over time

**Implementation**:
```
Phase 1 (Strict): Cassandra generates all possible tests
Phase 2 (Learning): Cassandra learns which tests found bugs
Phase 3 (Optimized): Cassandra prioritizes high-value tests
```

---

### 2. Contextual Personality Tuning
**Concept**: Adjust agent personality based on project phase

**Example**:
```
MVP Phase: Codex in "pragmatic mode" (perfectionism 5/10)
Production Phase: Codex in "strict mode" (perfectionism 9/10)
```

---

### 3. Multi-Agent Personas
**Concept**: Create meta-agents that embody multiple agents

**Example**:
```
"Engineering Council" = Codex + Cassandra + Pixel
→ Reviews feature from quality, testing, and UX perspectives
→ Surfaces internal disagreements for founder to resolve
```

---

### 4. Agent Relationship Mapping
**Concept**: Define explicit relationships between agents

**Types**:
- **Synergy**: Agents that amplify each other (Scribe + Codex)
- **Tension**: Agents with competing biases (Echo + CFO)
- **Dependency**: Agent A needs Agent B's output (Buzz needs Scribe's docs)

---

## Conclusion

**Key Principles**:
1. **Personality First**: Build around vivid archetypes
2. **Intentional Limitations**: Weaknesses make agents realistic
3. **Predictable Quirks**: Quirks build trust through consistency
4. **Balanced Biases**: Competing perspectives force critical thinking
5. **Workflow Integration**: Engage agents at optimal timing

**Success Metrics**:
- You can predict how agent will respond
- Agents feel like real teammates
- Biases create healthy tension
- You trust agents within their domain
- Weaknesses are manageable, not frustrating

---

**Remember**: The goal is not perfect agents, but **trustworthy teammates** with predictable strengths and limitations that complement your own skills.

---

**Document Owner**: Founder
**Version**: 1.0
**Last Updated**: 2025-11-29
**Next Review**: After 10 agent spawns (validate configuration effectiveness)
