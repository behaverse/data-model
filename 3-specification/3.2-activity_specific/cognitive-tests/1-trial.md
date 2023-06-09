---
layout: page
title: Trial
permalink: spec/cognitive-tests/L1/trial
nav_order: 1
parent: L1 data
grand_parent: Cognitive tests
is_table: true
---


# <i class="fa fa-table"></i> Trial
{: .no_toc }


# Table of contents
{: .no_toc .text-delta }
- TOC
{:toc}


## Key

id [integer]
: The unique trial identifier, generated in temporal order (meaning that a greater `id` refers to a trial that occurred later in time).
unique in *<i class="fa fa-table"></i> Trial* (i.e., each row in *<i class="fa fa-table"></i> Trial* has a different `id` value.)

> This `id` is used by other tables. For example, there is a table called *<i class="fa fa-table"></i> Stimulus* that describes in greater detail the sequence of images shown during a trial, their timing and visual properties. That table will refer to this `id` in order to link those descriptions (typically multiple lines in the *<i class="fa fa-table"></i> Stimulus* table, to a unique row in the *<i class="fa fa-table"></i> Trial* table).
{: .note}


## Context

study_name [string]
: The name of the study the participant participated in.
: unique in *<i class="fa fa-table"></i> Study* table.


subject_id [string]
: The identifier of the entity (typically person) generating the responses.
: unique in *<i class="fa fa-table"></i> Subject* table.


