---
layout: page
title: OptionComponent
permalink: spec/cognitive-tests/L1/option-component
nav_order: 6
parent: L1 data
grand_parent: Cognitive tests
is_table: true
---

# <i class="fa fa-table"></i> OptionComponent
{: .no_toc }

Options can comprise multiple components. This table describes each component of an option.


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Key

option_id [integer]
: A reference to the primary key of the *<i class="fa fa-table"></i> Option* table.


index [integer]
: A number from 1 differentiating each part. An option component with a higher `index` is displayed above all other components with a lower index.


## Where

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
