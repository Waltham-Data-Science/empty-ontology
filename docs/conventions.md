# Term conventions

These are the rules EMPTY terms follow. Each rule has an example from
[`src/ontology/empty-edit.owl`](https://github.com/Waltham-Data-Science/empty-ontology/blob/V2/src/ontology/empty-edit.owl).
The rules were set by Jess Haley. The label rules come from tenet T19 of the NDI V2 schema
(did-schema `schemas/V_eta_tenets.md`, "T19 — A term is as general as its meaning allows; the
document carries the rest").

Terms minted before these rules were written do not all follow them yet. Where that is so,
it is noted under the rule.

## 1. Mint a term only when none exists

Look for a term in this order, and stop at the first one that has the meaning (T19):

1. a term already used in an NDI dataset (the NDI term registry);
2. a term in an existing ontology, found with an [OLS](https://www.ebi.ac.uk/ols4/) search;
3. only when neither has the meaning, a new EMPTY term.

The comment of a new term records the OLS search that found nothing, and why near terms do
not fit. For example, EMPTY:0000366 *flashed bar*: "No ontology term found (OLS4, 2026-10-22;
queries flashed bar, flashed bar stimulus, …): XCO visual stimulus (0000049) and NCIT Stimulus
(C41210) are general classes that do not name the stimulus kind; …".

## 2. Labels

- A label is as general as the meaning allows. It names nothing that the document using the
  term already carries: not the subject, species, place or partner (T19). For example, EMPTY:0000137
  is *body midpoint*, not "C. elegans midpoint". The species belongs to the subject.
- A label is as specific as its definition. When the meaning really depends on a species, a
  model or a protocol, the label says so (T19, clarified 2026-10-20). An example is
  EMPTY:0000293 *patch exploitation encounter*.
- Labels are lower case except for proper names and acronyms (*NDI binary format*,
  *OME-Zarr*).

*Not yet followed everywhere:* many labels from before 2026-10-20 still carry their context,
for example "elevated plus maze: open arm (north) - entries" and the
"C. elegans chemotaxis assay parameter: …" terms.

## 3. Definitions

- Every term has a definition (`IAO:0000115`).
- A definition names the kind of thing the term is (the genus) and what sets it apart from
  others of that kind (the differentia). For example, EMPTY:0000370 *analog input channel*:
  "A channel through which an acquisition system samples a continuously valued signal."
- A definition does not state units, because the document that uses the term carries the
  unit (commit 0d27041, EMPTY:0000119 and EMPTY:0000120).

*Not yet followed everywhere:* 9 live terms have no definition: EMPTY:0000163, 0000164,
0000181–0000187.

## 4. Synonyms

A synonym is a genuine alternative name for the same thing, in the way "average" is for
"mean". A standard abbreviation counts as a synonym. A label that appeared in a published
release counts as a synonym too (see "previous name" below). Labels that existed only on
development branches are not kept. Lab-specific vocabulary is **not** a synonym: column names,
code names and lab labels. A lab's column and code names belong in that lab's mapping, such as
the per-lab `tableDoc_dictionary.json` in NDI-matlab (`src/ndi/+ndi/+setup/+conv/+<lab>/`, for example `+haley`) or an SSSOM mapping, not in this ontology.

- An alternative name with the same meaning is an exact synonym (`oboInOwl:hasExactSynonym`),
  with an `@en` language tag. For example, EMPTY:0000259 *OME-Zarr* has "OME-NGFF".
- A name that overlaps the term but is not interchangeable with it is a related synonym
  (`oboInOwl:hasRelatedSynonym`). For example, EMPTY:0000368 *onset time* has "start time".
  "Start time" can also correctly name the start of the period around a stimulus (stimopen),
  which the definition of onset time excludes. EMPTY:0000369 *offset time* has "end time"
  for the same reason.
- Synonym types come from the OBO Metadata Ontology (OMO), attached as an axiom annotation
  `oboInOwl:hasSynonymType`:
  - **abbreviation** (`OMO:0003000`) types every abbreviation or initialism. For example,
    EMPTY:0000317 *quadratic discriminant analysis* has "QDA", EMPTY:0000182 *dorsal dentate
    gyrus of hippocampal formation* has "dDG", and EMPTY:0000370 *analog input channel* has "ai":

        AnnotationAssertion(Annotation(oboInOwl:hasSynonymType obo:OMO_0003000) oboInOwl:hasExactSynonym obo:EMPTY_0000317 "QDA"@en)

  - **previous name** (`OMO:0003008`) types a label the term had in a published release
    (`main`). The scope says how the old label relates to the term now. It is exact when it
    meant the same thing: EMPTY:0000105 *target seeding OD600* has "bacterial OD600 (target)
    at seeding". It is related when the term has since been generalised: EMPTY:0000137 *body
    midpoint* has "C. elegans midpoint".
- Both synonym types are declared in the edit file as sub-properties of
  `oboInOwl:SynonymTypeProperty`, with OMO's label and definition. They are also listed in
  `src/ontology/imports/omo_terms.txt`, so the OMO import brings them in when it is next
  refreshed. In the OBO release they become `synonymtypedef` lines.
- An old label or a lab code that is not kept as a synonym belongs in the term's comment. For
  example, the comment on EMPTY:0000374 says "the NDI v1 channel prefix is 't' (a code, not a
  synonym)", and the comment on EMPTY:0000293 records that it was relabelled from 'exploit'.

## 5. Comments

A term's `rdfs:comment` records where the term came from:

- who decided it, and on what date;
- the decision it cites, for example a did-schema plan document and its tag;
- the OLS search that found no existing term (rule 1);
- where it is used, for example the code or dataset that writes it.

For example, EMPTY:0000359 *ethics jurisdiction*: "No ontology term found (OLS4, 2026-10-21;
queries ethics jurisdiction, jurisdiction): … Jess Haley, 2026-10-21."

