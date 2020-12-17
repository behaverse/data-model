---
layout: page
title: "Naming data"
permalink: guideline/naming-data
parent: Guideline
nav_order: 1
---

# Columns in data tables and variables
{: .no_toc }

Naming things is notoriously hard. In addition to naming concerns that are common to all of programming, there are some naming concerns that may be more specific to data science / data analysis (e.g., naming data). In particular, we need to be careful about how to name variables that are successively transformed and aggregated within a data analysis pipeline.  Below are a few examples to illustrate and justify our choices.


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}



## Naming columns

While our focus is on naming columns in data tables (which we sometimes call "variables"), most of the rules and advice presented here applies equally to variables in code. 


TODO: LIST_OF_BOOKS

## General advice on naming things

The books listed above provide great advice on naming variables (among others); here we present some of them succinctly.

It is hard to overstate the importance of making your code readable (meaning that it is as easy as possible to understand the code's intention by reading the code, not the comments or the documentation). Good variable names are an important component in making both your code and data easier to understand and use. 

Here are a few points to consider when naming variables:
- Names should be explicit and easy to understand ("intention-revealing"; e.g., instead of `t` use `elapsed_time_in_days`).
- Ideally, names should tell you why they exist, what it does and how it is used. 
- Avoid names that can be misinterpreted outside of their context (`left` could mean `remaining` and `right` could mean `correct`); unfortunately, many words are ambiguous in programming.
- It's OK to use technical terms and abbreviations if they are common knowledge among those who will read the code or use the data; you don't want people to mentally rename your variable into some other variable name that is more common and familiar;
- don't shorten regular words, in particular if they are already short and shortening them may lead to confusion (e.g., `acc` for "accuracy" or is it "anterior cingulate cortex", `corr` for "correct" or for "correlation").
- Choose specific and more "colorful" words.
- Avoid{: .warn} generic names like "tmp", `Data`, `Manager`.
- Avoid noise words; among equally informative names, prefer the shortest; 
- Avoid number-series naming (e.g., a1, a2)
- Attach extra information if needed (e.g., "plaintext_password" rather than "password", "height_in_cm" rather than "height", "raw_data" rather than "data")
- Do not encode the type of the variable in the variable name (e.g., date_string). 
- Use names that can be searchable (e.g., if you search for a variable "t" you will get many false positive; rename it to "elapsed_time_in_days" and your search will be more effective);
- Use pronounceable and phonetically and visually distinct names (vital if you have to communicate with a peer about the code or data)
- Don't be cute, don't pun, don't use jokes; other people might not have the same sense of humor and get confused.
- It's OK to use long names; but throw out unnecessary words; Sometimes creating a new expression that refers to the long can be useful (however, add explanation in the codebook/documentation);
- Use formatting to convey meaning (e.g., capitalization, underscores, dashed).

> **Tip**{: .label} If you feel the need to write a comment to explain the meaning of a variable or function or expression, instead of writing the comment think about the possibility to change the names/code to make them more readable (ideally to the point no comments are needed).

> **Tip**{: .label } Test your variable names. Show someone (a peer) your variable name and ask them to guess what the variable means and what type it likely has (and whether it is a variable, a function or something else). 

> **Tip**{: .label } Don't hesitate to change names when you come up with better ones.


## Hierarchy


Many variable names include hierarchical information. Here are a few examples that one could find in the wild (not necessarily following the guidelines in this document):

- `houseIndex`
- `petal_length`
- `ReturnOnInvestment`
- `woman_age_usa`
- `car_batterySize`
- `test_phase`
- `gross_salary`
- `student_response_type`
- `problem.view`
- `problem.start_time`
- `total_number_hits`
- `coroutines_mean_cycle_duration`

It seems reasonable to have such names go from the highest/biggest/abstract to the lowest/smallest/concrete. For example `car_battery_size` makes more sense than `battery_car_size` or `size_car_battery`. It also makes sense to first name an entity (e.g., "house", "petal", "car battery") before naming its feature (e.g., "index", "length", "age"). Imagine a data set that contains many different entities and each entity has many features. This naming convention seems to fit more naturally with the way we think: it seems more natural to think first about the entities one wants to compare before thinking about their attributes. 

Note that in some cases this convention goes against the way we would name things in plain English. For example, "Gross salary" seems more natural than "salary gross"; however "salary_gross" is what is consistent with our style guide.

Note also that there might be cases where the terms used to form a variable name do not on their own reveal their relationships (entity versus property) and background knowledge is required to determine the correct order (i.e., `<entity>_<property>`).


> **Rule #1**{: .label .label-green} **Use the naming pattern `<entity>_<property>`.**


## Adjectives

There are cases that look like `<entity>_<feature>` (or `<class>_<property>`) but are in fact quite different. Consider for example variable names like "expected_response", and "left_button". In these examples, "response" and "button" are not properties of "expected" and "left". Should we instead rename these variables into "response_expected" and "button_left"? Again, it is important to note that "left" does not refer to a type of feature of button; the feature that would have "left" as a value might be called position and it would then make sense to have a variable called "button_position" which could take the value "left"'. button_left then does in fact NOT follow the convention `<class>_<property>`; 

In these examples, "left" and "expected" are values not variables; they play the role of adjectives and specify in greater detail which entity is being referred to (it is not button in general, it's only the left_button, it's not response we're talking about but expected response). In this case, it seems to make more sense to have the adjective be placed as a prefix to the entity, rather than as a post-fix (because it's similar to natural language use and should be different from the <entity>_<feature> pattern). Hence, we will use "left_button" instead of "button_left". 

Thus our general pattern for naming columns in a data table is:

> **Rule #2**{: .label .label-green} **Use the naming pattern `[<adjective>_]<entity>_<feature>`.**

## Singular versus plural

The use of singular versus plural in variable names is sometimes inconsistent. This inconsistency seems to arise from the fact that the plural may either refer to the values of a variable or to its cardinality. For example, does `customers_served` indicate "how many customers were served" or "list which customers were served"?

This point raises in fact two questions: 
When should we use plurals? 
How do we name "those variables" when we don't use plurals? 

Regarding the first question, plurals should be used for variables that have multiple values (e.g., a list). Following this rationale, `served_customers` would be a valid name for a variable listing which customers were served. Note however, that typical tabular data only allow for a single value per cell; it follows then, that in general column names in tabular data should be in singular form.

Regarding the second question, we follow the pattern <entity>_<property> with the <entity> being in singular form and <property> indicating cardinality.  Among the numerous options to name <property>, one can find "num", "total", "n" and "count"; as described later, we will use count to refer to the cardinality of a variable (e.g., "served_customer_count").

Finally, note that it's OK to use plurals for naming units (e.g., age_in_years). 


> **Rule #3**{: .label .label-green} **When naming variables using `<entity>_<property>` pattern, express the entity in singular form.**


## Boolean variables

There are two main rules for naming booleans:
- don't use negatives or negations in boolean names to avoid mental gymnastics (e.g., instead of "has_not_succeeded" or "has_failed", use "has_succeeded");
- use `is_`, `has_` or `should_` to make clear the variable is a boolean when there is ambiguity (e.g., space_left versus has_space_left).

It's OK to not use prefix boolean variables with `is_`, `has_` or similar when there is no ambiguity or a convention. In particular we use the following two booleans: 
- `correct`
- `timed_out`

> **Rule #4**{: .label .label-green} **Make clear when a variable is a boolean and express the variable positively.**

## Aggregation and transformation

In data analysis pipelines variables are typically transformed and aggregated. Sometimes it can be hard to come up with names for the new variables and to do so in a consistent way. The following provides some rules to do so in a consistent way.

To keep things consistent with the "Hierarchy" rule presented earlier, we will use suffixes of specific terms (see below). For example, if there's a variable called `response_time` and we compute first the log of response_time and then average the logs of response_time we would end up with a new variable called `response_time_log_mean`.


> **Rule #5**{: .label .label-green} **When transforming or aggregating variables, use dedicated suffixes..**


**Note:** Sometimes such names can get quite long and hard to read and there might in fact exist specific names to refer to a sequence of transformation or one can come up with such a specific new name. For example, one might use `x_rmse` rather than `x_square_mean_root`. 
