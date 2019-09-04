for i in {1..50}
do
    sleep 0.5
    xid=$(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2)
    pname=$(xprop -id $xid _NET_WM_NAME) 
    echo $pname >> test.txt
done