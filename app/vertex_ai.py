from google.cloud import aiplatform
import streamlit as st

PROJECT_ID = "kif-kaiseki-kun-project"
LOCATION = "asia-northeast1"
ENDPOINT_ID = "7618190613418082304"


def evaluate(csa_file_path):
    client_options = {"api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    endpoint = client.endpoint_path(
        project=PROJECT_ID, location=LOCATION, endpoint=ENDPOINT_ID
    )

    instances = [{"csa_file_path": csa_file_path}]
    response = client.predict(endpoint=endpoint, instances=instances)

    evaluate_values_before = response.predictions[0]["evaluate_value"]

    evaluate_values = []

    for index, evaluate_value in enumerate(evaluate_values_before, 1):
        if index % 2 == 0:  # 偶数の場合、後手の評価値を1から引いて、全て先手の評価値に直す
            first_player_value = 1 - evaluate_value
            evaluate_values.append(first_player_value)
        else:
            evaluate_values.append(evaluate_value)

    return evaluate_values
