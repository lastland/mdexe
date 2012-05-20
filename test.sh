#/bin/bash

testdir=test/
testsrcdir=$testdir"test-src/"
testresdir=$testdir"test-res/"
testworkdir=$testdir"tmp/"
testfiles=(Test.file Test.markdown Test-Content.markdown)

originpwd=$PWD
program=$PWD/mdexe.py

if test -d $testworkdir
then
    echo "$testworkdir already exists. Trying to clean it up."
    rm -r $testworkdir
    echo "Done."
fi

mkdir $testworkdir

echo "Copying test files into working directory."
for i in "${testfiles[@]}"; do
    echo $testsrcdir$i
    cp $testsrcdir$i $testworkdir
done
echo "Done."

echo "Start testing mdexe exec."
cd $testworkdir
python2 $program \exec Test.markdown
cd $originpwd
echo "There would be no following lines if test is correct."
diff $testresdir"Test.file" $testworkdir"Test.file"
