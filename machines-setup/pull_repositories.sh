cd ..
echo "Pulling..."
git lfs pull
cd ../stack
echo "Pulling stack..."
git lfs pull
echo "Pulling scheduler..."
cd ../stack-scheduler
git lfs pull
echo "Pulling discovery..."
cd ../stack-discovery
git lfs pull