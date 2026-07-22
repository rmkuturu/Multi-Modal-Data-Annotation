# Hedgehog Multi-Modal Evaluation Toolkit

## Credit and Origin
This project is an independent derivative built from the original repository by [@armaanshk](https://github.com/armaanshk).

Original project:
- Source: https://github.com/armaanshk/Multi-Modal-Data-Annotation
- Original creator: armaanshk

This fork keeps upstream credit intact and extends the project toward multi-modal AI evaluation and review workflows.

## Overview
This project is a lightweight multi-modal review and annotation toolkit for **text**, **image**, and **audio** tasks. It is adapted for evaluation-style work where annotators do more than assign labels: they also assess quality, confidence, ambiguity, and whether an item should be flagged for follow-up review.

## What Makes This Version Different
- Reframed from a basic annotation demo into an evaluation-oriented toolkit
- Adds room for reviewer notes and quality-control thinking
- Better aligned with AI evaluation workflows such as instruction-following review and error flagging
- Preserves creator attribution while extending the project independently

## Core Use Cases
- Text sentiment and quality review
- Image labeling with optional bounding box metadata
- Audio clip categorization and evaluator notes
- Reviewer confidence tracking
- Flagging uncertain or ambiguous samples for second-pass review

## Features
- Text review for Positive / Negative / Neutral items
- Image review with label and optional bounding box coordinates
- Audio review for Speech / Music / Noise items
- Annotation statistics dashboard
- Review guidelines page
- CSV-based annotation saving in `annotations/`

## How to Run
1. Install Python 3.8 or later.
2. Create a virtual environment if needed:
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install streamlit pandas pillow
```
4. Run the app from the project folder:
```bash
streamlit run app_streamlit.py
```

## Project Direction
This fork is being developed as an independent project focused on practical multi-modal evaluation workflows, especially for human review settings where consistency, notes, confidence, and escalation matter.

## Future Improvements
- Add disagreement and consensus tracking
- Add review queues and audit filters
- Add export formats for downstream evaluation pipelines
- Add dataset-level quality dashboards
- Add video support in a future version

## License
MIT
