ticket=`git symbolic-ref -q HEAD | cut -c 12- | cut -d '/' -f 2 | cut -c -7`
if [ "$(grep -c "$ticket" CHANGELOG.md)" -lt 1 ]; then
    echo 'No changelog entry found for '$ticket'. Add one before continuing.'
    exit 1
fi