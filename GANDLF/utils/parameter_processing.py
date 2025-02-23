from GANDLF.models.modelBase import ModelBase


def populate_header_in_parameters(parameters, headers):
    """
    This function populates the parameters with information from the header in a common manner

    Args:
        parameters (dict): The parameters passed by the user yaml.
        headers (dict): The CSV headers dictionary.

    Returns:
        dict: Combined parameter dictionary containing header information
    """
    # initialize common parameters based on headers
    parameters["headers"] = headers
    # ensure the number of output classes for model prediction is working correctly

    if len(headers["predictionHeaders"]) > 0:
        parameters["model"]["num_classes"] = len(headers["predictionHeaders"])

    # initialize model type for processing: if not defined, default to torch
    if not ("type" in parameters["model"]):
        parameters["model"]["type"] = "torch"

    if parameters["model"]["type"] == "openvino" and parameters["model"][
        "architecture"
    ] in ["brain_age", "sdnet"]:
        print(
            "Only PyTorch for inference is supported for the current model architecture: {0}.".format(
                parameters["model"]["architecture"]
            )
        )
        parameters["model"]["type"] = "torch"

    # initialize number of channels for processing
    if not ("num_channels" in parameters["model"]):
        parameters["model"]["num_channels"] = len(headers["channelHeaders"])

    parameters["problem_type"] = find_problem_type(
        parameters, ModelBase(parameters).final_convolution_layer
    )

    # if the problem type is classification/segmentation, ensure the number of classes are picked from the configuration
    if parameters["problem_type"] != "regression":
        parameters["model"]["num_classes"] = len(parameters["model"]["class_list"])

    return parameters


def find_problem_type(parameters, model_final_layer):
    """
    This function determines the type of problem at hand - regression, classification or segmentation

    Args:
        headersFromCSV (dict): The CSV headers dictionary.
        model_final_layer (model_final_layer): The final layer of the model. If None, the model is for regression.

    Returns:
        str: The problem type (regression/classification/segmentation).
    """
    # check if regression/classification has been requested
    classification_phrases = [
        "classification_but_not_softmax",
        "logits",
        "classification_without_softmax",
    ]
    headersFromCSV = parameters["headers"]
    class_list_exist = "class_list" in parameters["model"]
    if (
        class_list_exist
        and parameters["model"]["final_layer"].lower() in classification_phrases
    ):
        return "classification"

    if len(headersFromCSV["predictionHeaders"]) > 0:
        if model_final_layer is None:
            return "regression"
        else:
            return "classification"
    else:
        return "segmentation"


def populate_channel_keys_in_params(data_loader, parameters):
    """
    Function to read channel key information from specified data loader

    Args:
        data_loader (torch.DataLoader): The data loader to query key information from.
        parameters (dict): The parameters passed by the user yaml.

    Returns:
        dict: Updated parameters that include key information
    """
    # using train_loader makes this slower as train loader contains full augmentations
    batch = next(iter(data_loader))
    all_keys = list(batch.keys())
    channel_keys = []
    value_keys = []
    label_keys = []
    print("All Keys : ", all_keys)
    for item in all_keys:
        if item.isnumeric():
            channel_keys.append(item)
        elif "value" in item:
            value_keys.append(item)
        elif "label" in item:
            label_keys.append(item)
    parameters["channel_keys"] = channel_keys
    if value_keys:
        parameters["value_keys"] = value_keys
    if label_keys:
        parameters["label_keys"] = label_keys

    return parameters
