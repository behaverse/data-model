---
layout: page
title: Option
permalink: spec/L1/option
nav_order: 5
parent: L1
grand_parent: Cognitive tests
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
: Primary key.


trial_id [integer]
: Refers to the *<i class="fa fa-table"></i> Trial* table and indicates in which L1 trial this option was shown.


input_index [integer]
: Indexing all the clicks that occurred within a given trial, starting at 1 and going up to `Trial.input_count`.


index [integer]
: indexing each of the options within the set of options that were available to subjects on a given trial.


## When

onset [float]
: Duration between the start of the trial and the moment the option was displayed or activated.


duration [float]
: Describes for how long the option was displayed or active in seconds.

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

description [string]
: Describes what clicking on this object means given the current state of the test (e.g., "new_empty").


value [float]
: A numeric value associated with a particular response option; typically indicating the "worth" of a response (e.g., `value` = 1 for the correct response).


## How

: animation [string]
Describes the animation that was used to show a particular option.


## Other
Instrument-specific variables, NA when not applicable.