session_index [integer]
: When there are multiple sessions, this variable indicates the order of each session (i.e., the first session completed by the subject has `session_index` = 1, the second session has `session_index` = 2; even if the second session is an exact repetition of the first one.
: indexes sessions within study and subject. 

> We currently don’t use `session_name`, `session_id` and `session_repetition` in this table.
{: .note}

## Task

instrument_name [string]
: The name of the instrument used for collecting data (e.g., the name of the computer script used to run the test).
: unique in *<i class="fa fa-table"></i> Instrument* table.


language_code [string]
: The language the task was completed in (expressed as the code within the [ISO_639-1 standard](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)). 


transformer_id [integer]
: Refers to the specific source-to-L1 data transformer (parameters) used to form this table (i.e., the ETL pipeline); the transformer embodies the definition of a trial for a particular task.
unique in *<i class="fa fa-table"></i> Transformer* table.


timeline_name [string]
: The name of the timeline currently implemented in the *<i class="fa fa-table"></i> Instrument* (e.g., the name of a specific version of a test the instrument supports).
: unique in *<i class="fa fa-table"></i> Timeline* table.


timeline_repetition [integer]
: The number of times this particular timeline has already been completed anytime in the past by this particular subject in this study.

> Repetition starts "counting" at 0.
{: .note }


multitask_type [enum]
: A timeline may require subjects to perform multiple tasks at the same time. This variable indicates the type of multitasking required by the timeline.
:  - **none:**  No multitasking, i.e., single-tasking;
:  - **concurrent:**  There are at least two independent tasks that need to completed in parallel;
:  - **compound:**  The task requires multiple successive stages or involves tasks that are dependent/coupled.

> This characterization of `multitasking_type` is rudimentary and will likely evolve in the future. 
{: .note }


job_type [string]
: The general type of operation the subject needs to perform. The job typically is expressed as a verb (e.g., "recall", "sort") and can be the same for different instruments (e.g., digit span test and spatial-span test both have a job of type "recall-forward").


job_description [string]
: The more specific description of a job, which gives more information about what the participant sees and has to do. Whereas the `job_type` typically uses only verbs and adjectives, the `job_description` also contains nouns (e.g., "recall-digits-forward", "recall-letters-backward").


block_type [enum]
: A block can have one of the following types: 
: - **tutorial:**  Typically a simplified version of the test designed to teach participants how the test works;
: - **practice:**  Typically identical to the test blocks but are used to get participants accustomed to the task in a no-stakes environment;
: - **test:**  Test blocks form the main test.
: - **instruction:**  Instruction blocks present participants the instructions for a given test as text and possibly images.


block_name [string]
: The name of a particular block in a timeline. If the same block is completed twice in a row, they would have different `block_index` values (1 and 2, respectively) but they would have the same block_name (e.g., "NB_timeline1_block1").
: unique within the *<i class="fa fa-table"></i> Timeline* table.


block_index [integer]
: Refers to the order in which this block has been experienced by the subject. When there are multiple blocks, this variable indicates the order of each block (i.e., the first block completed by the subject has `block_index` = 1, the second block has `block_index` = 2; even if the second block is an exact repetition of the first one.
: index of block within a timeline.


episode_index [integers separated by ;]
: Refers to a particular time interval, in chronological order, of the `timeline_run`. Episodes are temporally distinct (no overlap) and discrete. The binning of the `timeline_run` into successive episodes depends on the task; it is mostly used and necessary to group data in cases where two distinct trials occurred at the same time (e.g., dual N-back). 
: index of episode within a timeline.

> Note that in some cases two different trials may use data from partially different but overlapping episodes. For example, consider the 2-back task with the stimulus sequence *A-X-F-X*. The first trial involves the stimuli *A-X-F* and the second trial the sequence *X-F-X*; these two trials refer in fact to the same instances of stimuli *X* and *F*. To clarify that these two trials use overlapping episodes we specify `episode_index` = "1;2;3" in the first case and `episode_index` = "2;3;4" in the second case.
{: .note }

> Also, note that in cases where trials make use of data from multiple stimulus events without there being an overlap of such events across trials (for example, the AX-CPT task where a trial may be defined for example as the letters A or B followed by the letters X or Y), there is no need to list multiple episode indices within a trial---we nevertheless recommend listing them for consistency.
{: .note}


task_index [integer]
: when `multitask_type` is other than none, `task_index` refers to each of the individual tasks in a block. 
: index of the task within a block.


trial_index [integer]
: The index of the trial inside a block, starting from 1 and "counting" separately for each of the tasks within a block (e.g., if there are two "streams" within a block as in the dual N-back, this variable indexes trials separately for each stream). 
: index of trial within task and block.


trial_start_datetime [datetime]
: The date time of the beginning of the trial. This serves as the default temporal reference for other timing events within the trial (but there are some exceptions; e.g., the timing of a cue being expressed relative to the onset of a stimulus; see corresponding documentation).


trial_seed [integer]
: The seed used to initialize the <abbr title="Random Number Generator">RNG</abbr> and generate everything that is random in the trial. Knowing this seed it should in principle be possible to exactly reproduce the `timeline_run` as experienced by the subject.


## Stimulus
Describes the most relevant information about the stimuli presented during a given trial and provides information on where to find more detailed information about what exact stimuli were presented, how and when (this sub-trial data will be in separate tables).


stimulus_panel_count [integer]
: The number of panels or screen areas stimuli may appear on during the trial. For example, in a task where stimuli to be compared are presented on the left and right side of the screen, `stimulus_panel_count` = 2.


stimulus_structure [enum]
: We distinguish three stimulus structures: 
 - **unitary:**  Only one stimulus is shown, alone;
 - **set:**  Many stimuli are shown, either at the same time or not; order does not matter;
 - **sequence:**  Multiple stimuli are shown, either at the same time or not; order does matter (order may be indicated by the order of presentation or by a digit for example).


stimulus_structure_source_type [enum]
: Indicates the type of method used to generate the `stimulus_structure` (this is relevant when a trial displays a sequence of or set of stimuli):
 - **none:**  When `stimulus_structure` == unitary;
 - **preset:**  `stimulus_structure` is hard coded in a file;
 - **generator:**  A procedure was used to generate the stimulus_structure.


stimulus_structure_source [string]
: Refers to the specific generator used to produce the `stimulus_structure` (e.g., sequence of digits in a digit span test). When no generator was used, this variable has a value of none.


stimulus_set_size [integer]
: The number of different values each presented stimulus could have taken. This value gives an indication of the complexity of the stimulus space. When this number is large we set to infinity, when for any reason it was not computed, it has a value of NA. 

> To specify "infinity" in a CSV file we use `+Inf` and `-Inf`; these are correctly recognized in R (tidyverse) and Python (pandas) as being valid numbers rather than strings.
{: .note }


stimulus_count [integer]
: The number of stimuli shown to the participant during the trial.


stimulus_source_type [enum]
: A stimulus is typically created using a particular procedure/algorithm ("generator") or is sampled from a particular set ("set"). This variable indicates which of these two applies for the current stimulus.


stimulus_source [string]
: Refers to the specific generator or set the stimulus belongs to. Stimuli that stem from the same source have the same data scheme and could thus be described in a table named after `stimulus_source` (i.e., `stimulus_source` indicates which table contains the full information about the stimulus; e.g., "digit1to9").


stimulus_index_in_source [integer]
: Index of the stimulus within the table referred to by `stimulus_source`.
: For example, if `stimulus_source` == "digit1to9", `stimulus_index_in_source` = 1 refers to "1" while for `stimulus_source` == "LettersAtoD", `stimulus_index_in_source` = 1 refers to "A".

> It is not because a particular `stimulus_source` is used in a given timeline that all possible stimuli of that source are displayed to the user. For example, the AX-CPT may use "upper-case-letters" but only use a subset of those letters (e.g., "A", "B", "X", "Y"). Whenever possible, we specify the most relevant/specific set (e.g., "digit1to9" rather than "digit").
{: .note }

stimulus_position_index [integer]
: Refers to discrete positions on the screen the stimulus may appear on. The set and ordering of possible positions depends on the test. Whenever possible, it follows a natural order (left to right, top to bottom), but in free-form layouts, indices are arbitrary.


stimulus_description [string]
: A human readable, compact description of the main aspects of the stimulus. The description for a given stimulus depends on the task but follows a specific template for a given task. Because of this, it looks like the `stimulus_description` could be "parsed" and "tidied"---however, this is not the intention; parsed/tidied data will be available in other tables; description is for human readability and facilitates the understanding of the data.

> In some cases, when stimuli are too complex or can't be precisely described, a summary of all stimuli is given instead.
{: .note }


stimulus_uid [integer]
: Is a unique identifier for the (unitary, set or sequenquence of) stimuli presented during a trial; if those exact same stimuli are repeated in a different trial, that trial would have the same value for `stimulus_uid`.


stimulus_role [enum]
: A stimulus may play different roles within a trial. Below is a list of some possible roles:
: - **target:**  A stimulus the subject must process and which should trigger the completion of the response (e.g., classify, reach, memorize) if the subject is doing the task as intended. Note that in some cases (e.g., in a go/no-go task) the correct response to a stimulus is to NOT click the button. In this case, the stimulus that triggered the decision to NOT click the button is still a "target".  
: - **non_target:**  A stimulus the subject must process but which does not trigger the completion of the response (e.g., the first two stimuli in a 2-back test).
: - **distractor:**  A stimulus the subject should not process at all (i.e., ignore) and which is unrelated to the correct execution of the task.
: - **location_cue:**  A stimulus giving a spatial location information that subjects could use to improve their performance.
: - **job_specifier:**  A stimulus specifying which job the subject should perform. 
: - **stop_signal:**  A stimulus signaling the participant he should abort his current action.
: - **probe:**  A stimulus indicating about which stimulus to respond.

## Option
Describes the set of options that were offered to the subject for responding on a given trial. Information about the individual options within that set are stored in a different, sub-trial table.

option_source_type [enum]
: A set of options is typically created using a particular procedure/algorithm ("generator") or is sampled from a particular set ("set"). This variable indicates which of these two applies for the current options.


option_source [enum]
: Refers to the specific generator or set that determined the options on a given trial. Option that stem from the same source have the same data scheme and could thus be described in a table named after `option_source` (i.e., `option_source` indicates which table contains the full information about the option set).

> While there is a `stimulus_index_in_source` to refer to the particular stimulus that was used, we don’t have an equivalent `opiton_index_in_source` since all options are displayed. Instead, we use `response_index` and `expected_response_index` to refer to a particular option within the set of options.
{: .note }


option_count [integer]
: The number of options the participant can choose from on a given trial.


measurement_type [enum]
: Describes the type of measurement implied by Option which in turn has implications on how that data should be processed during analysis; takes a value in 
: - **nominal:**  Set of values, without order (e.g., {"Luxembourg", "France", "Germany"});
: - **ordinal:**  Ordered values without clear distance (e.g., {"a lot", "a bit", "not at all"});
: - **interval:**  Ordered values with clear distances but no absolute zero (e.g., 10 versus 20 degrees Celsius); 
: - **ratio:**  Values with clear distance metrics and absolute zero (e.g., length in cm).

## Input
Describes the kinds of actions the subject performed in a trial. 

input_interface_type [enum]
: Refers to the type of interface subjects used to input actions. Possible values include (non-exhaustive):
:  - **keyboard:**  A keyboard is displayed on the screen;
:  - **buttons:**  Dedicated buttons on the screen;
:  - **stimulus-button:**  Stimuli serves as buttons;
:  - **text-field:**  A text field is displayed on the screen;
:  - **slider:**  A slider is displayed on the screen;


input_action_type [enum]
: Refers to the type of action the subject performs to give a response. Possible values include (non-exhaustive):
 - mouse-click
 - mouse-release
 - key-press
 - key-release
 - mouse-drag
 - touch
 - swipe

> The type of `input_action` determines the structure of detailed response data (i.e., mouse-click data is different from key-press data).
{: .note }

input_count [integer]
: The number of inputs (i.e., actions) the user made during the trial.

> For mouse-drag, it corresponds to the number of drag points that have been sampled during the drag-and-drop.
{: .note }


## Expectation
Describes what response is expected from the subject (i.e., which response would evaluate to correct).

In general, expectation will display/refer to a particular option among the set of options offered to the subject (in choice tasks) and will have the same structure and format as the actual response data so that expected response and actual responses can be directly compared (e.g., if `response_index` == `expected_response_index`, then `correct` = TRUE).


expected_response_index [integer]
: The index of the option the subject is expected to choose from the set of options.

> When `expected_response_index` = 0, it means that the subject should not respond at all. 
{: .note }

> Sometimes stimuli serve both as stimuli and as response options as subjects have to click on a particular stimuli to give their response (e.g., spatial span, odd one out). It is convenient in those cases to use `stimulus_position_index` to order/index the options (i.e., `option_index` == `stimulus_position_index`) and consequently also the responses. 
{: .note }

expected_response_description [string]
A description of the expected response using the same convention as `response_description`.

## Response

response_structure [enum]
: The structure of the response required by the subject; can take values in:
:  - **unitary:**  The subject provides a single input (e.g., chooses option "same");
:  - **sequence:**  The subject provides a sequence of information, and the order matters (e.g., a sequence of memorized digits in their order of appearance); 
:  - **set:**  The subject provides a set of information, and the order does not matter (e.g., "list words that start with the letter "A"); 

> Note that the distinction between set and sequence refers to the importance of order information to evaluate if the response is correct or not; a response with a set structure may unfold over time (each piece of information is given in a particular temporal order) and it may be of scientific interest to take into account that order; however, the order itself is not important within the task itself. For example, in the [MOT task](https://en.wikipedia.org/wiki/Multiple_object_tracking) one may ask subjects to point to all dots that hide a token. If subjects point to all such dots they will be correct no matter in which order the dots were clicked in.
{: .note}


response_count [integer]
: Each trial contains by definition only one response. However, when `response_structure` is other than unitary, a response comprises multiple pieces of information (e.g., "3-5-7" could be one response in the digit span task and this response contains three components, namely "3", "5" and "7"). `response_count` refers to the number of components that make up a response (not the number of responses within a trial).

> `response_count` is different from `input_count`; a subject may in some cases change their response multiple times before submitting the final response. In such cases, there would be many more inputs than there are components to the final response.
{: .note }

> While we have `stimulus_set_size` we currently don’t have a `response_set_size`, but we do have `option_count` and `response_count`.
{: .note }

response_index [integer]
: The index of the option the participant chose, starting from 1.

> `response_index = 0` means the subject chose none of the options (e.g., a "no-go" response in a Go/No-go task).
{: .note }

> `response_index` can be directly compared to `expected_response_index`.
{: .note }

> `response_index` refers to an entry in the Option table (i.e., there is no *<i class='fa fa-table'></i> Response* table).
{: .note }


response_description [string]
: A description of participant’s response; typically the description of the option that was chosen.

> `response_description` can be directly compared to `expected_response_description`.
{: .note }


response_value [float]
: A numeric value associated with a particular response option; typically indicating the "worth" of a response (e.g., `response_value` = 1 for the correct response). Depending on the context, `response_value` can mean something different. In some cases `response_value` will be redundant with accuracy and correct.


response_time [float]
: The duration between the earliest possible time a response could have been completed and the moment that response was actually completed (and NOT when it was initiated).


timed_out [boolean]
: Some tasks require subjects to give a response within a certain time limit. When subjects fail to respond before that time runs out, `timed_out` is set to TRUE. 


## Evaluation

accuracy [float]
: A task-dependent accuracy measure ranging from 0 to 1 (inclusive).


correct [boolean]
: Indicates whether the response matches the expected response (i.e., `correct` = TRUE) or not (i.e., `correct` = FALSE).


evaluation_label [string]
: There are several labels that can be assigned to a given response to specify what that response means in terms of evaluation within a task. The most general terms are "correct" and "error" (which are already given by the `correct` variable). There are however more specific sets of terms that may apply in different contexts. For example, in a signal detection task, it is common to use labels from the signal detection theory framework (i.e., "hit", "miss", "false alarm", "correct rejection"). In other contexts, researchers might use terms like "omission" or "commission" errors or even things like "perseveration" error (e.g., in the Wisconsin Card Sorting Test). Note that these terms are not always well defined or exclusive. For example, a "hit" is also a "correct" response and a "false alarm" may be synonymous to "commision error". Whenever possible use the more specific terms (i.e., always use "hit" rather than "correct" when applicable).
: Here are few evaluation labels that are commonly used: 
:  - **correct:**  The response is correct;
:  - **error:**  The response is incorrect;
:  - **hit:**  The stimulus was "present" and the subject correctly responded "present";
:  - **miss:**  The stimulus was "present" and the subject incorrectly responded "absent";
:  - **fa:**  The stimulus was "absent" and the subject incorrectly responded "present";
:  - **cr:**  The stimulus was "absent" and the subject correctly responded "absent".


## Feedback
Describes what feedback was shown on a given trial. Because feedback hasn’t yet been fully specified in our data model we will use the most basic representation for feedback information in the trial table.

feedback_description [string]
: Lists the different kinds of feedback that were shown on a given trial. When multiple types of feedback were used, feedback will list them using `;` as a separator. If a given type of feedback was shown multiple times during a trial, that feedback type is listed only once (i.e., `feedback_description` does NOT represent the sequence of feedbacks).
: The possible values for feedback are:
:  - **none:**  No feedback was shown;
:  - **expected_response:**  Feedback indicated what the correct response would have been;
:  - **explanation:**  Feedback explains *why* a certain option is the correct one;
:  - **correctness_on_option:**  Feedback indicates (on the the option itself) if the option chosen by the participant was correct one (e.g., in green), or not (e.g., in red);
:  - **correctness_on_screen:**	 Feedback displayed on the screen center indicates if the response to the current trial was correct or not (e.g., using a green check or a red cross).

> This list is not exhaustive and characterizing feedback in the future will involve more variables (e.g., separating the type of information shown (e.g., correctness) and how it is shown ("on_option" versus "on_screen").
{: .note }

> We don’t consider here as "feedback", the kind of feedback that is used in UI to confirm to users that a button has indeed been clicked.
{: .note }


## Experimental Design

job_repeat [enum]
: Whether this trial's job has not been seen before in this timeline.
: The possible values for `job_repeat` are:
:  - **new:**  The job has never been seen before in this timeline.
:  - **repeat:**  The job is the same as the previous trial.
:  - **switch:**  The job is different from the previous trial but has been seen prior in the timeline.


## Accessories

additional_measures
: Indicates whether additional measures have been recorded during this trial and if so what kind of measures they are. Possible values include (non-exhaustive):
:  - none
:  - mouse_trajectories
:  - fmri
:  - eye_tracking
:  - heart_rate

