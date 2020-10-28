#!/bin/bash
#set -ex
set -e


#cd "$(dirname "$0")"
cd `dirname "$0"`
echo "[当前目录: ] $(pwd)"

git add .
git status
#echo $?

echo '------------------------------------------------------------------------------------'
echo '请输入本次更新的注释:　'
read message

if [[ ${message} = "q" ]]
then
    # 通过输入 q, 直接推出当前脚本
    exit 1
elif [[ ${message} = "d" ]]
then
    echo "使用默认注释，进行更新"
    git commit -m "更新"
elif [[ -n ${message} ]]
then
    git commit -m "${message}"
else
    echo "请输入本次更新信息"
fi

echo '------------------------------------------------------------------------------------'
echo "是否向远程分支推送本次修改"
read is_push

case ${is_push} in
"y" | "yes")
  git push origin master;;
"q" | "exit" | "e")
 echo "退出,不推送到远程分支"
 exit 1;;
 *)
 echo "退出";;
esac
echo '---------------------------------[end]-----------------------------------------------'