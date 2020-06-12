test -f $1
ret=$?
echo $ret
if [ $ret -eq 1 ] 
then
cat /dev/null > $1
echo "cree"       
fi
exit $ret
