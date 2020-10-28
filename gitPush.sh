#!/bin/bash
#set -ex
set -e


#cd "$(dirname "$0")"
cd `dirname "$0"`
echo $(pwd)

git add .
git status
#echo $?

echo '请输入本次更新的注释:　'
read message

if [[ -n ${message} ]]
then
    git commit -m "${message}"

elif [[ ${message} = "d" ]]
then
    echo "使用默认注释，进行更新"
    git commit -m "更新"
else
    echo "请输入本次更新信息"
fi

echo "是否向远程分支推送本次修改 $(read is_push)"


case ${is_push} in
"y" | "yes")
  git push origin master;;
 *)
 echo "没有提交本次更新";;
esac
