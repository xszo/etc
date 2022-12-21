#!/bin/zsh

genList=( net/main net/rule )

optOut=false
while getopts "o" opt; do
  case ${opt} in
    o ) optOut=true ;;
esac; done

rm -Rf gen
cp -Rf gen.d gen
python gen.py
for item in ${genList[@]}; do
  git checkout ${item}
  python gen.py
done

if [ ${optOut} = true ]; then
  if git checkout o; then
    cp -Rf gen/* .
    git add -A
    git commit -qm gen --amend --reset-author
    git push -f
fi; fi

git checkout main
