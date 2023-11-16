from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class MHGrader:
    def __init__(self, model_name="google/flan-t5-large"):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def createPrompt(self, answer, point, prompt_type=1):
        """Create a prompt for the model to grade the answer

        Args:
            answer (str): The answer to the question
            point (str): The point to be graded
            prompt_type (int, optional): The type of prompt to be used. Defaults to 1.

        Returns:
            str: The prompt for the model to grade the answer
        """
        match prompt_type:
            case 1:
                return f'{answer}\n\nBased on the paragraph above can we conclude that {point}?\n\n["yes", "no"]'
            case 2:
                return f'Answer based on context:\n\n{answer}\n\nIs the context saying that {point}?\nOptions:\n-yes\n-no'


    def gradePoint(self, answer, point, verbose=False):
        """Grade the answer based on the point specified

        Args:
            answer (str): The answer to the question
            point (str): The point to be graded
            verbose (bool, optional): Print the prompt and answer. Defaults to False.

        Returns:
            float: The grade of the answer
        """
        answers = []
        for prompt_type in [1, 2]:
            prompt = self.createPrompt(answer, point, prompt_type=prompt_type)
            verbose and print(f'Prompt: {prompt}')
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_length=200)
            ans = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            verbose and print('Output:', ans)
            verbose and print('-'*50)
            answers.append(ans)
        answers = list(map(lambda x: int('yes' in x.lower()), answers))
        grd = sum(answers) / len(answers)
        verbose and print(f'Grade w/o weight (out of 1): {grd}')
        return grd

    def grade(self, answer, points, weights=None, verbose=False):
        """Grade the answer based on the points specified

        Args:
            answer (str): The answer to the question
            points (list): The points to be graded
            weights (list, optional): The weights of each point. When None, it weighs equally. Defaults to None.
            verbose (bool, optional): Print the prompt and answer. Defaults to False.

        Returns:
            float: The grade of the answer
        """
        if weights is None:
            weights = [1] * len(points)
        assert len(weights) == len(points), 'The length of weights and points must be the same'
        grades = [self.gradePoint(answer, point, verbose=verbose) for point in points]
        grd = sum([w * g for w, g in zip(weights, grades)])
        verbose and print(f'Final Grade (out of {sum(weights)}): {grd}')
        return grd, [(w * g, w) for w, g in zip(weights, grades)]
        
if __name__ == '__main__':
    grader = MHGrader()

    points = [
        'The initial position of centroids in K-Means clustering is so important',
        'Choosing the value of k is so important in K-Means clustering',
    ]

    answer = "K-means clustering heavily depends on the initial centroids. Choosing inappropriate initial centroids may cause the algorithm to converge to a suboptimal solution, leading to inaccurate cluster assignments."

    grade, detail = grader.grade(answer, points, weights=[3, 2], verbose=False)

    print(f'Answer: {answer}')
    print('-'*50)
    for i, (g, w) in enumerate(detail):
        print(f'Point {i+1}: {g} out of {w}')
    print('-'*50)
    print(f'Final Grade: {grade}')