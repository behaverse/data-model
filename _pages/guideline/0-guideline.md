---
layout: default
title:  "Guideline"
permalink: guideline
nav_order: 1
has_children: true
has_toc: false
---

# Styleguide, standards, and conventions
{: .no-toc }

Styleguides and conventions can apply to:

- data
- code (surface-level properties; literal)
- code (structural, architectural, paradigmatic properties)
- workflow and practices (everything that is not directly code)

There are various great books that cover 2-4 but comparatively less about 1 and in particular within the context of behavioral data science.

This document focuses on 1 (with repercussions on 2). It takes advantage of lessons learned about 2 and applies them to 1 but it also addresses points that are specific to 1 and haven’t perhaps been addressed before. Overall this document also serves to list and sometimes explain the particular choices we’ve made and styles and conventions that we follow in our lab.

> We do not claim that the conventions and rules listed in this document are the absolute best way of doing things. We agree with “Clean Code” and others that consistency is more important than the choice for a particular set of conventions; this document therefore reflects our opinionated choices to achieve such consistency.
{: .note }


## General advices

- For column names, variables, and functions we use `lower_snake_case`.
- For enum values, we also use `lower_snake_case` (because those values might end up becoming columns during the data analysis).
- For dataset names in code and classes we use `CamelCase`.
- For named constants we use ALL_CAPS (e.g., `PI`, `MAX_RADIUS`).
- For naming data files and data folders see below. 


In some cases data may be aggregated from multiple different sources, each following their own conventions and it might not always be feasible/practical to harmonize them. More on this later. 
{: .note }


There are usually higher-level standards regarding the naming and structuring of code depending on the particular tool stack people use to analyze data (for example, for Python, there is PEP-8 and Flake-8, for R there is the Tidyverse style). It is generally advised to follow such well-known and widely used standards when applicable.
{: .note }


{% include toc_children.html parent=page %}
