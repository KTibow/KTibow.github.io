rm -r lighthouse || true
mkdir lighthouse
cat sitemap.txt | while read line
do 
  filename=`date "+%s"`
  lighthouse --chrome-flags="--headless" --output=json --output-path="./lighthouse/${filename}.json" $line
  lighthouse --chrome-flags="--headless" --output-path="./lighthouse/${filename}.html" $line
done
rm .json || true
ls ./lighthouse/*.json
