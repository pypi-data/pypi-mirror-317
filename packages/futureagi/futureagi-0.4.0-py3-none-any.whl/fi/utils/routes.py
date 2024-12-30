from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"

    # logging
    log_model = "sdk/api/v1/log/model/"

    # evaluation
    evaluate = "sdk/api/v1/eval/"
    evaluate_template = "sdk/api/v1/eval/{eval_id}/"

    # dataset
    dataset = "model-hub/develops"
    dataset_names = "model-hub/develops/get-datasets-names/"
    dataset_empty = "model-hub/develops/create-empty-dataset/"
    dataset_local = "model-hub/develops/create-dataset-from-local-file/"
    dataset_huggingface = "model-hub/develops/create-dataset-from-huggingface/"
    dataset_table = "model-hub/develops/{dataset_id}/get-dataset-table/"
    dataset_delete = "model-hub/develops/delete_dataset/"
    dataset_add_rows = "model-hub/develops/{dataset_id}/add_rows/"
    dataset_add_columns = "model-hub/develops/{dataset_id}/add_columns/"
    # model provider
    model_hub_api_keys = "model-hub/api-keys/"
    model_hub_default_provider = "model-hub/default-provider/"
