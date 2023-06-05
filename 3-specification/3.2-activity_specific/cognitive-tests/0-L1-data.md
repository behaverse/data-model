---
layout: page
title: L1 data
permalink: spec/cognitive-tests/L1
nav_order: 0
parent: Cognitive tests
has_children: true
has_toc: false
---


# {{ page.title }}
{: .no_toc }

The L1-data contains multiple tables, some of which are detailed in this document, others will be added in the future.

> We use <i class="fa fa-table"></i> icon to refer to specific tables (e.g., the *<i class="fa fa-table"></i> Trial* table or the *<i class="fa fa-table"></i> Stimulus* table) and **subsections** to indicate the semantic category that groups various columns in a table; these semantic categories are used here only to highlight the ordering of the columns within each table.
{: .note}


# L1 tables


{% assign _tables = site.spec | where:"parent", "L1 data" | sort:"nav_order" %}

<ul class='tables-toc'>
  {%- for table in _tables -%}
    {%- if table.title != page.title -%}
      <li>
        <a href="{{ table.url | absolute_url }}"><i class="fa fa-table"></i> {{ table.title }}</a>{% if table.summary %} - {{ table.summary }}{% endif %}
      </li>
    {%- endif -%}
  {%- endfor -%}
</ul>

