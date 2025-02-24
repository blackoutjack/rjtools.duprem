
HASH=$1

if [[ -z "$HASH" ]]; then
    HASH=$(GIT_WORK_TREE="../rjtools.util" GIT_DIR="$GIT_WORK_TREE/.git" git hash | tr -d "\n")
    echo "Using rjtools.util hash $HASH"
fi



yes | pip uninstall util
sed -i 's/^\(git+.*\)@[0-9a-f]*#\(.*\)$/\1@'$HASH'#\2/' requirements.txt
pip install -r requirements.txt

