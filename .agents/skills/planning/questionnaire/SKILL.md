---
name: questionnaire
description: "Turn a decision the user can't answer alone into a questionnaire for someone else (a stakeholder, a domain expert, a customer, another team) to fill in async or in a meeting. Use when the user says 'I need to ask X', 'I don't know, that's for the PM / legal / the client', or when a grilling question is blocked on someone outside the conversation."
---

# Questionnaire

Some answers live in someone else's head. This skill writes the document that gets them out.

**Grill the send, not the subject.** Interview the user only about the send, which they can always answer. The questions in the document then aim at the gap between what the recipient knows and what the user needs.

1. **Who is it going to?** In one exchange, ask for the recipient's role, expertise, and relationship to the user. This sets the tone and how much context the document must carry. Done when you know what the recipient knows that the user doesn't.
2. **What do you need back?** In one exchange, ask for the specific decisions or facts the user needs from this person. Pull candidates from the open questions in the feature folder's briefs and spec (see the `doc-templates` skill) and offer them. Done when there is a concrete list of what the user must be able to decide afterwards.
3. **Write it.** Draft questions aimed at that gap with `QUESTIONNAIRE.md` from the `doc-templates` skill, most important first, grouped by theme once there are more than a handful, one idea per question. Save it to the feature folder as `questionnaire-<recipient>.md`, or the current directory without a feature. Done when every item from step 2 has a question.

When the answers come back, they are input for the `grilling` skill or the `spec` skill. Link the filled questionnaire from whichever document uses it.

## Attribution

Adapted from `skills/productivity/to-questionnaire` in mattpocock/skills (MIT, Matt Pocock). See `THIRD_PARTY_NOTICES.md`.
