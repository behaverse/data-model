---
layout: page
title: "Standards/Conventions"
permalink: guideline/conventions
parent: "Styleguide, standards, and conventions"
nav_order: 2
---


# {{page.title}}
{: .no-toc}

While the sections above were concerned with the general naming pattern of columns in data tables, the sections below will argue for the use of specific terms to the exclusion of others.


- TOC
{:toc}


## Standard variables and their default units

### Naming people

There are three issues related to naming people in a data set; they concern how to name the “entity” (e.g., “participant”), which postfix to use (e.g., “_id”) and what format to use for its values (e.g., an integer). We will go over each of this in turn and justify our choice for a particular convention.


#### Naming the entity

People who participate in a study and from whom data is collected are typically called “Subjects” or “Participants”; while “subject” has been standard in many subfields of cognitive sciences, “participant” has become more common recently and is considered more respectful to human study participants as it acknowledges their active involvement in the study. Other terms may be common in specific research domains investigating humans (e.g., “respondent”, “patient”, “child”), non-human animals (e.g., “monkey”) or computational models (e.g., “agent”). Still, in other contexts, it might be customary to use more generic terms (e.g., “person”, “user”). Finally there are terms that are idiosyncratic to particular data collection services (e.g., “worker”).

It is our view that the entity name in the data table should be generic to encompass a large set of use cases (e.g., children, animals, artificial agents) and we therefore second BIDS in the use of “subject” in the data specification and avoid using any other term in the data. This does not mean however that human participants should be addressed as “subjects” in general (for example, when communicating with them or about them); all participants are subjects, but not all subjects are participants (e.g., an AI-agent). Naming a columns or data file using “subject” is convenient and does not imply a disrespect towards study participants.


**Rule #6: Use “subject” to refer to the entity generating the response data. **


#### A postfix for the entity and format of the value

A reference to a subject identifier can serve multiple purposes and depending on that purpose a different postfix and format are preferable. The main purposes for a subject identifier are:

purpose #1: ensure the uniqueness of a subject within a study; link all data from a subject within a study. 

purpose #2: select or identify data belonging to a particular subject. For example, if you see an outlier point in a plot and want to understand why that point occurred, it might be necessary to identify that data as belonging to a particular subject and then look in greater detail in that subject’s data.

purpose #3: use the subject's identifier to name their data files.


purpose #4: ensure the uniqueness of a subject across studies. A subject may participate in multiple studies and it might be necessary (e.g., for meta-analyses) to determine whether subjects participated in multiple studies. 

These four purposes have somewhat different requirements. 
P#1 requires uniqueness within a study while P#4 requires uniqueness in general. For P#1 it would suffice to have a participant counter and assign an integer to each participant. But this would not work for P#4. Also while P#4 will typically require long strings to ensure uniqueness, soch long names are impractical for data analysis and storage (P#2, P#3). 

Because of these distinct purposes, we will use two different variables to refer to a subject.


subject_index: an integer assigned to subjects within a data set, typically but not necessarily in chronological order of starting participation in the study.

subject_name: a name given to subjects within a data set. Following BIDS recommendations, this name is obtained by converting subject_index to a string and using 0 padding, such that the first subject is named “01”. Note that such 0 padding requires knowing how many subjects there are in a study before being able to name them (e.g., if there are less than 100, the first subject would be called “01”, but if there are 1000 subjects in total, that subject would be called “0001”). 
We will use a string of length 4 by default as this will most likely cover all of our use cases.

subject_uuid: a universally unique identifier (UUID), which looks something like: "20025fe6-6868-47c6-a222-a5c06b49c8db". Note that this subject_uuid will not be directly in the L1 Trial data but rather will be stored in a separate table that contains for each subject_name its corresponding subject_uuid.

