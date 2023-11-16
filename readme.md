#  AutoGrade
## 1. Introduction
This tool is designed to be a simple, easy to use, and easy to extend autograder for assignments or exams. It is designed to help TAs and instructors grade assignments and exams. It is not designed to be a replacement for a human grader, but rather to help the grader by automating the tedious parts of grading. 

I've used flan-t5-large, a famous and open-source Large Language Model (LLM), to grade the assignments. The model is trained on a large dataset of English text, and it can be used to generate text, answer questions, and summarize text. I've used the model to grade the documents.

Several prompts, based on the training procedure of flan-t5, is used to grade each part of an answer. The model is being used in a zero-shot setting. The model is not fine-tuned on the dataset, and it is used as it is. I've tested this script on several manually graded answers, and it did a great job. However, it is not perfect, and it can make mistakes. Therefore, I recommend that you check the answers manually before submitting the grades.

## 2. Installation
### 2.1. Requirements
- Python 3.10 or higher

### 2.2. Install the requirements
```bash
pip install -r requirements.txt
```
You can also use the docker image to run the script. It's much easier this way. Just use the following command to run the script:
```bash
./docker.sh
```

## 3. Usage
### 3.1. Prepare the data





