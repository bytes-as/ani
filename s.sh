ROOT=${1}
ROOT="/home/bt0/16CS10008/ani"
GRAPH1=${2}
MIN1=${3}
FREQ1=${4}
GRAPH2=${5}
MIN2=${6}
FREQ2=${7}
DICT=${10}


SCRIPTS="${ROOT}"/scripts
OUTPUT="${ROOT}"/outputs

PYTHON="/home/bt0/16CS10008/anaconda3/envs/tf_gpu/bin/python"

# Conversion dictionaries generation and frequncy generation
$PYTHON "${SCRIPTS}"/process_frequency.py "${FREQ1}" english $OUTPUT # --OVERWRITE
$PYTHON "${SCRIPTS}"/process_frequency.py "${FREQ2}" hindi $OUTPUT # --OVERWRITE

# generating queries
$PYTHON "${SCRIPTS}/create_queries.py" $FREQ1 "english" ${OUTPUT} 10000 --OVERWRITE # ${MIN1}  --OVERWRITE
$PYTHON "${SCRIPTS}/create_queries.py" $FREQ2 "hindi" ${OUTPUT} 10000  --OVERWRITE # ${MIN2} --OVERWRITE


# cutting graph, processing
$PYTHON "${SCRIPTS}"/process_graph.py "${GRAPH1}" english $OUTPUT "${MIN1}" #  --OVERWRITE
$PYTHON "${SCRIPTS}"/process_graph.py "${GRAPH2}" hindi $OUTPUT "${MIN2}" # --OVERWRITE

# running deepwalk on both the graph
$PYTHON "${SCRIPTS}"/deepwalk.py --input "${OUTPUT}/english_int_${MIN1}.graph" --format edgelist --walks-output "${OUTPUT}/english_int_${MIN1}.walks"  --number-walks ${8} #--OVERWRITE

$PYTHON "${SCRIPTS}"/deepwalk.py --input "${OUTPUT}/hindi_int_${MIN2}.graph" --format edgelist --walks-output "${OUTPUT}/hindi_int_${MIN2}.walks" --number-walks ${9} #--OVERWRITE

# Converte walks from int to word
$PYTHON "${SCRIPTS}"/convert_walks.py "${OUTPUT}/english_int_${MIN1}.walks" "${OUTPUT}/english.int2word" "${OUTPUT}/english_word_${MIN1}.walks" --OUT_DELIMITER ' '  #--OVERWRITE

$PYTHON "${SCRIPTS}"/convert_walks.py "${OUTPUT}/hindi_int_${MIN2}.walks" "${OUTPUT}/hindi.int2word" "${OUTPUT}/hindi_word_${MIN2}.walks" --OUT_DELIMITER ' '  #--OVERWRITE

# generate word embedding on first language
"${SCRIPTS}"/fasttext skipgram -input "${OUTPUT}/english_word_${MIN1}.walks" \
   -output "${OUTPUT}/english_${MIN1}" \
   -lr 0.025 -dim 100 -ws 5 -epoch 1 -minCount 5 -neg 5 -loss ns -bucket 2000000 \
   -minn 3 -maxn 6 -thread 4 -t 1e-4 -lrUpdateRate 100

# generate word embedding on the second language
"${SCRIPTS}"/fasttext skipgram -input "${OUTPUT}/hindi_word_${MIN2}.walks" \
   -output "${OUTPUT}/hindi_${MIN2}" \
   -lr 0.025 -dim 100 -ws 5 -epoch 1 -minCount 5 -neg 5 -loss ns -bucket 2000000 \
   -minn 3 -maxn 6 -thread 4 -t 1e-4 -lrUpdateRate 100

# echo "generating vector files for first language:"
#rm "${OUTPUT}/english_${MIN1}.vec"
cat "${OUTPUT}/english_10000.queries" | ${SCRIPTS}/fasttext print-word-vectors "${OUTPUT}/english_${MIN1}.bin" > "${OUTPUT}/english_${MIN1}.vec"

# echo "generating vector files for second language:"
#rm "${OUTPUT}/hindi_${MIN2}.vec"
cat "${OUTPUT}/hindi_10000.queries" | ${SCRIPTS}/fasttext print-word-vectors "${OUTPUT}/hindi_${MIN2}.bin" > "${OUTPUT}/hindi_${MIN2}.vec"

$PYTHON ${SCRIPTS}/fasttext2word2vec.py "${OUTPUT}/english_${MIN1}.vec"
$PYTHON ${SCRIPTS}/fasttext2word2vec.py "${OUTPUT}/hindi_${MIN2}.vec"


