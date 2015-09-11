echo "I am doing my work...."
mkdir output
python code4.py 
python eval_scramble.py output/unscrambled.en original.en

echo "Give me some time to check how good my alignments are..."
python compareAlignments.py alignment_sample_model1.txt output/alignments4IBM1.txt > output/alignmentlog1
python compareAlignments.py alignment_sample_model2.txt output/alignments4IBM2.txt > output/alignmentlog2
