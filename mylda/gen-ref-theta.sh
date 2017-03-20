#! /bin/bash
model_str=$1
ref_file=$2

java -cp /home/gwlin/dev/JGibbLDA-v.1.0/bin:/home/gwlin/dev/JGibbLDA-v.1.0/lib/args4j-2.0.6.jar jgibblda.LDA -inf -model $model_str -dfile $(basename $ref_file) -dir $(dirname $ref_file)

echo "I have a little donkey!\n"
