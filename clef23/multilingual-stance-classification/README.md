
# Synopsis

* **Task**: Given a proposal on a socially important issue, the task is to classify whether a comment is in favor, against, or neutral towards the proposal.
* **Input**: A proposal and an associated comment, with metadata.
* **Communication**: Subscribe to the [Googlegroup](https://groups.google.com/g/clef-2023-cofe-shared-task). 
* **Submission**: A tsv file containing the id of the comment, and stance of the comment towards its associated proposal (*In Favor*, *Against*, or *Other*). 
* **Evaluation**: Submissions will be evaluated using [this script](https://drive.google.com/file/d/1T-QO1dkfXhMxzOtHxNLS_vdAbsCoVVFf/view?usp=sharing), using the [TIRA platform](https://www.tira.io/task/touche-2023-task-4). 

# Tasks

The goal of the **Tasks 4** is to support opinion formation on socially important topics. Given a proposal text on a socially important issue, the task is to classify whether a comment is *In Favor*, *Against*, or *Other* towards the proposal. 

Other metadata will be given to the participants: 
* For the proposals: the title of the proposal, the topic, the ID of the writter, the language of the text and the number of endorsments. 
* For the comments: the ID of the writter, the language of the text and the number of up/downvote.

The proposals and titles can be written in any of the 24 EU languages (plus Catalan and Esperanto), and they will come with their automatic English translation. 

## Subtask 1: Cross-Debate Classification

In the first subtask, the participants cannot use in their training set the examples from debates that are in the test set. 

## Subtask 2: All-data-available

In the second subtask, the participants can use all the available data, labeled or unlabeled. 


# Datasets

The data used in this Shared Task comes from the CoFE dataset, presented at AACL-IJCNLP 2022 [[Oral presentation]](https://drive.google.com/file/d/1ARE-Po6rWEvOkTuaCVOZpSj0Eb9qpTk8/view?usp=sharing) [[Slides]](https://drive.google.com/file/d/1D3ao_A3bKx-Xd1JK0c8t8Uv_x6NSGU8N/view?usp=sharing)  

## Comments 

### CF$_S$

This is a dataset composed of 7k comments from CoFE that are annotated in stance by the writer him/herslef. The self-annotation is binary: *In favor* or *Against*. It can be found in the column `alignment`. 

### CF$_U$

This is a dataset composed of 12k unlabeled comments from CoFE. All the `alignment` are `None`. 

### CF$_E$-Dev

This is a dataset composed of multiligual comments that have been annotated by external coders (not the writer of the comment him/herself) in a 3-class fashion. It is consider as silver-standard because of low inter-annotator-agreement. The labels are in the columns `label`. Note that all the `alignment` of those comments are `None`. 

### CF$_E$-Test

This is a dataset composed of 1.2k comments in English, French, German, Italian, Greek and Hungarian that have been annotated by external coders (not the writer of the comment him/herself) in a 3-class fashion. It is considered as gold-standard because of higher inter-annotator-agreement. This dataset will used for the test phase. This test set will be available a few days before the test phase. 

### Links to download the comments

The datasets to use for the *Subtask 1: Cross-Debate Classification* are the ones below:
* CF$_U$ without the comments from the debates of the test set CF$_E$-Test, it is available [here](https://drive.google.com/file/d/1Sf3j0phfcCwD3ZYmNuUdOYlc-5yV8Da2/view?usp=sharing) 
* CF$_S$ without the comments from the debates of test set CF$_E$-Test, it is available [here](https://drive.google.com/file/d/1SbVLDIM8aARTUdwxJESM-6bucsLz-wk0/view?usp=sharing)
* CF$_E$-Dev without the comments from debates of the test set CF$_E$-Test, it is available [here](https://drive.google.com/file/d/1SfaGsZu7P3JKyLXckpitXpWqqSsRmVeN/view?usp=sharing)


The datasets to use for the *Subtask 2: All-data-available* are the ones below:
* CF$_U$, it is available [here](https://drive.google.com/file/d/1SOlTUmlIhdIKKeGVVTwyNihApgQAC_Nd/view?usp=sharing) 
* CF$_S$, it is available [here](https://drive.google.com/file/d/1SOiEDLdlIzWpWJlSBMQoP9TfUqBBMHTv/view?usp=sharing)
* CF$_E$-Dev, it is available [here](https://drive.google.com/file/d/1SKQhew5AdQw59oGsawHzqy4GZ9GU-OcN/view?usp=sharing)


The teams are free to use every other datasets they want to. 

## The proposals

All the proposals are in a separated file containing all the 4.2k proposals. The column `id` of the proposal file correspond to the column `id_prop` of the comment files. 

It is publicly available [here](https://drive.google.com/file/d/1R-eAEghjAns6CjC7P48DH1wOWYKHcvEx/view?usp=sharing). 

## Example data instance for Task 4:

### Proposals 

|    id | title                                 | proposal                                                                                                                                                                                                                                                                        | proposal_en                                                                                                                                                                                                                                                                                                  | title_en                                         | Topic        | lan   |   endorsements |
|------:|:--------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|:-------------|:------|---------------:|
| 43992 | Massentierhalter EU-Agrarsubventionen | Die EU hat "schöne" Ideen und arbeitet an Gesetzte für den Tierschutz und die Umwelt. Doch solange immer noch Massentierbetriebe von der EU durch Subventionen unterstützt werden, ist dies alles nicht glaubwürdig!                                                            | The EU has “beautiful” ideas and is working on legislation for animal welfare and the environment. But as long as EU subsidies still support mass animal farms, all of this is not credible!                                                                                                                 | Mass livestock farmers EU agricultural subsidies | GreenDeal    | de    |              1 |
| 11138 | Författningsdomstol                   | För att säkra skyddet av konstitutionen i varje EU-land bör krav ställas av EU att en oberoende konstitutionsdomstol finns i varje land. Exempelvis saknas en sådan i Sverige vilket leder till låg kvalité på stiftade lagar samt lagar som inte är anpassade till grundlagen. | In order to ensure the protection of the Constitution in each EU country, the EU should be required to have an independent constitutional court in each country. For example, there is no one in Sweden, which results in a low quality of enacted laws and laws that are not in line with the Constitution. | Constitutional court                             | ValuesRights | sv    |              0 |posa | The Catalá llengua Europa                              | ValuesRights | ca    |              2 |

### Comments 

| id            |   id_prop | alignment   | comment                                                                                                                                                                                                                                                                                                                           |   depth | thread_id     | last_comment_in_thread   |   upvote |   downvote | Topic        | lan   | time  |
|:--------------|:----------|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------:|:--------------|:-------------------------|---------:|-----------:|:-------------|:------|:----------------|
| comment_90817 |     89992 | Against     | Europäische Waffenexporte leisten einen großen Beitrag zum Elend in der Welt [...]                                                                                                                       |       0 | comment_90817 | True                     |        0 |          0 | EUInTheWorld | de    | 2021-09-14 10:28:46+02:00 |
| comment_1330  |       417 | Against     | Je ne comprend pas très bien ce que l'on reproche a l'UE (vous devriez pouvoir m'éclairer) [...]  |       0 | comment_1330  | True                     |        3 |          0 | ValuesRights | fr    | 2021-04-22 18:55:25+02:00 |


# Baseline

The file [baseline/baseline-stance-classification.py](baseline/baseline-stance-classification.py) contains a baseline that always predicts "In favor".

To run the baseline on the toy dataset as it would be executed in TIRA, please run (please install the tira utility with `pip install tira` first):

```
tira-run \
	--image webis/touche-multilingual-stance-classification-baseline:0.0.1 \
	--input-directory ${PWD}/example-data/toy-input \
	--command '/baseline-stance-classification.py --input $inputDataset/data.tsv --output $outputDir/run.tsv'
```

This has produced a file `tira-output/run.tsv` (see output via `head -3 tira-output/run.tsv`):

```
comment_886	In favor
comment_39734	In favor
comment_87319	In favor
```

You can then evaluate this using the command `docker run --rm -ti -v ${PWD}/example-data/:/data -v ${PWD}/tira-output:/run -v ${PWD}:/out webis/touche-multilingual-stance-classification-evaluator:0.0.1 --input_run /run/run.tsv --ground_truth /data/toy-truth/data.tsv --output_prototext /out/evaluation.prototext`.

To run the baseline in TIRA, please click on "Docker Submission" -> "Upload Images" to upload your image and subsequently add the software with the command `/baseline-stance-classification.py --input $inputDataset/data.tsv --output $outputDir/run.tsv`. Please find a more detailed instruction on how to add your software to tira at [https://www.tira.io/t/how-to-make-a-software-submission-with-docker](https://www.tira.io/t/how-to-make-a-software-submission-with-docker).

You can build the baseline via

```
docker build -t webis/touche-multilingual-stance-classification-baseline:0.0.1 baseline
```

You can push the baseline via `docker push` (please adjust the tag accordingly as in your personalized documentation):
```
docker push webis/touche-multilingual-stance-classification-baseline:0.0.1
```


# Evaluation

Results will be evaluated using a macro-averaged F1-score over the 3 classes, overall and per language. 

### Build the evaluator

```
docker build -t webis/touche-multilingual-stance-classification-evaluator:0.0.1 evaluation
docker push webis/touche-multilingual-stance-classification-evaluator:0.0.1
```

Run the evaluation with docker:

```
docker run --rm -ti -v ${PWD}/example-data/:/data -v ${PWD}:/out webis/touche-multilingual-stance-classification-evaluator:0.0.1 --input_run /data/toy-run/run.tsv --ground_truth /data/toy-truth/data.tsv --output_prototext /out/evaluation.prototext
```

In TIRA, add the evaluator with: `/evaluation.py --ground_truth $inputDataset/data.tsv --input_run $inputRun/run.tsv --output_prototext $outputDir/evaluation.prototext`