echo "mapping embeddings: supervised"
$PYTHON ${SCRIPTS}/map_embeddings.py --supervised $DICT \
	"${OUTPUT}/english_${MIN1}.vec" \
	"${OUTPUT}/hindi_${MIN2}.vec" \
        "${OUTPUT}/english_${MIN1}_supervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_supervised.cvec"
echo "mapping embedding: semi_supervised"
$PYTHON ${SCRIPTS}/map_embeddings.py --semi_supervised $DICT --cuda \
        "${OUTPUT}/english_${MIN1}.vec" \
        "${OUTPUT}/hindi_${MIN2}.vec" \
        "${OUTPUT}/english_${MIN1}_semi_supervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_semi_supervised.cvec"
echo "mapping embedding: unsupervised"
$PYTHON ${SCRIPTS}/map_embeddings.py --unsupervised --cuda \
        "${OUTPUT}/english_${MIN1}.vec" \
        "${OUTPUT}/hindi_${MIN2}.vec" \
        "${OUTPUT}/english_${MIN1}_unsupervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_unsupervised.cvec"


# finally evaluation using vecmap scripts
echo "evaluating embeddings: supervised"
$PYTHON $SCRIPTS/eval_translation.py \
        "${OUTPUT}/english_${MIN1}_supervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_supervised.cvec" \
	-d $OUTPUT/test_dict.txt
echo "evaluating embeddings: semi_supervised"
$PYTHON $SCRIPTS/eval_translation.py \
        "${OUTPUT}/english_${MIN1}_semi_supervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_semi_supervised.cvec" \
        -d $OUTPUT/test_dict.txt
echo "evaluating embeddings: unsupervised"
$PYTHON $SCRIPTS/eval_translation.py \
        "${OUTPUT}/english_${MIN1}_unsupervised.cvec" \
        "${OUTPUT}/hindi_${MIN2}_unsupervised.cvec" \
        -d $OUTPUT/test_dict.txt

<<MERGE_WALKS_PROCESS
# Merge walks
$PYTHON "${SCRIPTS}"/merge_walks.py "${OUTPUT}/english_word_${MIN1}.walks" "${OUTPUT}/hindi_word_${MIN2}.walks" $DICT "${OUTPUT}/merged_walks_${MIN1}_${MIN2}.walks" --WALKS_DELIMITER ' ' --OUTPUT_DELIMITER ' ' #--OVERWRITE


# generate word embedding on the merged walks
#"${SCRIPTS}"/fasttext skipgram -input "${OUTPUT}/merged_walks_${MIN1}_${MIN2}.walks" \
#   -output "${OUTPUT}/merged_walks_${MIN1}_${MIN2}" \
#   -lr 0.025 -dim 100 -ws 5 -epoch 1 -minCount 5 -neg 5 -loss ns -bucket 2000000 \
#   -minn 3 -maxn 6 -thread 4 -t 1e-4 -lrUpdateRate 100


# echo "generating vector files for merged walks:"
rm "${OUTPUT}/english_${MIN1}_${MIN2}.cvec"
cat "${OUTPUT}/english_10000.queries" | ${ROOT}/fastText/fasttext print-word-vectors "${OUTPUT}/merged_walks_${MIN1}_${MIN2}.bin" >> "${OUTPUT}/english_${MIN1}_${MIN2}.cvec"


rm "${OUTPUT}/hindi_${MIN1}_${MIN2}.cvec"
cat "${OUTPUT}/hindi_10000.queries" | ${ROOT}/fastText/fasttext print-word-vectors "${OUTPUT}/merged_walks_${MIN1}_${MIN2}.bin" >> "${OUTPUT}/hindi_${MIN1}_${MIN2}.cvec"

$PYTHON ${SCRIPTS}/fasttext2word2vec.py "${OUTPUT}/english_${MIN1}_${MIN2}.cvec"
$PYTHON ${SCRIPTS}/fasttext2word2vec.py "${OUTPUT}/hindi_${MIN1}_${MIN2}.cvec"


# becasue of prerequisite of vecmap evaluation script, we need to change the delimiter
#python $SCRIPTS/changeDelimiter.py $DICT $OUTPUT/test_dict.txt --out_dlim ' '

# finally evaluation using vecmap scripts
$PYTHON $ROOT/vecmap/eval_translation.py $OUTPUT/english_${MIN1}_${MIN2}.cvec $OUTPUT/hindi_${MIN1}_${MIN2}.cvec -d $OUTPUT/test_dict.txt
MERGE_WALKS_PROCESS
