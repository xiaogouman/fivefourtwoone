set -ex
types=("READ UNCOMMITTED" "READ COMMITTED" "REPEATABLE READ" "SERIALIZABLE")
for type in "${types[@]}"
do
    echo $type
    for p in 1 10 20 30 40 50 60 70 80 90 100
    do
        e=$((2000 / p))
        echo $p, $e
        for execute_ct in {1..20}
        do
            output=$(python -W ignore run_experiments.py 100 $e $p "$type")
            correctness=$(echo $output | cut -f2 -d' ')
            time=$(echo $output | cut -f4 -d' ')
            echo "iter=$execute_ct,p=$p,e=$e,correct=$correctness,time=$time"
            echo "$execute_ct,$p,$e,$correctness,$time" >> "$type".csv
        done
    done
done
