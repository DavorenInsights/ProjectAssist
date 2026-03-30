# Critical review and amendments

## What was weak in the original version

1. The visual language was much darker and more futuristic than the official Just Energy Transition site. The app looked like a cyber dashboard rather than a programme support tool.
2. The home-page navigation cards used JavaScript `onclick` blocks inside raw HTML. In Streamlit this is brittle and can fail depending on rendering and deployment context.
3. The example project funding badges were sliced using string indexes, which produced misleading outputs like `R12M` for `12,500,000` and `R6M` for `6,800,000`.
4. Session-state initialization was duplicated manually instead of being centralized.
5. User-entered content in the summary and PDF path was not escaped before being injected into HTML or ReportLab paragraphs. That creates display breakage risk whenever an applicant types `&`, `<`, `>` or pasted markup.
6. The framing was still too close to an assessment tool. For your intended pitch, the wording needs to emphasise applicant support and quality uplift before formal review.

## What was changed

- Reworked the shared theme to a lighter palette aligned to the JET logo impression: green, orange, charcoal, white, and soft grey backgrounds.
- Refactored shared helpers into `utils/styles.py`.
- Replaced brittle `onclick` tiles with anchor-based navigation tiles.
- Fixed compact funding display on example cards.
- Tightened the product language to position the app as a support wizard rather than a rejection-oriented checker.
- Escaped user content in the summary renderer and PDF export flow.

## Files changed

- `styles.css`
- `utils/styles.py`
- `app.py`
- `pages/5_Summary_Export.py`

## Still recommended next

1. Move repeated default field dictionaries into one shared config file.
2. Add a simple scoring rubric per section so the applicant sees where the application is weak.
3. Add a reviewer checklist tab using the actual categories usually applied by the PMO.
4. Add export to Word in addition to PDF later, because applicants often edit Word more easily.
5. Replace the placeholder JET badge with an approved programme logo asset once you have the official file.
