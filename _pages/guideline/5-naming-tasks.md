---
title: "Naming tasks"
parent: "Standards and conventions"
grand_parent: Guideline
layout: page
nav_order: 5
---


# Naming tasks and their components


<hr>

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc}


Numerous terms designate different aspects of a task. Here we list some of these terms and provide our definition (as for most cases, we did not find clear and consensual definitions in the literature).

job
: refers to the high level description of the activity the subject is expected to perform. The job is typically described in the instructions (e.g., "your job is to classify these images in one of two categories").
Within job we distinguish `job_type`, which typically takes the form of a verb (e.g., "classify", "sort") and `job_description`, which adds nouns to that verb (e.g., "classify even/odd numbers", "sort by color").


instrument
: refers to the code or material that is used to present stimuli to subjects and record responses. In computer-based assessments, this could be the filename of a script or the link to a repository.
<br />
*Note:* a paradigm refers to a family of instruments.


config (timeline)
: refers to a particular use of the instrument, where all parameters values are set. For example, one timeline could use the N-back instrument using N = 3 with letters while another could use the same N-back instrument using N = 2 with digits.

block
: a timeline may comprise sub-timelines. For example, a timeline may include a practice and two test blocks. We distinguish 4 types of blocks: 
- instruction
- tutorial
- practice
- test


task
: refers to a particular mapping between a specific stimulus set and a specific response set; task determines the meaning of a "trial" in an experiment and the structure of the resulting data tables (as each trial is a row in the L1 Trial data); task can be seen as a class of policies. 

policy
: is a term from RL theory and refers to a mapping between specific stimuli (states) and responses (actions). While a task specifies a mapping in a generic way (i.e., the stimulus is a sequence of 4 letters and the response is a click on one of two buttons), a policy specifies particular values for that mapping (i.e., when you see "A-B-C-D", click on the left button; otherwise click the right button).


implied_policy *OR*{: .text-delta} assumed_policy *OR*{: .text-delta} task_policy
: when subjects engage in a cognitive test, their responses are typically evaluated as being correct or incorrect (this information may or may not be shown to subjects or affect subsequent experiences). This evaluation implicity presumes a particular policy, which reflects the experimenters assumption about how subjects should perform the task (this `implied_policy` is typically provided to subjects in the task instructions). However, this assumption may be wrong: subjects may use a different policy, and their policy may be better than the one assumed by the experimenter. 

timeline_run
: refers to the actual unfolding in time of participants interacting with the instrument and performing the task.


## Hierarchical structure of an experimental study

study
: refers to a meaningful and complete unit of a research project. A study must have a research question and the data collected in a study should be necessary and sufficient to answer that question. A study typically involves many subjects, completing several tests, over multiple sessions. 

session
: refers to a grouping of consecutive timelines and thus also to a time period in a study.. Typically (but not necessarily), when subjects are tested on multiple days, each such day is called a session (i.e., consecutive sessions are typically separated by several hours). Note that there are other more technical and more local definitions of session that are commonly used in computer science. Session in psychology and related fields has a more abstract meaning and is typically related to the experimental design of a study.

timeline
: see above. 

block
: see above.

episode
: as a study unfolds over time with possibly many events occurring at the same time, it is useful to be able to refer to specific time intervals within the overall time course of the observed behavior. While in simple tasks, a trial counter could serve as an index for consecutive time intervals in a timeline, in more complex tasks, trials of different tasks may occur in random order and multiple trials may even occur within the same time period. Here, we use episode to refer to consecutive, non-overlapping time periods within the course of a timeline. The splitting of a timeline into episodes can but does not necessarily follow a specific semantic structure (e.g., an episode starts with X and ends with Y); its main purpose is as an index to time intervals and the grouping of trials that occurred in the same time bin.
<br />
*Note:* "episode" is used in RL, it seems, to refer to what we call "trial". 

trial
: refers to a particular instance of an experiment (in the probability theoretical sense) where the structure of the experiment is defined by the task. For example, in a particular instance of the 2-back test, a particular trial may involve showing the letters "A-B-A" and observing the response "match". A timeline may combine multiple tasks (e.g., in a task-switching experiment) and for each task, there would be many trials (to support statistical inference).
