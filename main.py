import os
import argparse
import pandas as pd
from tqdm import tqdm
from mh_grader import MHGrader
import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--answers", type=str, required=True, help="Path to the answers excel (xlsx) file")
parser.add_argument("-g", "--grading", type=str, required=True, help="Path to the grading csv file")
parser.add_argument("-o", "--output", type=str, required=False, help="Path to the output csv file")

args = parser.parse_args()

assert os.path.exists(args.answers), f'Path to answers csv file does not exist: {args.answers}'
assert os.path.exists(args.grading), f'Path to grading csv file does not exist: {args.grading}'

##  Reading the points that each answer should have mentioned...
log.info(f'Reading the points that each answer should have mentioned from {args.grading}...')
df_points = pd.read_csv(args.grading)
points, weights = df_points['Point'].tolist(), df_points['Weight'].tolist()

##  Reading the answers...
log.info(f'Reading the answers from {args.answers}...')
df_anwers = pd.read_excel(args.answers)

##  Output dataframe...
log.info(f'Creating the output...')
df_res = pd.DataFrame(columns=['Student ID'] + [f'Point {i+1} ({weights[i]})' for i in range(len(points))] + ['Final Grade'])

##  Grading the answers...
grader = MHGrader()
for i, row in tqdm(df_anwers.iterrows(), total=len(df_anwers)):
    student_id = row['Student ID']
    answer = row['Answer']
    grade, detail = grader.grade(answer, points, weights=weights, verbose=False)
    df_res.loc[i] = [student_id] + [g for g, _ in detail] + [grade]

df_res['Student ID'] = df_res['Student ID'].astype(int)

##  Saving the output...
if args.output is None:
    args.output = os.path.splitext(args.answers)[0] + '_graded.csv'
df_res.to_csv(args.output, index=False)

log.info(f'Grading completed. Output saved to {args.output}')