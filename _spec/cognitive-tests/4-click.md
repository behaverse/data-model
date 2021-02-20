---
layout: page
title: Click
permalink: spec/cognitive-tests/L1/click
nav_order: 4
parent: L1 data
grand_parent: Cognitive tests
is_table: true
---

# <i class="fa fa-table"></i> Click
{: .no_toc }

Table describing each click that was recorded during an [L1 trial](/trial).


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}



## Referencing

id [integer]
: Primary key; each click has its own `id` value.


trial_id [integer]
: Refers to the *<i class="fa fa-table"></i> Trial* table and indicates in which L1 trial this stimulus was shown.


index [integer]
: Indexing all the clicks that occurred within a given trial; ranging from 1 to `Trial.input_count`.


response_element_index [integer]
: Indicates which of the clicks is used and in what order to form the actual response in the L1 trial when `response_structure` is "sequence" or "set".

> This needs to be here rather than in *<i class="fa fa-table"></i> Option* because the same option can be clicked multiple times and either serve or not for the response depending on the order of the clicks. For example, in the Digit Span test we could have the response of "3;5;7" on a particular trial. This might correspond to
>  - `option.description` = ["3", "4", "delete", "delete", "3", "5v, v7", "enter"]
>  - `click.response_element_index` = [NA, NA, NA, NA, 1, 2, 3,  NA]
{: .note }


## When

onset [float]
: Duration between the start of the trial and the moment the mouse button press occured.


duration [float]
: Describes for how long the mouse button was pressed.

## Where

x_screen [integer]
: X coordinates of the stimulus component on the screen in pixels. 


y_screen [integer]
: Y coordinates of the stimulus component on the screen in pixels. 


x_viewport [float]
: X coordinates of the stimulus component on the screen expressed as a fraction of the screen width. 


y_viewport [float]
: Y coordinates of the stimulus component on the screen expressed as a fraction of the screen height. 


## What
Describes what was clicked on.

object_type [enum]
: Describes the type of object that was clicked on (e.g., "button").


object_name [string]
: The name of the object that was clicked on (e.g., "sos_box_1_3").


is_object_enabled [boolean]
: Indicates whether the object that was clicked on was enabled (clickable) or not.


object_state [string]
: Describes the state the object was in *before* it was clicked on. The meaning of "state" depends on the particular task (e.g., "new empty").


option_id [integer]
: If the click is on an option, this variable indicates which option it was. Note that `option_id` refers to an id in the *<i class="fa fa-table"></i> Option* table.


stimulus_id [integer]
: If the click is on a stimulus, this variable indicates which stimulus it was. Note that `stimulus_id` refers to an id in the *<i class="fa fa-table"></i> Stimulus* table.


## How
animation [string]
: Describes the animation that was used to show a particular stimulus. 


## Other
Instrument-specific variables, NA when not applicable.