Note: we do not use “*_label” because it does not convey the idea of uniqueness; we do not use “*_ria” (which is obtained by shortening the subjects’s uuid; https://github.com/datalad/git-annex-ria-remote) to avoid potential data privacy issues.


### Naming Tasks and their components
Numerous terms designate different aspects of a task. Here we list some of these terms and provide our definition (as for most cases, we did not find clear and consensual definitions in the literature).


job	
refers to the high level description of the activity the subject is expected to perform. The job is typically described in the instructions (e.g., “your job is to classify these images in one of two categories”).
Within job we distinguish job_type, which typically takes the form of a verb (e.g., “classify”, “sort”) and job_description, which adds nouns to that verb (e.g., “classify even/odd numbers”, “sort by color”).

instrument
refers to the code or material that is used to present stimuli to subjects and record responses. In computer-based assessments, this could be the filename of a script or the link to a repository.
Note: a paradigm refers to a family of instruments.

config (timeline)
refers to a particular use of the instrument, where all parameters values are set. For example, one timeline could use the N-back instrument using N = 3 with letters while another could use the same N-back instrument using N = 2 with digits.

block
a timeline may comprise sub-timelines. For example, a timeline may include a practice and two test blocks. We distinguish 4 types of blocks: 
instruction
tutorial
practice
test

task
refers to a particular mapping between a specific stimulus set and a specific response set; task determines the meaning of a “trial” in an experiment and the structure of the resulting data tables (as each trial is a row in the L1 Trial data); task can be seen as a class of policies. 

**policy**
is a term from RL theory and refers to a mapping between specific stimuli (states) and responses (actions). While a task specifies a mapping in a generic way (i.e., the stimulus is a sequence of 4 letters and the response is a click on one of two buttons), a policy specifies particular values for that mapping (i.e., when you see “A-B-C-D”, click on the left button; otherwise click the right button).

implied_policy | assumed_policy | task_policy | 
When subjects engage in a cognitive test, their responses are typically evaluated as being correct or incorrect (this information may or may not be shown to subjects or affect subsequent experiences). This evaluation implicity presumes a particular policy, which reflects the experimenters assumption about how subjects should perform the task (this implied_policy is typically provided to subjects in the task instructions). However, this assumption may be wrong: subjects may use a different policy, and their policy may be better than the one assumed by the experimenter. 


**timeline_run**
refers to the actual unfolding in time of participants interacting with the instrument and performing the task. 


#### Hierarchical structure of an experimental study

study
refers to a meaningful and complete unit of a research project. A study must have a research question and the data collected in a study should be necessary and sufficient to answer that question. A study typically involves many subjects, completing several tests, over multiple sessions. 

session
refers to a grouping of consecutive timelines and thus also to a time period in a study.. Typically (but not necessarily), when subjects are tested on multiple days, each such day is called a session (i.e., consecutive sessions are typically separated by several hours). Note that there are other more technical and more local definitions of session that are commonly used in computer science. Session in psychology and related fields has a more abstract meaning and is typically related to the experimental design of a study.

timeline
see above. 

block
see above.

episode
as a study unfolds over time with possibly many events occurring at the same time, it is useful to be able to refer to specific time intervals within the overall time course of the observed behavior. While in simple tasks, a trial counter could serve as an index for consecutive time intervals in a timeline, in more complex tasks, trials of different tasks may occur in random order and multiple trials may even occur within the same time period. Here, we use episode to refer to consecutive, non-overlapping time periods within the course of a timeline. The splitting of a timeline into episodes can but does not necessarily follow a specific semantic structure (e.g., an episode starts with X and ends with Y); its main purpose is as an index to time intervals and the grouping of trials that occurred in the same time bin.
Note: “episode” is used in RL, it seems, to refer to what we call “trial”. 

trial
refers to a particular instance of an experiment (in the probability theoretical sense) where the structure of the experiment is defined by the task. For example, in a particular instance of the 2-back test, a particular trial may involve showing the letters “A-B-A” and observing the response “match”. A timeline may combine multiple tasks (e.g., in a task-switching experiment) and for each task, there would be many trials (to support statistical inference).


### Naming stimuli
There are several terms that are commonly used to refer to specific categories of stimuli. These include “item”, “target” and “non-target”, “distractor”, “cue”, “probe”, “flanker”, “mask”, “lure”, “stop-signal”, “task-cue”, “warning signal”. Unfortunately, it seems that these terms are not used in a consistent manner (e.g., a “no-go” stimulus may be referred to as either a non-target because it does not require a “go” response or a distractor because that stimulus should be ignored; a “target” might be a stimulus you need to respond to or a reference you need to search for in a set).

Furthermore, some of these terms belong to different semantic categories: a “cue” designates a functional role played by a stimulus within the context of the task (e.g., “this is to tell subjects to pay attention to the left”) while “lure” reflects assumptions about the cognitive processes underlying task performance (e.g., “this type of stimuli should be more confusing to subjects because …”).  Following this insight, we distinguish 

stimulus_role		a functional role assigned to a stimulus within the context of the task. This assignment does not depend on who/what is performing the task.

design_vector	a variable mapped to stimuli that reflects a data analysis intention (in reference to “design matrix”); examples include “lure”, “task_switch”, “congruent”.
Note: Oftentimes these data analysis intentions determined the choice of task parameters (e.g., the use of a particular trial sequence); in those cases, those intentions will be reflected in the parameters that describe a trial (e.g., the value of N in the N-back task, the current task in a task-switching task).

Naming Stimulus Roles
To decrease ambiguity in the naming of stimulus roles we will adopt the perspective on an “implied” ideal agent performing the task, that is, a schematic model of how the task designer intends agents to perform the task.

We define a stimulus as being a set of physical events that are presented to subjects with the intention or assumption that they cause a particular effect. Not all physical events are stimuli and the qualification of a physical event as being a stimulus or not depends on the context. 

By performing the task, the ideal agent performs a mapping between the stimulus space and the response space; in other words, we have:

R = Cognition(Stimulus; Task)

It is important to note here that Stimulus can be further broken down into categories, with a given stimulus possibly belonging to more than one of these categories. In particular, we have the following stimulus_role types:

input = mandatory input that causes a response when Task is fully specified; “domain” of the “Cognition” function. Example: a particular letter in the N-back task; 
distractor = a stimulus that is not used by the “ideal agent”. Example, a light flashing at random intervals.
modulator | supporter = optional argument which may improve performance if taken into account. Example: spatial cue in the Posner task.
specifier | goal | task = mandatory input to specify the Task; on its own, the specifier is  insufficient to yield a response. Example: task cue in a task-switching paradigm.
selector = stimulus used to highlight a subset of stimuli for which to respond to. Example: a question mark on top of one of the MOT dots. Probably a subclass of specifier.
modifier = stimulus that implies a transformation of the mapping from stimuli to responses. Example: negation sign in a symbol detection task (i.e., “now press the key in response to all but the digit ‘3’). Probably a subclass of specifier.

Having defined these categories, we now define the following stimulus roles within each category:


| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |




Note: the goal of this table is to enforce consistency. When using the term “non-target” we will always mean a mandatory input which does not trigger a response and not a subtype of distractor.


### Naming Responses and Response Options
Various terms and constructs are somehow related to the concept of a “response”. Here we list those terms and clarify how we use them. To illustrate the various terms we will use the example of the digit span task where people have to click with their mouse on a virtual keyboard displayed on the screen which shows the digits 1 to 9, an “enter” button and a “delete” button.

input action
Each time a subject clicks on a button, we record an (action) input of type “click”. 
Input can be of different types (e.g., mouse-click, key-press). An input is not necessarily meaningful or interpreted.

input interface
The keyboard displayed on the screen is the input interface.
The input interface can be of different types (e.g., buttons, text-field, slider).

response
is defined by the task and typically comprises only a subset of the inputs. For example, if the digit span task required reproducing a sequence of 3 digits (e.g, 3-5-7), the response might be 3-5-7 even though there might have been many more inputs (e.g., 3-6-delete-5-7-enter).
An input is an objective description of a type of event, while a response is an “interpretation” of those events, an interpretation that is determined by the task definition.
Note: sometimes people use “answer” instead of “response”. An “answer” is a “response” that is verbal or written (i.e., a subset of response). We will not use “answer” and instead always use “response”.
Responses can be of different types (e.g., choice, number, text, choice-sequence).

option (i.e., response options)
In most computerized cognitive tests and surveys, subjects are offered a discrete set of options to choose from in order to form their response. This set is sometimes called “possible responses”; we call this entity “option”. It is important to record information about the response options because they directly determine the meaning of the data (a rating of “3”  if very different if the scale goes from 1 to 3 versus 1 to 10).

One key concern when describing response options is how to name the “good” one. 
In the survey literature, that option is sometimes referred to as the “key” while the remaining options are called “distractors” (https://images.pearsonassessments.com/images/tmrs/tmrs_rg/Distractor_Rationales.pdf.). We will not use these terms because they are unfamiliar to most and may be confusing (as “distractor” could also refer to a stimulus and a “key” could refer to a button on a keyboard or a column in a data table). It is also common to see the term “correct_response” (or equivalent) to designate the “good” option. “correct_response” is however ambiguous as it could refer to a) the response that was given on a correct trial (i.e., correct serves as an adjective/filter); b) what response will evaluate to correct (i.e., if “response”==”correct_response”, then correct = TRUE) or c) a boolean indicating if the current response is correct or not (“is_response_correct”). 

To refer to the option that we expect the subject to choose, we will use the term “expected_response”. 

To indicate whether an option is “good” or not, we will use a variable called “value” which assigns a numerical value to each option within an option set; the “correct” option would then have a value of 1, while all the “incorrect” ones would have a value of 0.

Note also that the property of being the “correct” option is not a property of the option per se but depends on the “question” being asked (this question being an actual question or a stimulus depending on the case). Furthermore, being the “correct” option is a property that does not depend on an actual response; hence it does not make sense to call it the correct_response, as it is not an attribute of the response but rather an attribute of the option in the context of an item/trial). 


### Naming temporal variables
Numerous words refer to “time”; below we describe what those words mean for us.

Some names are used to designate specific points in time: 

*_datetime indicates a date and a time in a (somewhat) absolute sense for an event; datetime variables are expected to be in a specific format (see below). For example the start datetime of a timeline may be “2009-10-31T01:48:52.512Z”.
Note: we use *_datetime rather than * _date_time because date_time may suggest that time is a feature of the entity time rather than datetime being a single construct/feature of the entity it is appended to (e.g., start_datetime is less ambiguous than start_date_time which could be read as (start_)date_time or (start_date)_time).
*_timestamp refers to the timing of an event but its reference may be relative (e.g., beginning of the session) and its format less specified (e.g., a duration expressed in seconds). Because of the referencing, “timestamp” may be more ambiguous; if it refers to a date and time, use *_datetime; if it refers to a duration relative to a particular reference, use a term that makes this reference more explicit (e.g., stimlus_onset instead of stimulus_timestamp);
*_onset: refers to the duration between the trial start and the start of some event (e.g., stimulus_onset); 
*_offset: refers to the duration between the trial start and the end of some event (e.g., stimulus_offset); 
*_time: ambiguous term we keep for historic reasons; we currently use it only for “response_time”. 

Note that a point in time may be seen as a duration relative to a reference point; in the examples above, the focus is on the event itself rather than on the duration.


Other names refer to the duration of an event itself (the onset and offset of the event itself).

duration refers to the time difference between the end and the start of some entity; for example, stimulus_duration describes how long the stimulus was displayed;

Finally, still other names refer to the duration separating two specific events:
interval refers to the time difference between the end of an entity and the start of another (typically, but not always of the same type). For example inter_stimulus_interval is the duration between the disappearance of a stimulus and the appearance of the next one; cue_target_interval is the duration between the end of the cue and the start of the target (see figure below); Other examples include:
inter-trial interval (ITI)
inter-stimulus-interval (ISI)
cue-target-interval (CTI)
period (or phase) is used to refer to a temporal range in a more generic/abstract sense. For example, foreperiod may refer to the duration between the beginning of a trial and the onset of a stimulus.  
onset_asynchrony describes the elapsed time between the start of one entity and the start of another one (e.g., stimulus onset asynchrony; SOA)
delay: could refer to the unexpected addition of a duration (e.g., the takeoff was delayed); in general should be avoided; 
latency: expresses the idea of a duration for an event that could occur right away but might for some reason take more or less time. ”An input to a system produces some response which appears with a latency”; in general should be avoided.
 
As Martin Kleppman says in his book Designing Data Intensive Applications:
Latency is the duration that a request is waiting to be handled - during which it is latent, awaiting service. Used for diagnostic purposes ex: Latency spikes
Response time is the time between a client sending a request and receiving a response. It is the sum of round trip latency and service time. It is used to describe the performance of applications.



FIGURE FIGURE FIGURE



Examples
stimulus_onset refers to the duration between trial start and appearance of the stimulus; 
stimulus_duration is the duration between the appearance and the disappearance of the stimulus;
response_time: typically represents the duration between the onset of a stimulus and the completion of the response to that stimulus.
response_onset: refers to the duration between trial start (not stimulus onset) and the start of the response;
response_offset: refers to the duration between trial start (not stimulus onset) and the moment the response was completed; 
response_duration: refers to the difference between response_offset and response_onset and indicates how long it took to enter the response. 


Note: In general, in data tables, we should refer to stimulus onset times relative to the beginning of the trial (time reference of the trial) and specify their duration (i.e., onset and duration, rather than onset and offset or start_datetime and end_datetime). If there’s a need for additional time measurements, which are not part of the task parameters, these can be computed by the analyst rather than be precomputed and present in the shared data. 


### Other common Names
age [float]
Age is typically expressed in years. However, we don’t recommend flooring “age” to get integer values, as flooring implies losing data. It is better to leave variables as floats (when they are floats) and let the analyst decide whether or not flooring this variable is necessary for their specific purpose.

accuracy [float]
Accuracy refers to a measure of performance; in many tasks, it reflects the percentage (0-100%) or fraction (0-1) of correct responses. We will always use accuracy to refer to a performance measure that is a float and bounded in the [0-1] range.

correct [boolean]
correct is a boolean variable which indicates for a given trial or response whether it was correct or not. When no response was given when it should (i.e., timeout), correct evaluates to FALSE rather than NA. This is to avoid the case where people would be given a high performance score when in fact they avoided all difficult trials and responded correctly only to easy trials.

response_time [float]
The meaning of response_time (and its units) is not consistent across studies. For us, response_time is the duration between the moment the participant fully completed their response on a given trial and the moment that the earliest possible correct response could have been completed by an AI agent with perfect knowledge of the task and ability to instantaneously execute the response.
default unit: seconds  

Note: Other measures of durations exist and may be useful to describe a persons’ response. If such additional measures are needed, they should be specified explicitly. For example, 
response_onset
response_offset
response_duration

Note: Units for response times are not consistent across papers and publicly available datasets and one can find them expressed in either seconds or milliseconds. We decided to use seconds as the default unit for response times because:
avoid “exception” by always using seconds as duration measure;
avoid computation by keeping the units as they currently are in our raw data and task specs;
avoid the temptation to round rt to integers when expressed in milliseconds;
take advantage of the fact that most packages to analyse rt seem to be using seconds as a default unit;
be congruent with what seems to be the default unit in fMRI measurements. 

Note: It is tempting to abbreviate “response_time” as “rt”; however, there are several other variables prefixed “response_” which do not have abbreviations. Spelling the names out, while making the name longer, makes the overall data structure more consistent and explicit.

timeout [boolean]
Indicates whether the participant failed to respond within the allocated time period. 

gender / sex [enum]
Gender and sex are not exactly the same. Sex refers to a biological sex while gender is a more complex construct. A person may have a male biological sex but identify as a women for example. Depending on the question asked, the variable should therefore be either sex or gender. “What sex were you assigned at birth, such as on an original birth certificate?” is clearly a question about biological sex and should be coded as “sex”. The values for “sex” should be an enum:
Female
Male
Other
Prefer not to say



Units in variable names
“According to [NASA 1999] Arthur Stephenson, chairman of the Mars Climate Orbiter Mission Failure Investigation Board:
"The 'root cause' of the loss of the spacecraft was the failed translation of English units into metric units in a segment of ground-based, navigation-related mission software, ..."
from https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12

Some variables have measurement units. Variables should use the standard measurement unit for their type (e.g., durations in seconds; defined below), or the default unit assigned to them specifically within this document. Variables that use a non-standard, non-default measurement unit MUST specify the units explicitly using the format <variable>_in_<unit>

Examples:
age (by default in years)
age_in_months


When the units are a single word it’s OK to use the complete word; if it has multiple words, it’s better to abbreviate them unless the abbreviation can lead to confusion or ambiguity. For example, prefer “seconds” to “s” but “mpg” to “miles_per_gallon”.

Note: There are default units, these are marked with *. In addition there are default units for specific variables. If a “standard” variable has a default unit, that default unit overrides the default in this list. For example, the default for duration is seconds. “Age” is a duration but its default is years rather than seconds.

This document does not cover the subject of units exhaustively and will be updated as new use cases arise. When in doubt, consult BIDS:
https://bids-specification.readthedocs.io/en/latest/99-appendices/05-units.html
https://bids-specification.readthedocs.io/en/latest/02-common-principles.html#units


The formatting of the units should probably be specified further, maybe using an international standard (https://ucum.org/ucum.html or the one Morty mentioned once in his presentation ?)



Standard variable name suffixes 
Standard feature names
Variables may describe a feature or property of an entity, using the format <entity>_<feature>.  

length
refers to the length in cm of a physical object. When possible use a more specific word (e.g., height, width, distance). Don’t use length to mean count or size!

height, width
refers to the height and width in cm of a physical object.

weight
refers to the weight in kg a physical object.

size
Don’t use “size” as this term is ambiguous. “size” could refer to 180cm, “Medium” or 230x230. Instead, use a more specific term. 

count
refers to the cardinality of the entity. If an observation/row has “car_count = 5” this means that this particular observation involves a total count of 5 cars; this 5 is unrelated to other rows in the table.
Standard suffixes
All names below are not to be used alone but rather as suffixes (e.g., “block_type”, “stimulus_description”).

*_type [enum]
is always an enum. The meaning of the particular enum needs to be explained in a codebook.
It can be tempting to use synonyms of “type”, in particular when “type” is already taken; such synonyms include things like “category”, “kind” or  “set”. When those synonyms are not required (e.g., domain language) they should be avoided and replaced by “type”. Not all enums however need to be suffixed with “type”. 

*_description [string]
is always a text (String) for human consumption. While it is not strictly necessary, a textual description can greatly facilitate the understanding and processing of the data by humans.



Standard Aggregation suffixes
We will use the following names as suffixes to refer to particular operations in variable names. For example the mean of a variable “age” would be called “age_mean” (and not for example age_avg or age_m). We typically use the same name as the aggregation function name in R or Python. More specialized terms require explicit descriptions.

mean
average of the variable. Don’t use “avg” or “average”

median
median of the variable. Don’t use “med”. 

mode
mode of a variable.

min, max
minimum and maximum of a variable

sd
standard deviation of a variable. there are many other abbreviations for the standard deviations for the standard deviation but https://en.wikipedia.org/wiki/Standard_deviation uses SD and SD is the most common according to https://www.abbreviations.com/abbreviation/Standard+Deviation. However we won’t use sd in all caps.

var 
variance of a variable.

sum
the sum on a variable (e.g., item_price_sum = sum(item_price)). Don’t use total to designate the result of a sum operation. 

count
integer value, refers to the count of a particular entity (e.g., a variable named `page_count` indicates the number of pages). Note that “count” is different from “sum” (e.g., one can sum negative float values while count involves positive integers only) and from “index” (e.g., “this is the second” versus “there are two”).
Note also that while the use “n” to refer to counts is much shorter and might be standard in some circles, “count” is more explicit and less error prone than “n” which may mean different things in other contexts (e.g., the length of the variable, an iterator).

quantile25, quantile50
quantiles are similar to percentiles; both refer to the value of a variable x that splits the data such that a given fraction of the data is smaller than x. Quantile expresses that fraction as a number between 0 and 1 while percentiles express it as a percentage (between 0 and 100). 

We use quantiles rather than percentiles because they allow us to name the resulting variables in a simpler way. We use the following convention: 

quantile(x, q = 0.23) -> quantile23
quantile(x, q = 0.145) -> quantile145

Note that there could be an ambiguity when using quantile(x, q = 0.100) versus quantile(x, q = 1). However, note that quantile(x, q = 1) is in fact equivalent to max(x); quantile(x, q = 1) is median(x) and quantile(x, q = 0) is min(x). In these cases it is preferable to use the more direct name (max(x) rather than the quantile(x, q = 1)).



Standard Transformation Suffixes
In general, use the function name that was used to do the transformation. 
For example the log of a variable “age” would be called “age_log” (and not for example log_age or age_in_log). We typically use the same name as the transformation function name in R or Python.  We will use the following names to refer to particular operations in variable names.

log, log10, log2
natural log, log of base 10, log of base 2. Always specify the base when using the log except for the natural log (this seems standard in R and Python).

sqrt
square root of a variable.

pow2, pow3, pow4…
square or raised to the power of 3, 4, etc.

floor, ceil, round
flooring, ceiling or rounding a variable. Rounding may require specifying additional parameters.

rank
variables can be ranked (for example from the smallest to the largest values) and some values can be tied (in which case the rank will no longer be all integers). It might not be clear if the ranks are descending or ascending (e.g., age_rank). If such confusion arises it might be preferable to use a more direct name (e.g., youngest_to_oldest or youngest_first_rank).


Standard Referencing postfix terms
Several variables are used to filter, identify or locate particular rows in a table or across multiple tables. Below, we list and clarify the ones we use and how we use them.
Note: some people start counting from 1 others from 0; here we follow the convention of always starting counting/indexing from 1.

*_id [string, integer]
If a column name is postfix with “_id” (e.g., participant_id, task_id) it is expected that there exists a table which has the same name (i.e., “participant”, “task), with a primary key named “id” such that a value of in the first (particiapant_id = 215) refers to an entry in the second (a row in the participant table where id = 215). It is expected that the values in a variable postfixed “_id” are unique within a “local scope” (e.g., a dataset); however, it is not expected that they are unique globally—for such purposes one should use the “_uuid”.
If there is a column named “id” (i.e., without prefix) it is expected that there are other data tables or files that refer to this column; if such a link does not exist, use “index” instead.
Finally, the postfix “_id” does not imply a particular value format: both integers and strings are valid formats. 

*_name [string]
Sometimes “name” is used in a way that is similar to id (e.g., “study_name” or “task_name”).
The difference between “_id” and “_name” is that “_name” is expected to be a readable string (e.g., “n-back” versus “f346-r23v”). As with “_id”, it is expected that name refers to other data tables and that names are unique within a certain context (contrary to *_label).

*_uuid [ISO/IEC 11578:1996; sting] 
Universally unique identifier (https://en.wikipedia.org/wiki/Universally_unique_identifier) is a 128-bit number that can be generated on the fly and will most likely be unique. uuid can be used to assign a row a unique id without having to ensure that that number is not yet used by some other table.
_uuid are expected to be unique (globally); 
_uuid are not expected to be human readable; 
Example: 123e4567-e89b-12d3-a456-426614174000
Note: there also exists a uid which we don’t cover here.

*_hash
Sometimes it is useful to create a key by combining other keys. A hash is not strictly necessary as it can be recreated using other variables but it can be convenient for data processing.
https://en.wikipedia.org/wiki/Hash_function 
There is not a single standard for hashing; rather there are multiple algorithms that can be used. We use both CRC32 (32 hexadecimal characters; e.g., ”098f6bcd4621d373cade4e832627b4f6”) and SHA256 (base64 characters, e.g., “d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f”); depending on the probability of collision (i.e., two hashes being identical); when that probability is deemed high, we use SHA256.







*_index [integer]: Index should be favored when a variable is used for referencing and when order is important (often, but not always the chronological order).  For example, “stimulus_position_index” implies its value points to an entry in a list of possible stimulus_positions. Note that “index” typically implies a context within which the indexing occurs and that context must be made explicit. For example, trial_index may index trials within a block or a timeline.

*_repetition
is used to count the number of times the same “thing” occurred (e.g., a participant completes the same test twice, the same stimulus appears multiple times). As with index, repetition assumes a context which must be clarified when ambiguous. 
Note that repetition starts “counting” at 0 rather than 1; *_iteration instead of *_repetition would solve this issue but is less explicit and thus less preferred.

*_label [string]
an text attached to a variable; expected to be human readable, but not unique. 

Note: we avoid the use of *_number because it is typically too general and thus confusing.


Indexing contexts
We use several variables to index particular types of entities. As stated earlier, a context for indexing must be specified. We use the convention illustrated in the figure below:




The figure above indicates that the largest context is study. subjects of a study are indexed within a study; the first subject has index 1, the second has index 2, etc.
A subject may complete multiple sessions. Within a subject, the first session has index 1 and the second session has index 2, etc.
Timelines are indexed within sessions and subjects. The first timeline in the second session of the third subject has timeline_index = 1.
Blocks are indexed within a timeline. The third block, in the first timeline of the fourth session of the sixth subject has block_index = 3.
Episodes are also indexed within a timeline. This means that the first episode within each timeline has episode_index = 1 and this index continuously increases over the course of a timeline.
Tasks are indexed within blocks; if a block involves multiple tasks, each task will have its own index value.
Trials are indexed within tasks; if a block alternates between two types of tasks (i.e., task_index = [1, 2, 1, 2, 1, 2, …], the trial indices might look something like [1, 1, 2, 2, 3, 3, 4, 4, …]. 
Formats
Numeric values 
It can be sometimes tempting to floor, ceil or round a float variable into an integer. For example, one might assume that age when expressed in years should be an integer or that response times when expressed in milliseconds should be integers as well. 

Such data transformations should be avoided as a default because they lose data. A data analyst who wishes to round a variable for a particular purpose can still perform that operation later one and name her variables accordingly (e.g., age_floor).

Date, date time and timezones
Variables that express a “datetime” must 
be formatted using ISO 8601
express time at a resolution of the millisecond or smaller
include a timezone if possible
express participants local date and time in day

Imagine an online study with participants all over the world. At 6pm UTC, it is 11am in Los Angeles, 2pm in New York, 8pm in Paris and 3am (of the next day) in Tokyo. One would clearly expect a cognitive test completed at 6pm UTC to yield very different results depending on participants’ local timezone (e.g., 11am versus 3am). From a psychological point of view then, is participants’ local time (for a system administrator, on the other hand, UTC time would be more useful). Hence, we should express datetime variables in participants’ local timezone. 

There are cases where recording local timezones may infringe privacy. In such cases there are several possible solutions: 
remove timezones (11am Los Angeles -> 11am, 2pm New York -> 2pm)
replace timezones while keeping date and time in day (11am Los Angeles -> 11am UTC, 2pm New York -> 2pm UTC)
keep timezones but shift days (cf BIDS)
remove timezones and shift days

We recommend solution 1, where timezones are “missing”, rather than the other solutions which inject “lies” in the data. Hence, when timezones are not specified we assume (contrary to BIDS) that date_times are expressed in participants’ local (but unknown) timezone.

Example: “2009-10-31T01:48:52.512Z”
Note: the “year-month-day-hour-minute-second-ms” ordering is consistent with the hierarchy principle and provides a better view of the raw data than the format that would display day-month-year.
Note: we diverge here from BIDS because BIDS accepts missing timezones (assuming it implies the local time of the data viewer) and does not require millisecond precision (but does require format consistency within a dataset; 
https://bids-specification.readthedocs.io/en/latest/02-common-principles.html#units).

Languages
When referring to particular languages, we use the ISO_639-1 standard.
Colors
Colors can be expressed in many different ways,including hex (e.g., #A9A9A9), RGB (e.g., (169, 169, 169)) or CMYK (e.g., (0,0,0, 33.73). We use two conventions to describe colors depending on the use case. 
If the exact color value is not relevant and the information is destined for human readers, we refer to colors using color words (e.g., “red”, “green”, “blue”).
If, however, colors need to be specified exactly, we use the RGBA format which defines a color using 4 floating point values, each within the [0-1] range, and where the the first three number define the red, green and blue components of the color and the last number it’s opacity (0 = transparent, 1 = opaque).

Format of data values
Sometimes it is necessary to spread a table by one of its variables; meaning that the values of a particular variable become the names of new columns. In order for those new columns to be named in a way that is consistent with this style guide it is necessary that variable values (in particular for enums) follow the same standard as the variable names: they should be in lower_snake_case.
Missing values and errors
There is considerable variability in what is considered a missing value and how to deal with them. For example, in a go/no-go task where the correct response to no-go stimuli is to NOT respond, should a non-response be considered a missing value? Can a missing value evaluate to a correct response on a trial? In a different test, if a person had to choose between two options within a certain time interval and failed to respond within that time, should the accuracy of the trial be set to NA as the person did not in fact make a choice between the two options?

First of all, it is useful to have a variable that explicitly indicates whether the participant timed out or not (rather than having to infer this information by looking at the presence of missing values within a particular task context). 

Second, missing values should be applied only to the data that is in fact missing. If a person did not press a key in the go/no-go task, the response time would be missing but that would be considered reflecting the participant’s choice for a “no-go” and in a particular trial that response would evaluate to correct. 

Third, a response evaluates to correct if a specific set of conditions are met and evaluates to incorrect in all other cases. For example, in the “two choice” task with limited time to decide, a correct response would be defined by choosing the better option within that time limit. If no response was given (i.e., missing value) that condition is not fulfilled and thus the response evaluates to incorrect (and not NA). This is an important point because some people might instead decide to evaluate only those trials on which the person actually made a choice. Evaluating accuracy conditional on there being an input or not might be valid in some contexts but will typically lead to very different results. Imagine for example a case of a test where the questions asked are easy or hard. A weak student that answers correctly only the easy questions should not get a higher score than a better student who responded to all questions and made some errors on the hard questions. 

Regarding the coding of missing values, some people also use various numeric codes to “tag” missing values (e.g., -9 or -99). This can lead to errors down the line (e.g., missing values are not noticed or missing and actual values look similar). This practice should be avoided and missing values should be coded explicitly as NA.
Default Units
Below we list the names we use for different measurement units by measurement dimension (e.g., duration); these are the names that should be used when suffixing variables (to explicitly indicate units; e.g., response_time_in_milliseconds). Default units for each measurement dimension are marked by an *, those units need not be explicit in the variable names. Note that some specific variables listed in this document have their own default units (e.g., age in years); the variable specific default unit override the dimension default (i.e., duration is typically expressed in second, but for age we use years).
Duration
milliseconds
*seconds
minutes
hours
days
months
years
decades
centuries

Weight
mg:	milligrams
g:	grams
*kg:	kilograms
pounds

Length
mm:	millimeters
*cm:	centimeters
m:	meters
km:	kilometers
inches
feet
feet_inch:		mix of feet and inches (e.g., 5”3’)
pixels:			number of pixels; the pixel size in cm depends on subjects screen size and resolution.
screen_fraction: 	fraction of subject’s screen diagonal expressed between 0 and 1, from bottom-left to top-right.  For example, if the diagonal of the screen is 40cm long, a screen_fraction of 0.25 corresponds to 10cm. 

Note: for more information on viewports, see: https://developer.mozilla.org/en-US/docs/Web/CSS/length#Viewport-percentage_lengths

Frequency
*hertz:	count per second


Tables
Ordering of variables within a data table
The ordering of the columns within a table may facilitate the understanding of particular variables and can be useful when inspecting the data. Columns in a data table should be ordered according to the following rules:

first the primary key of the table, 
first the general, then the specific variables,
first the parameters/fixed variables, then the measurements,
group columns that are semantically related (e.g., columns describing the task, columns describing the response). 
if there’s an implicit ordering, use that ordering (the stimulus was shown before the response was recorded, the stimulus columns should be to the left of the response columns);
order columns alphabetically.

Regarding the ordering of the suffixes within an entity (e.g., block) we use the following convention:

block_type > block_name > block_id > block_index

Rows should be ordered using the indexing rules described earlier; that is ordered by study, then subject, then session, then timeline, then episode, then task and finally trial. This will also be the ordering of the primary key of the table.

Tidy tables
“Tidy data allows one to start analyzing the data right away“
Wickham, Hadley (20 February 2013). "Tidy Data" (PDF). Journal of Statistical Software.

Data should be in a tidy format. However, it is not always clear what that actually means. Take for example the case of survey data: should a row contain all the data for one participant (in which case each question has its own column) or should it contain the data for a single question (in which case there would be as many rows per participant as there were questions in the survey)?

When all the questions are of the same Type (say, “True/False” questions), one can have one row per question as the values within the same column would be of the same type (e.g., all responses are either “True” or “False”). But what if some questions ask about “True/False” and others ask for a rating from 1 to 5 and still others ask for a written text? In this case we can no longer have a row per question because the values would not be of the same type across rows; in this case, it seems to make more sense to have the questions be organized in columns rather than in rows. 


We currently do not have a satisfactory solution to deal with survey data using tabular data. All of our solutions have pros and cons and we finally decided for the following rules:
Firstly, survey data will be organized as a table per questionnaire where each row represents data from one subject and each question has its dedicated columns. We will use this “wide” format even when all questions and responses within a questionnaire are of the same “type” and a “long” data format would be possible. Second, data about the meaning of the variables (e.g., the exact wording of a particular question) will be stored in a separate table. Finally, variables in the survey data table should be given names that are indicative of the question (what does “q212” mean and how is it different from “q121”?) and need not be prefixed by the name of the questionnaire. Prefixing the questionnaire name might however be useful (to locate columns) or necessary (because the same column name is used for two different questions from different questionnaires) when combining data across multiple questionnaires. 

Note: it might be useful to use a hashing technique to guarantee various documentation files actually refer to specific dataset (by having the hash of the data (md5) in the documentation itself).

Note: some variables may have values that look as if they should/could be split into multiple, more tidy columns; it is OK to have such variable values to the extent that they are supposed to be used as is. For example, imagine there is a variable called timeline_name which takes values of the form <instrument_name>_<number>. It is in principle possible then to split this column in two columns that could be named <instrument_name> and <timeline_number_in_instrument>. However, the intention might be to have a variable to designate the construct “timeline” (which happens to be formatted in a principled way) rather than have two variables, one of which being rather useless on its own (i.e., <timeline_number_in_instrument>).



Datasets
Datasets can be organized and stored in many different ways. This section focuses only on the organization of datasets that are destined to be archived on a specialized website and/or shared with other researchers who might want to reproduce results or process the data in novel ways. These data sets can be seen as static and encapsulated/standalone; they are not meant to be updated and augmented as new data comes in.

Data from research projects often fit naturally in that category because a study will typically define a data collection campaign with a clear scope and well defined start and end times (determined for example by the timeline and funding of a particular research project). However, this need not always be the case. A research group may for instance collect data on a particular task for a long period of time and use different subsets of that data for different studies. 


Glossary
There are many concepts related to data and it is worth describing them quickly to make explicit what we mean when we use such terms. We can describe data using terms that indicate how it is stored/organized and terms that indicate how much the data has been “processed”. In addition there are terms for the entity that contains the data and for various processes involved in the collection, storage and processing of data. 

Data by levels of processing
Data that has not been processed at all is termed “raw” data. Data that is computed from other data, for example summary data, is called “derived” data. For reproducible research we want to share raw data with data analysis code that allows others to recompute all the analyses within a research project from the raw data, rather than only sharing the derived data. 

Data by file format and structure
Multiple different system may record data in a variety of forms (e.g., structured, unstructured) and file formats (e.g., “.csv”, “.json”, “.dat”); data in their “native” form are called “source data”. “Tidy” data is data that is organized in tabular form where each row is an observational unit and each column is a variable or property of that unit.

Data storage paradigms
A “data lake” refers to an unstructured collection of data, typically from many different sources. On the one hand, the data lake can be seen as maximally flexible (accepting all sorts of data) and holding the potential for limitless data analysis enterprises; on the other, the data lake can be seen as a chaotic data dump or data swamp. A “data warehouse” organizes the incoming data in a consistent way (schema) before storing it. Data from the data warehouse can (more) readily be used for data analysis; data from data lakes require significant background knowledge and work to be processed.

Note that some people use the term data mart to refer to either a subset or a view of the data warehouse (https://martinfowler.com/bliki/DataLake.html; https://en.wikipedia.org/wiki/Data_mart).
  

Database
A database usually refers to a collection of data that is under the control of a database management system (DBMS); database typically implies some form of interaction between the data and end users who read or write data from or into the database.
See https://en.wikipedia.org/wiki/Database.


Dataset 
A dataset also refers to a collection of data but while a database is a “living” entity, a dataset is typically a static resource which can be downloaded and shared as a whole (e.g., the PISA 2012 dataset). A dataset can be defined by a data collection campaign (e.g, all the data collected within a the research project) or a data analysis campaign (e.g, a dataset created from a larger medical database that focuses specifically on mental health issues during the COVD period).
See https://en.wikipedia.org/wiki/Data_set




Confusing terms
It is sometimes easy to confuse the terms described above. For example, source data is often called raw data even though the source data may in fact contain derived data (for example, the overall score a person achieved on a school test alongside all individual responses and their correctness). Source data is often messy but could in some cases be tidy.

Note also that it is not always clear what is meant by “processing” and what still counts as “raw data”. In our opinion, data is no longer “raw” when the data has been processed in a way that reflects assumptions about the values and relationships between variables. For example, filtering out trials with response times shorter than 150 milliseconds because one believes that such short durations imply those responses are not valid, is a form of data processing which is “biased” and thus the resulting, filtered data cannot no longer be considered “raw”. On the other hand, if for some reason, a system logs the same events multiple times, removing duplicates is a data processing step that is not biased and hence, the resulting, filtered data should still be considered “raw” data.

In general, we believe that the following operations may be performed on source data without compromising the “raw” status of the resulting data:
selection of variables
renaming variables and enum values
changes of units (from example, converting milliseconds to seconds)
reordering of columns and rows
removing duplicates
joining or separating tables



Which data to store? Which data to share?
It is typically the case that more data is stored than is shared. For example, researchers may store participants contact information or specific parameters of the hardware being used. The question then arises of what information should be collected in the first place and what subset of that data should be shared and whether or not the source data should be sent along with the data extracted from that source data.

Regarding what data to store, the answer depends on the purpose of the study. In any case, participants need to be informed about what data is being collected and the data collection must follow relevant regulations. It is generally well advised to be parsimonious regarding which personal data to collect (https://martinfowler.com/bliki/Datensparsamkeit.html). 

In our opinion, source data should not be shared if one has the ability to extract and share better formatted data. There are three main reasons not to share source data:  1) source data is not useable: they can be messy, come in diverse, sometimes proprietary formats, and lack documentation; 2) source data may contain personal data the data sharer is not aware of (e.g., participants’ full name, IP address); by defining what data is to be shared and extracting only that data it seems that such accidental privacy breaches could be avoided; 3) the extraction of data from the source data into usable data is outside the scope of responsibility of the data analyst. This last point deserves further explaining. For research to be reproducible one may want to test all the steps from the data collection up to the final results. While all the steps might be tested, they are not necessarily tested by the same person. For instance, a software company may run tests to determine that the recorded timestamps are accurate and a lab technician may run tests to calibrate the monitor and other hardware equipment. The question of what data to share is related to what quality assurance (QA) requirements are expected to be fulfilled by the data analyst. If both the source data and data extracted from the source data are handed over to the data analyst it becomes the data analyst’s responsibility to verify that both sets of data are in fact in agreement. If there is an error in the extraction code, the data analysis becomes responsible because he/she had access to that and could thus have spotted and corrected the error. In our opinion, the preparation of usable data from source data is not the responsibility of the data analyst; it is the responsibility of the data engineer and the entity that is sharing the data. It remains however that in any case tests must be conducted to verify the validity and accuracy of the process (we simply argue this is not the role of the person receiving the data). 

In short then, we say “don’t share source data”, instead share well documented, well formatted, tidy raw data.

Organization of Standalone Single Study Data
There are different valid options to organize standalone single study data and there are certain rules that apply to all such organizational systems.In particular, any dataset must have 
a document that describes and gives background information about the dataset as a whole (e.g., README.md, licence);
a code book that describes the meaning of the variables and the values they can take. 
Ideally these documents should have a code (hash) that guarantees that they refer to a particular dataset. These elements will be described later.


