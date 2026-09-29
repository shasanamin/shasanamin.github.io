# Publication illustrations

Each paper uses one wordless pictorial explanation of its research mechanism. Use concrete scenes: a lens looking inside a network, an AI anticipating a recipient's choices, or several answers retained for one prompt. These are conceptual reading aids, not experimental results.

Use flat shapes, open space, sage people, slate AI chips, and ochre for the important intervention. A layered network belongs where the network itself is the subject. Thought bubbles, advice cards, lenses, and calendars are useful when they explain the research. Avoid decorative circuitry, gloss, excessive arrows, or in-image labels.

This direction draws inspiration from [Ming Yin's publication illustrations](https://mingyin.org/), particularly the support-vector magnifier and AI anticipating human behavior. The current illustrations were newly generated; reference files are not shipped.

## Concepts

| Paper asset | Concept and interpretation |
| --- | --- |
| `arxiv26-simple-diffusion` | One model feeds an adjustable gold sampler dial, followed by three distinct text cards. The intervention is in sampling, not retraining; separate outputs acknowledge the paper's quality-and-diversity evaluation. No numerical speedup, universal sharpening benefit, or exact recovery of the data distribution is implied. |
| `arxiv26-scale-invariant-instability` | Two norm contours share a starting direction. An inward arrow depicts weight shrinkage, while the larger turn at the smaller radius illustrates how shrinking the norm can enlarge the effective directional step. A schedule slider cues control. This is schematic geometry, not a measured trajectory, a literal limit cycle, or guaranteed instability. |
| `icml26-consistent-diffusion` | Denoising token rows and a shortcut make faster language reconstruction tangible; no exact speedup or identical stochastic samples is implied. |
| `acl26-fallback-to-frontline` | Two observers consider the same group's perspective. Neither is crowned the winner and their judgments are not fused. |
| `arxiv26-escaping-mode-lottery` | One prompt and several retained answers convey conditional diversity in multi-response training. |
| `chi26-critical-thinking` | A person holds their own argument sheet and uses a pencil to reconsider a tentative reason-to-conclusion link. A smaller AI chip supports the magnifying lens focused on that link. Human ownership and revision are explicit; no AI prediction or guaranteed correction is shown. |
| `aaai26-adaptive-ensembles` | Overlap versus gap filling makes aligned and complementary expertise visible; the switch represents selection, not averaging. |
| `kdd25-support-vector-effect` | Looking inside a network reveals SVM-like behavior. Highlighted examples must be nearest the boundary on both sides. |
| `hcomp24-mix-and-match` | Different uses of an advice card illustrate heterogeneous reliance; the pictured behaviors are examples, not an exhaustive taxonomy. |
| `ijcai24-behavior-aware-ai` | The AI's thought bubble contains its recipient's possible behavior, making behavior-aware assistance explicit. |
| `neurips23-workshop-support-vector-attribution` | A repeated stamp on distinct same-class queries illustrates loss of instance-specific attribution, not document approval. |
| `icml23-workshop-human-reactions` | A modest confidence dial and offered advice illustrate the behavioral reliance assumption used in training. |
| `isi20-phishcasting` | Calendar, history, and a future phishing message express forecasting ahead of attacks, not blocking them. |
| `icdmw20-phishing-prediction` | Combining forecast sheets expresses generative-model and base-predictor fusion, not synthetic input augmentation. |

## Replacement workflow

The site uses transparent 480 × 480 WebPs in `files/`, rendered at 140px on desktop and 96px on mobile. One asset serves both themes.

1. Back up the current asset under ignored `bkp/`.
2. Read the paper and choose one concrete relationship. Generate a distinct square, wordless composition.
3. Review scientific meaning and legibility at both display sizes against white and `#1c1c1d`. Check real alpha through gaps and bubble interiors, not a painted checkerboard.
4. Export with `cwebp -q 88 -resize 480 480 input.png -o files/venueYY-paper.webp`. Preserve filenames and citation links; update `image_alt` in `_data/publications.yml` to match the actual scene.
5. Build at root and a test subpath, run `scripts/check_site.py`, and inspect both themes and mobile layouts.

Reusable prompts live in private `publication-figures_local.md`. This round's originals, candidates, prompts, and browser captures live under `bkp/publication-scenes-2026-09-10/`. Both are Git-ignored and Jekyll-excluded. Builds need neither them nor image-processing tools.

## Simple diffusion addition (29 September 2026)

The new illustration follows [arXiv:2609.33947](https://arxiv.org/abs/2609.33947), especially Sections 2–4 and Appendices A.1, A.8, B, and C. Sampler temperature and categorical precision change while model weights, schedule, and reveal rule remain fixed. The dial abstracts those sampling choices; it is not a posterior-calibration claim. Three differently arranged text cards suggest distinct outputs, without substituting visual variety for GroupEval's actual semantic judgments.

The paper separates prediction loss from generation quality, and its finite-step analysis explains how parallel token draws can lose dependencies even with an exact denoiser. GroupEval reports individual quality and across-output diversity separately. The thumbnail focuses on the practical sampler intervention so it remains legible at small sizes; it does not try to compress the proofs or empirical plots into a badge. The positive small-model results are not represented as a guarantee for all diffusion models or sampling settings.

Generated with the built-in image-generation tool and exported to `files/arxiv26-simple-diffusion.webp`, a transparent 480 × 480 image. Original pixels, the full prompt, research notes, and browser review captures are retained in ignored `bkp/simple-diffusion-2026-09-29/`. The prompt asks for an unchanged slate model, an ochre sampler control, and distinct slate/sage/ochre text cards in the existing flat, wordless style. No theme-specific image or build dependency is required.
