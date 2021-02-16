---
layout: page
title: Instrument
permalink: spec/L1/instrument
nav_order: 6
parent: Cognitive tests
grand_parent: Specifications
---

# <i class="fa fa-table"></i> Instrument
{: .no_toc }

This table contains information describing the instrument or software used to collect data from subjects (e.g., the Python script that executes the presentation of the stimuli and records key presses).


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Referencing

id [string]
: Unique identifier of an instrument. Can be formed by combining name and version (e.g., "ds_v2020.01").


name [string]
: Name of the entity (scene, config filename) that is used to collect the data. The specific parameterization of the instrument is defined in the "Timeline/configuration" (e.g., "ds").


version [string]
: Refers to the current version of a particular instrument (e.g., current build version). We will use a calendar based versioning system ([calver.org](https://calver.org/); e.g., "v2020.01").
