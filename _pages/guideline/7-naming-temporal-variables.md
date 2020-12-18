---
title: "Naming temporal variables"
parent: "Standards and conventions"
permalink: guideline/temporal-variables
grand_parent: Guideline
layout: page
nav_order: 7
---

# Naming temporal variable

<hr />

## Table of content
{: .no_toc .text-delta }
- TOC
{:toc}


Numerous words refer to "time"; below we describe what those words mean for us.

Some names are used to designate specific **points in time**: 

*_datetime
: indicates a date and a time in a (somewhat) absolute sense for an event; datetime variables are expected to be in a specific format (see below). For example the start datetime of a timeline may be `2009-10-31T01:48:52.512Z`.

> We use `*_datetime` rather than `* _date_time` because `date_time` may suggest that time is a feature of the entity time rather than `datetime` being a single construct/feature of the entity it is appended to (e.g., `start_datetime` is less ambiguous than `start_date_time` which could be read as `(start_)date_time` or `(start_date)_time)`.
{: .note }

*_timestamp
: refers to the timing of an event but its reference may be relative (e.g., beginning of the session) and its format less specified (e.g., a duration expressed in seconds). Because of the referencing, "timestamp" may be more ambiguous; if it refers to a date and time, use `*_datetime`; if it refers to a duration relative to a particular reference, use a term that makes this reference more explicit (e.g., `stimlus_onset` instead of `stimulus_timestamp`).

*_onset
: refers to the duration between the trial start and the start of some event (e.g., `stimulus_onset`);

*_offset
: refers to the duration between the trial start and the end of some event (e.g., `stimulus_offset`); 

*_time
: ambiguous term we keep for historic reasons; we currently use it only for `response_time`. 


> A point in time may be seen as a duration relative to a reference point; in the examples above, the focus is on the event itself rather than on the duration.
{: .note }

Other names refer to **the duration of an event** itself (the onset and offset of the event itself).

duration
: refers to the time difference between the end and the start of some entity; for example, `stimulus_duration` describes how long the stimulus was displayed;

Finally, still other names refer to the duration separating two specific events:

interval
: refers to the time difference between the end of an entity and the start of another (typically, but not always of the same type).
: For example `inter_stimulus_interval` is the duration between the disappearance of a stimulus and the appearance of the next one; `cue_target_interval` is the duration between the end of the cue and the start of the target (see figure below); Other examples include:
- inter-trial interval (ITI)
- inter-stimulus-interval (ISI)
- cue-target-interval (CTI)

period (or phase)
: is used to refer to a temporal range in a more generic/abstract sense. For example, foreperiod may refer to the duration between the beginning of a trial and the onset of a stimulus.  

onset_asynchrony
: describes the elapsed time between the start of one entity and the start of another one (e.g., stimulus onset asynchrony; SOA)

delay
: could refer to the unexpected addition of a duration (e.g., the takeoff was delayed); in general should be avoided.

latency
: expresses the idea of a duration for an event that could occur right away but might for some reason take more or less time. *"An input to a system produces some response which appears with a latency"*; in general should be avoided.
 
As Martin Kleppman says in his book [Designing Data Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/):
>>> ***Latency** is the duration that a request is waiting to be handled - during which it is latent, awaiting service. Used for diagnostic purposes ex: Latency spikes.*
>>> ***Response time** is the time between a client sending a request and receiving a response. It is the sum of round trip latency and service time. It is used to describe the performance of applications.*
{: .text-grey-dk-000 }


![Temporal variables]({{ site.baseurl }}/assets/images/temporal_variables.png)


## Examples

- `stimulus_onset` refers to the duration between trial start and appearance of the stimulus; 
- `stimulus_duration` is the duration between the appearance and the disappearance of the stimulus;
- `response_time` typically represents the duration between the onset of a stimulus and the completion of the response to that stimulus.
- `response_onset` refers to the duration between trial start (not stimulus onset) and the start of the response;
- `response_offset` refers to the duration between trial start (not stimulus onset) and the moment the response was completed; 
- `response_duration` refers to the difference between `response_offset` and `response_onset` and indicates how long it took to enter the response. 


> In general, in data tables, we should refer to stimulus onset times relative to the beginning of the trial (time reference of the trial) and specify their duration (i.e., onset and duration, rather than onset and offset or `start_datetime` and `end_datetime`).
> 
> If there's a need for additional time measurements, which are not part of the task parameters, these can be computed by the analyst rather than be precomputed and present in the shared data.
{: .note }

