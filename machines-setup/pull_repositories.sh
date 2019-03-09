cd ..
echo "Pulling..."
git lfs pull
git pull
cd ../stack
echo "Pulling stack..."
git lfs pull
git pull
echo "Pulling scheduler..."
cd ../stack-scheduler
git lfs pull
git pull
echo "Pulling discovery..."
cd ../stack-discovery
git lfs pull
git pull
