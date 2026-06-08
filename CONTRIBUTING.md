# Contributing to the Behaverse Data Model (BDM)

Thanks for your interest in BDM. Contributions of documentation, code, and data are all welcome.

## Ways to contribute

- **Documentation** — improve the guides, explanations, and conventions in this repo (the [Quarto](https://quarto.org) site).
- **Schemas** — BDM *documents* schemas but does not define them. The machine-readable schemas live in **[behaverse/schemas](https://github.com/behaverse/schemas)**; propose schema changes there.
- **Data** — share a dataset in BDM format, or help convert one.
- **Discussion** — open an [issue](https://github.com/behaverse/data-model/issues) or join the [discussions](https://github.com/orgs/behaverse/discussions).

## Where things live (single source of truth)

BDM references machine-readable artifacts; it does not replicate them. So *where* you change something matters:

| You want to change… | Edit it in… |
|---|---|
| A field/term in a schema (trial, event, dataset, …) | **[behaverse/schemas](https://github.com/behaverse/schemas)** — BDM renders it by reference |
| Folder structure, naming conventions, explanations, guides | **this repo** (`behaverse/data-model`), as prose |
| The glossary's cross-cutting terms | the `vocabulary/` resource in `behaverse/schemas` |

Please don't hand-edit generated content (any page BDM fetches/renders from `behaverse/schemas`).

## Develop locally

Install the [Quarto CLI](https://quarto.org/docs/get-started/) and [uv](https://docs.astral.sh/uv/). The schema reference pages (`spec/trial/`, `spec/event/`) are **generated** from `behaverse/schemas` (see `scripts/build_spec.py` + `schemas.lock`), so generate them first, then preview:

```bash
uv run scripts/build_spec.py   # fetch schema artifacts -> spec/trial, spec/event
quarto preview .
```

To preview against a local `behaverse/schemas` checkout (before changes are merged/deployed):

```bash
uv run scripts/build_spec.py --local-dir ../schemas
```

## Conventions

Follow the naming and structure conventions documented in the site's *Explanations* and *Conventions* sections. In short: `snake_case` variable names, a trailing `_id` denotes a foreign key into a documented table, and dates/times use ISO 8601.

## License

By contributing, you agree that your contributions are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
