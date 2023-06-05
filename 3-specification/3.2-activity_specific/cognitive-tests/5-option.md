---
layout: page
title: Option
permalink: spec/cognitive-tests/L1/option
nav_order: 5
parent: L1 data
grand_parent: Cognitive tests
is_table: true
---

# <i class="fa fa-table"></i> Option
{: .no_toc }

Table describing each option that a subject could choose from in a given L1 trial. Note that in some tasks the options may change within a trial after each input (e.g., SOS task); therefore the options need to also be indexed by `input_index`. 


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Referencing

id [integer]
: Primary key of the *<i class="fa fa-table"></i> Option* table.
: Each row in this table has a unique `id`.
: If the same option is shown at two different times in a trial, those two instances will have their own row in the *<i class="fa fa-table"></i> Option* table, each with its own `id`.


trial_id [integer]
: Refers to the id in the *<i class="fa fa-table"></i> Trial* table and indicates in which (L1) trial this option was shown.

index [integer]
: indexing each of the options within the set of options that were available to subjects on a given trial.

object_id [integer]
: An option is defined by a set of features. This variable is used to identify each time the same features were used. For example, if the same white digit "3" is used as an option in the digit span task, all those instances would have the same `object_id` although they would have different `id`s (as they appeared at different times). 


## When

onset [float]
: Duration between the start of the trial and the moment the option was displayed or activated.

duration [float]
: Describes for how long the option was displayed or active in seconds.


## Where

panel_id [string]
: Identifier of the panel this option is displayed over.

x_screen [integer]
: X coordinates of the option component on the screen in pixels. 

y_screen [integer]
: Y coordinates of the option component on the screen in pixels. 

x_viewport [float]
: X coordinates of the option component on the screen expressed as a fraction of the screen width. 

y_viewport [float]
: Y coordinates of the option component on the screen expressed as a fraction of the screen height. 


## What

description [string]
: A human readable, compact description of the main aspects of the option. The description for a given option depends on the task but follows a specific template for a given task. Because of this, it looks like the `option_description` could be "parsed" and "tidied"---however, this is not the intention; parsed/tidied data will be available in other tables; description is for human readability and facilitates the understanding of the data.

value [float]
: A numeric value associated with a particular response option; typically indicating the "worth" of a response (e.g., `value` = 1 for the correct response).

source_type [enum]
: An option is typically created using a particular procedure/algorithm ("generator") or is sampled from a particular set ("set"). This variable indicates which of these two applies for the current option.

source [string]
: Refers to the specific generator or set the option belongs to. Options that stem from the same source have the same data scheme and could thus be described in a table named after `option_source` (i.e., `option_source` indicates which table contains the full information about the option; e.g., "digit1to9").

> We could include a `source_count` variable here that indicates how many different stimuli there are in the set; but this is probably better stored in the table that contains information about that source.
{: .note }

index_in_source [integer]
: When a option is picked from a particular set (e.g., "digits1to9"), this index refers to the index within that set. 


## How

animation [string]
: Describes the animation that was used to show a particular option.
