#!/bin/bash
dir_commands=$1
id=$2
out_base="/edx/var/edxapp/staticfiles/codebrowser"
#out_base="/home/zyu/xblock-codebrowser/codebrowser"
woboq_base="/edx/var/edxapp/woboq_codebrowser"
output_dir=$out_base/$id
data_dir=$out_base/"data"

if [ -d $output_dir ]
then
    rm -r $output_dir
fi

echo "$output_dir"
echo "$dir_commands"

$woboq_base/generator/codebrowser_generator -b $dir_commands -a -o $output_dir -p ucore_plus:/home/zyu/ucore_plus/ucore

$woboq_base/indexgenerator/codebrowser_indexgenerator $output_dir

if [ ! -d $data_dir ]
then
    ln -s $woboq_base/data $out_base/
fi



