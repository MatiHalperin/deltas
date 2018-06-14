while read -r filename
do
    rm -rf "$filename"
done < delete_list