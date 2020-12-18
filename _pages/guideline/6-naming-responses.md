---
title: Naming responses
parent: "Standards and conventions"
grand_parent: Guideline
layout: page
nav_order: 4
---

# Naming responses and response options


<!-- there is only one section -->
<!-- <hr>

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc} -->


Various terms and constructs are somehow related to the concept of a "response". Here we list those terms and clarify how we use them. To illustrate the various terms we will use the example of the digit span task where people have to click with their mouse on a virtual keyboard displayed on the screen which shows the digits 1 to 9, an "enter" button and a "delete" button.

input action
: each time a subject clicks on a button, we record an (action) input of type "click". 
Input can be of different types (e.g., mouse-click, key-press). An input is not necessarily meaningful or interpreted.

input interface
: The keyboard displayed on the screen is the input interface.
The input interface can be of different types (e.g., buttons, text-field, slider).

response
: is defined by the task and typically comprises only a subset of the inputs. For example, if the digit span task required reproducing a sequence of 3 digits (e.g, 3-5-7), the response might be 3-5-7 even though there might have been many more inputs (e.g., 3-6-delete-5-7-enter).

: An input is an objective description of a type of event, while a response is an "interpretation" of those events, an interpretation that is determined by the task definition.

> Sometimes people use "answer" instead of "response". An "answer" is a "response" that is verbal or written (i.e., a subset of response). We will not use "answer" and instead always use "response".
> 
> Responses can be of different types (e.g., choice, number, text, choice-sequence).
{: .note }

option (i.e., response options)
: in most computerized cognitive tests and surveys, subjects are offered a discrete set of options to choose from in order to form their response. This set is sometimes called "possible responses"; we call this entity "option". It is important to record information about the response options because they directly determine the meaning of the data (a rating of "3"  if very different if the scale goes from 1 to 3 versus 1 to 10).

: One key concern when describing response options is how to name the "good" one. 
In the survey literature, that option is sometimes referred to as the "key" while the remaining options are called ["distractors"](https://images.pearsonassessments.com/images/tmrs/tmrs_rg/Distractor_Rationales.pdf). We will not use these terms because they are unfamiliar to most and may be confusing (as "distractor" could also refer to a stimulus and a "key" could refer to a button on a keyboard or a column in a data table). It is also common to see the term "correct_response" (or equivalent) to designate the "good" option. `correct_response` is however ambiguous as it could refer to
1. the response that was given on a correct trial (i.e., correct serves as an adjective/filter); 
2. what response will evaluate to correct (i.e., if `response == correct_response`, then `correct = TRUE`) or
3. a boolean indicating if the current response is correct or not (`is_response_correct`). 

: To refer to the option that we expect the subject to choose, we will use the term `expected_response`. 

> To indicate whether an option is "good" or not, we will use a variable called "value" which assigns a numerical value to each option within an option set; the `correct` option would then have a value of 1, while all the `incorrect` ones would have a value of 0.
{: .note }

> The property of being the `correct` option is not a property of the option per se but depends on the "question" being asked (this question being an actual question or a stimulus depending on the case).
> 
> Furthermore, being the `correct` option is a property that does not depend on an actual response; hence it does not make sense to call it the `correct_response`, as it is not an attribute of the response but rather an attribute of the option in the context of an item/trial). 
{: .note }
