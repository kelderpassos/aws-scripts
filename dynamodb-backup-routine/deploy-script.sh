set -e

cd infra
npm i
echo -e "Deploying backup infrastructure on bigtrade-${1}...\n"
npm run deploy:$1
echo -e "Deploy finished sucessfully!\n"

cd ../service/
npm i 
echo -e "Deploying backup infrastructure on bigtrade-${1}...\n"
npm run deploy:$1
echo -e "Deploy finished sucessfully!\n"
