mkdir output
echo "Working on Problem 4..."
python code/question4.py 
python eval_tagger.py tag_dev.key output/tag_dev.out

echo "Working on Problem 5: Bigram, tagging and suffix features"
python code/question5.py
python code/question5b.py
python eval_tagger.py tag_dev.key output/tag_dev5b.out

echo "Working on Problem 6 : Additional feature: <previous word, current tag>..."
python code/question6a_1.py
python code/question6b_1.py
python eval_tagger.py tag_dev.key output/tag_dev6_1.out

echo "Working on Problem 6 : Additional feature: <previous two words, current tag>..."
python code/question6a_2.py
python code/question6b_2.py
python eval_tagger.py tag_dev.key output/tag_dev6_2.out

echo "Working on Problem 6 : Additional feature: <current word, next word, current tag>..."
python code/question6a_3.py
python code/question6b_3.py
python eval_tagger.py tag_dev.key output/tag_dev6_3.out