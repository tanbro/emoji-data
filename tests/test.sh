set -e

pyversion_array=( "3.7" "3.8" "3.9" "3.10" "3.11" )

for pyversion in "${pyversion_array[@]}"
do
    python${pyversion} -VV
    echo ""
    python${pyversion} -m pip install --root-user-action=ignore . && python${pyversion} -B -m unittest -v
    echo ""
    echo "======================================================================"
    echo ""
done
