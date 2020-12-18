---
title: Naming stimuli
parent: "Standards and conventions"
grand_parent: Guideline
layout: page
nav_order: 4
---


# Naming stimuli

<hr>

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc}


There are several terms that are commonly used to refer to specific categories of stimuli. These include "item", "target" and "non-target", "distractor", "cue", "probe", "flanker", "mask", "lure", "stop-signal", "task-cue", "warning signal". Unfortunately, it seems that these terms are not used in a consistent manner (e.g., a "no-go" stimulus may be referred to as either a non-target because it does not require a "go" response or a distractor because that stimulus should be ignored; a "target" might be a stimulus you need to respond to or a reference you need to search for in a set).

Furthermore, some of these terms belong to different semantic categories: a "cue" designates a functional role played by a stimulus within the context of the task (e.g., "this is to tell subjects to pay attention to the left") while "lure" reflects assumptions about the cognitive processes underlying task performance (e.g., "this type of stimuli should be more confusing to subjects because ...").  Following this insight, we distinguish:


stimulus_role
: a functional role assigned to a stimulus within the context of the task. This assignment does not depend on who/what is performing the task.

design_vector
: a variable mapped to stimuli that reflects a data analysis intention (in reference to "design matrix"); examples include "lure", "task_switch", "congruent".

> Oftentimes these data analysis intentions determined the choice of task parameters (e.g., the use of a particular trial sequence); in those cases, those intentions will be reflected in the parameters that describe a trial (e.g., the value of N in the N-back task, the current task in a task-switching task).
{: .note }


# Naming stimulus roles

To decrease ambiguity in the naming of stimulus roles we will adopt the perspective on an "implied" ideal agent performing the task, that is, a schematic model of how the task designer intends agents to perform the task.

We define a stimulus as being a set of physical events that are presented to subjects with the intention or assumption that they cause a particular effect. Not all physical events are stimuli and the qualification of a physical event as being a stimulus or not depends on the context. 

By performing the task, the ideal agent performs a mapping between the stimulus space and the response space; in other words, we have:

$$
R = Cognition(Stimulus; Task)
$$

It is important to note here that Stimulus can be further broken down into categories, with a given stimulus possibly belonging to more than one of these categories. In particular, we have the following `stimulus_role` types:


input
: mandatory input that causes a response when *Task* is fully specified; "domain" of the "Cognition" function.
<br />
*Example:* a particular letter in the N-back task.

distractor
: a stimulus that is not used by the "ideal agent". Example, a light flashing at random intervals.

modulator *OR*{: .text-delta} supporter
: optional argument which may improve performance if taken into account.
Example: spatial cue in the Posner task.

specifier *OR*{: .text-delta} goal *OR*{: .text-delta} task
: mandatory input to specify the Task; on its own, the specifier is  insufficient to yield a response.
<br />
*Example:* task cue in a task-switching paradigm.

selector
: stimulus used to highlight a subset of stimuli for which to respond to.
<br />
*Example:* a question mark on top of one of the MOT dots. Probably a subclass of specifier.

modifier
: stimulus that implies a transformation of the mapping from stimuli to responses.
<br />
*Example:* negation sign in a symbol detection task (i.e., "now press the key in response to all but the digit '3'). Probably a subclass of specifier.

Having defined these categories, we now define the following stimulus roles within each category:


| stimulus_role_type | stimulus_role      | description                                                  |
| :----------------- | :----------------- | :----------------------------------------------------------- |
| input              | target ("trigger") | stimulus that completes the input and triggers the execution of the response. |
|                    | non-target         | stimulus that is mandatory for performing the task but not sufficient to trigger a response. |
| distractor         | distractor         | stimulus that is not processed by the "implied" agent.       |
| modular            | location-cue       | stimulus that does not fundamentally change the task but may affect the importance that should be given to other stimuli but. |
| specifier          | task-specifier     | stimulus that indicates which task should be performed.      |
| selector           | probe              | stimulus that indicates how/about what to respond.           |
| modifier           | stop-signal        | stimulus that changes the stimulus-response mapping in a systematic way. |

>The goal of this table is to enforce consistency. When using the term "non-target" we will always mean a mandatory input which does not trigger a response and not a subtype of distractor.
{: .note }
