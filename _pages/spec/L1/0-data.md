---
layout: page
title: L1
permalink: spec/L1
nav_order: 0
parent: Cognitive tests
grand_parent: Specifications
has_children: true
---


# {{ page.title }}
{: .no_toc }

The L1-data contains multiple tables, some of which are detailed in this document, others will be added in the future.

> We use <i class="fa fa-table"></i> icon to refer to specific tables (e.g., the *<i class="fa fa-table"></i> Trial* table or the *<i class="fa fa-table"></i> Stimulus* table) and **subsections** to indicate the semantic category that groups various columns in a table; these semantic categories are used here only to highlight the ordering of the columns within each table.
{: .note}


# L1 tables
{: .no_toc .text-delta }
- TOC
{:toc}




{% assign l1_table = site.pages | where:'parent', 'Cognitive tests' | sort:"nav_order" %}

<ul>
  {%- for table in l1_table -%}
    {%- if table.title != page.title -%}
      <li>
        <i class="fa fa-table"></i> <a href="{{ table.url | absolute_url }}">{{ table.title }}</a>{% if table.summary %} - {{ table.summary }}{% endif %}
      </li>
    {%- endif -%}
  {%- endfor -%}
</ul>
