---
layout: page
title: Stimulus
permalink: spec/cognitive-tests/L1/stimulus
nav_order: 2
parent: L1 data
grand_parent: Cognitive tests
is_table: true
---

# <i class="fa fa-table"></i> Stimulus
{: .no_toc }

Table describing each of the stimuli that were shown during an L1 trial.



# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Referencing

id [integer]
: Primary key of the *<i class="fa fa-table"></i> Stimulus* table.
: Each row in this table has a unique `id`.
: If the same stimulus is shown at two different times in a trial, those two instances will have their own row in the *<i class="fa fa-table"></i> Stimulus* table, each with its own `id`.


trial_id [integer]
: Refers to the id in the *<i class="fa fa-table"></i> Trial* table and indicates in which (L1) trial this stimulus was shown.


object_id [integer]
: A stimulus is defined by a set of features. This variable is used to identify each time the same stimulus features were used. For example, if the same white digit "3" is shown in a digit span sequence, all those instances would have the same `object_id` although they would have different `id`s (as they appeared at different times). 


presentation_id [integer]
: In a multitasking setting, a particular instance of a stimulus (e.g., the current letter "A") may be used by multiple trials at the same time (e.g, in the dual N-back task). Because these are different trials, they will have different `trial_id` values and hence will have different rows in the *<i class="fa fa-table"></i> Stimulus* table. We use `presentation_id` to indicate that a given stimulus is in fact the same instance across those trials.


index_in_trial [integer]
: Refers to individual stimuli within the sequence or set of stimuli shown during a trial.


## When

onset [float]
: Duration between the start of the trial and the appearance of the stimulus.


duration [float]
: Describes for how long this stimulus was displayed in seconds.

> When the stimulus is shown using an animation, `duration` covers the complete period between the start of the animation and the end of the animation.
{: .note }


## Where

panel_id [string]
: Identifier of the panel this stimulus is displayed over.

x_screen [integer]
: X coordinates of the stimulus on the screen in pixels. 

y_screen [integer]
: Y coordinates of the stimulus on the screen in pixels. 

x_viewport [float]
: X coordinates of the stimulus on the screen expressed as a fraction of the screen width. 

y_viewport [float]
: Y coordinates of the stimulus on the screen expressed as a fraction of the screen height. 

## What

source_type [enum]
: A stimulus is typically created using a particular procedure/algorithm ("generator") or is sampled from a particular set ("set"). This variable indicates which of these two applies for the current stimulus.


source [string]
: Refers to the specific generator or set the stimulus belongs to. Stimuli that stem from the same source have the same data scheme and could thus be described in a table named after `stimulus_source` (i.e., `stimulus_source` indicates which table contains the full information about the stimulus; e.g., "digit1to9").

> We could include a `source_count` variable here that indicates how many different stimuli there are in the set; but this is probably better stored in the table that contains information about that source.
{: .note }


index_in_source [integer]
: When a stimulus is picked from a particular set (e.g., "digits1to9"), this index refers to the index within that set. 


role [enum]
: Describe the role this stimulus plays in the trial (e.g., "target").


## How

animation [string]
: Describes the animation that was used to show a particular stimulus.