*Not yet followed everywhere:* every term since EMPTY:0000354 has a comment with a date and
either an OLS search or a cited decision, but four of them (EMPTY:0000354, 0000356–0000358) do
not name who decided. Many earlier terms have no comment.

## 6. Obsoletion

A term is never deleted, and its id is never reused. To make a term obsolete:

- add `owl:deprecated true`;
- add "obsolete " to the start of the label;
- add `oboInOwl:consider` for each replacement term (CURIE as a string). More than one is
  allowed. `IAO:0100001` (term replaced by) is not used;
- start the comment with "Obsolete: replaced by *label* (*id*); *reason* (*who, date, source*).
  Use *label* (*id*)." and then keep any earlier comment after "Before:";
- keep the definition, and drop the superclasses and synonyms.

For example, EMPTY:0000140 *obsolete encounter onset time* has
`oboInOwl:consider "EMPTY:0000368"`. All 32 obsolete terms follow this pattern.

## 7. Identifiers

- Ids are `EMPTY:` followed by seven digits. They are allocated in sequence from the
  ONTOLOGY-CREATOR range in `src/ontology/empty-idranges.owl`.
- Classes and object properties use the same counter. EMPTY:0000001 to EMPTY:0000416 are all
  allocated with no gaps. EMPTY:0000406 and EMPTY:0000407 were allocated on the
  `development` branch (PR #28).
- An id is never reused, not even when its term is made obsolete (rule 6).

## 8. Object properties

Relations are OWL object properties (`Declaration(ObjectProperty(...))`). The first ones were
added on 2026-10-22: EMPTY:0000378–0000382 and EMPTY:0000386.

- Like a class, an object property has a label, a definition ("A relation between … and …")
  and a comment.
- Characteristics are declared as axioms. For example, EMPTY:0000380 *paired with* is
  `SymmetricObjectProperty`.
- No domain or range has been declared so far.
