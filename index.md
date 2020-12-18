---
layout: page
nav_order: 1
last_modified_date: Jan 20, 2020
parent: nil
---

# Behaverse Data Model
{: .no_toc }


There are increasing amounts of behavioral data freely available on the internet with metadata standards making it easier to find them. However, there are large inconsistencies in the way those datasets are structured and stored, in the way their variables are named and formatted and even in what is meant by various common terms. These inconsistencies make it unnecessarily hard to reuse datasets and prevent the development of effective software tools and automatization. *Behaverse Data Model* defines coherent data models for both cognitive tests and surveys that apply to a large range of use-cases. In addition, *Behaverse Data Model* defines concepts and best practices regarding the naming and structuring of datasets. 



<hr>

## Table of contents
{: .text-delta }

{% assign pages = site.pages | sort:"nav_order" %}
<ul>
  {%- for page in pages -%}
    {% if page.parent == nil %}
      <li>
        <a href="{{ page.url | absolute_url }}">{{ page.title }}</a>{% if page.summary %} - {{ page.summary }}{% endif %}
        {% assign children = site.pages | where:'parent', page.title %}
        {% if children.size > 0 %}
          <ul>
            {% for child in children %}
            <li>
              <a href="{{ child.url | absolute_url }}">{{ child.title }}</a>{% if child.summary %} - {{ child.summary }}{% endif %}
            </li>
            {% endfor %}
          </ul>
        {% endif %}
      </li>
    {% endif %}
  {%- endfor -%}
</ul>


## About

*Behaverse Data Model* is part of an [FNR](https://www.fnr.lu/) funded cognitive sciences research project from [xCIT](https://xcit.org/)—a research team led by Prof. Pedro Cardoso-Leite.

xCIT is part of the [University of Luxembourg](https://wwwen.uni.lu/), and more specifically the [Department of Behavioral and Cognitive Sciences](https://humanities.uni.lu/behavioural-cognitive-sciences) in the [Faculty of Humanities, Education and Social Sciences](https://wwwen.uni.lu/fhse) which is located on [Campus Belval](https://www.belval.lu/en), a former steel industry site recently transformed into a dynamic environment for interdisciplinary research and innovation.

xCIT is supported by the Luxembourg National Research Fund
(ATTRACT/2016/ID/11242114/DIGILEARN).


## Contact

To get in touch, simply send us an email to [contact@xcit.org](mailto:contact@xcit.org).
