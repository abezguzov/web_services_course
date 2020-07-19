docker exec -it modeldeployment_flask_1  bash
docker exec -it modeldeployment_flask_1  python train.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,1,1,1"}' \
  http://localhost:5000/iris_post