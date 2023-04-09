#!/usr/bin/env python3
# Author: Valentin Barriere
# Evaluation script for CoFE shared task: subtask-4, Touché Lab, CLEF 2023 

import argparse
import pandas as pd

to_round = 4

def calculatePRF(gold,prediction):
	"""
	gold/prediction list of list of classification predictions 
	"""
	# initialize counters
	labels = set(gold+prediction)
	tp = dict.fromkeys(labels, 0.0)
	fp = dict.fromkeys(labels, 0.0)
	fn = dict.fromkeys(labels, 0.0)
	precision = dict.fromkeys(labels, 0.0)
	recall = dict.fromkeys(labels, 0.0)
	f = dict.fromkeys(labels, 0.0)
	# check every element
	for g,p in zip(gold,prediction):
		# TP 
		if (g == p):
			tp[g] += 1
		else:
			fp[p] += 1
			fn[g] += 1
	# print("Label\tTP\tFP\tFN\tP\tR\tF")
	for label in labels:
		recall[label] = 0.0 if (tp[label]+fn[label]) == 0.0 else (tp[label])/(tp[label]+fn[label])
		precision[label] = 1.0 if (tp[label]+fp[label]) == 0.0 else (tp[label])/(tp[label]+fp[label])
		f[label] = 0.0 if (precision[label]+recall[label])==0 else (2*precision[label]*recall[label])/(precision[label]+recall[label])
		microrecall = (sum(tp.values()))/(sum(tp.values())+sum(fn.values()))
		microprecision = (sum(tp.values()))/(sum(tp.values())+sum(fp.values()))
		microf = 0.0 if (microprecision+microrecall)==0 else (2*microprecision*microrecall)/(microprecision+microrecall)
	# Macro average
	macrorecall = sum(recall.values())/len(recall)
	macroprecision = sum(precision.values())/len(precision)
	macroF = sum(f.values())/len(f)

	accuracy = 0
	for label in labels:
		accuracy += tp[label]

	accuracy = accuracy/len(gold)

	return round(microrecall,to_round),round(microprecision,to_round),round(microf,to_round),round(macrorecall,to_round),round(macroprecision,to_round),round(macroF,to_round),round(accuracy,to_round)


def create_dict_results(dfgt, dfp, lan=None):
	"""
	"""

	# gold = dfgt['label'].values.astype(list)
	gold = list(dfgt['label'].values)
	# rediction = dfp['prediction'].values.astype(list)
	prediction = list(dfp['prediction'].values)

	microrecall,microprecision,microf,macrorecall,macroprecision,macroF,accuracy = calculatePRF(gold, prediction)

	dict_res_lan = {
	'Micro Recall': microrecall, 
	'Micro Precision': microprecision, 
	'Micro F1-Score': microf, 
	'Macro Recall': macrorecall, 
	'Macro Precision': macroprecision, 
	'Macro F1-Score': macroF, 
	'Accuracy': accuracy}

	return dict_res_lan


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Evaluate submissions to the clickbait spoiling task.')
	parser.add_argument('--input_run', type=str, help='The input run (expected in tsv format) produced by a system that should be evaluated.', default='CFS_toy_pred.tsv')
	parser.add_argument('--ground_truth', type=str, help='The ground truth classes used to evaluate submissions to task 1 (spoiler type generation).', default='CFS_toy.tsv')
	# parser.add_argument('--task', type=str, help='The task to evaluate. Choose 1 (spoiler type classification) or 2 (spoiler generation).', choices=['1', '2'], required=True)	
	args = parser.parse_args()

	# GT file
	dfgt = pd.read_csv(args.ground_truth, sep='\t', index_col=False)
	# predictions of the participant, using the first column as index
	dfp = pd.read_csv(args.input_run, sep='\t', header=None, names=['id', 'prediction'])

	assert len(dfp) == len(dfgt), 'Submitted file has not the same lenght than the ground truth file'

	for id_gt, id_pred in zip(dfgt['id'].values.astype(list), dfp['id'].values.astype(list)):
		assert id_gt == id_pred, 'The first column containing the comments ids is different than the one from the ground truth file. Check order or missing samples'

	dict_results = {'all': create_dict_results(dfgt, dfp)}

	for lan in dfgt['lan'].unique():
		bool_lan = dfgt['lan'] == lan
		dict_results[lan] = create_dict_results(dfgt[bool_lan], dfp[bool_lan], lan)

	print(dict_results)
