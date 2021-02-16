---
layout: page
title: StimulusComponent
permalink: spec/L1/stimulus-component
nav_order: 3
parent: Cognitive tests
grand_parent: Specifications
---

# <i class="fa fa-table"></i> StimulusComponent
{: .no_toc }

Stimuli can comprise multiple components. This table describes each component of a stimulus.


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Key

stimulus_id [integer]
: A reference to the primary key of the *<i class="fa fa-table"></i> Stimulus* table.


index [integer]
: A number from 1 differentiating each part. A stimulus component with a higher `index` is displayed above all other components with a lower index.


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
: A human readable, compact description of the component.

symbol_name [string]
: The name of the displayed symbol.


symbol_count [integer]
: The number of symbols represented in this component.


symbol_layout [enum]
: How the symbols are laid out (vertical, horizontal, diagonal_top_left, diagonal_top_right, square, ring, cross, x, two_columns, h).


color_name [string]
: The human-readable name of the component color.


color_hex [string]
: The hexadecimal value of the component color.


orientation [enum]
: The symbol orientation (north, north_east, east, south_east, south, south_west, west, north_west, free).
