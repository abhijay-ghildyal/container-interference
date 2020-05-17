docker stats docker_mnist_1

docker stats --format "{{.Container}}: {{.CPUPerc}}"

# start=`date +%s`
# docker run --rm -v /home/abhijay/CS_533_Project:/workspace pytorch/pytorch python main.py --no-cuda --epochs 2 &&
# end=`date +%s`

# runtime=$((end-start))
# echo $runtime







