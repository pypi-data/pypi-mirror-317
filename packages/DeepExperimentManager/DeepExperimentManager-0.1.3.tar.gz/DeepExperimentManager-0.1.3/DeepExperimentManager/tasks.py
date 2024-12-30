from abc import ABC, abstractmethod
import torch
import torch.nn.functional as F

class BaseTask(ABC):
    """
    An abstract base class for various tasks. 
    Each specific task should override the 'inference' method 
    to produce its own prediction logic.
    """

    @abstractmethod
    def inference(self, model, inputs):
        """
        Returns predictions for the given inputs using the provided model.
        
        Args:
            model (nn.Module): A PyTorch model or any neural network model to perform inference.
            inputs (torch.Tensor): A batch of inputs for inference.
        
        Returns:
            torch.Tensor: The model's predictions in an appropriate format for each task.
        """
        pass


class ClassificationTask(BaseTask):
    """
    A class performing multi-class classification.
    Assumes the model outputs have shape (B, num_classes).
    The highest-scoring class is taken as the prediction (argmax).
    """

    def inference(self, model, inputs):
        """
        Runs inference for a classification task.

        Args:
            model (nn.Module): A trained PyTorch model that outputs class logits.
            inputs (torch.Tensor): Input features of shape (B, *).
        
        Returns:
            torch.Tensor: Predicted class labels of shape (B,).
        """
        with torch.no_grad():
            outputs = model(inputs)            # (B, num_classes)
            _, preds = torch.max(outputs, dim=1)
        return preds


class MultiLabelClassificationTask(BaseTask):
    """
    A class performing multi-label classification.
    Assumes the model outputs have shape (B, num_labels).
    Uses a sigmoid activation and a 0.5 threshold for each label.
    """

    def inference(self, model, inputs):
        """
        Runs inference for a multi-label classification task.

        Args:
            model (nn.Module): A trained PyTorch model that outputs raw logits for each label.
            inputs (torch.Tensor): Input features of shape (B, *).
        
        Returns:
            torch.Tensor: A binary matrix of shape (B, num_labels), 
                          where 1 indicates the label is predicted and 0 otherwise.
        """
        with torch.no_grad():
            outputs = model(inputs)            # (B, num_labels)
            probs = torch.sigmoid(outputs)     # apply sigmoid
            preds = (probs > 0.5).long()       # threshold at 0.5
        return preds


class RegressionTask(BaseTask):
    """
    A class performing regression.
    Assumes the model outputs have shape (B,) or (B, 1).
    """

    def inference(self, model, inputs):
        """
        Runs inference for a regression task.

        Args:
            model (nn.Module): A trained PyTorch model that outputs a continuous value.
            inputs (torch.Tensor): Input features of shape (B, *).
        
        Returns:
            torch.Tensor: Predicted continuous values of shape (B,).
        """
        with torch.no_grad():
            outputs = model(inputs)      # (B,) or (B,1)
            preds = outputs.squeeze(dim=-1)  # ensure shape (B,)
        return preds


class SegmentationTask(BaseTask):
    """
    A class performing semantic segmentation.
    Assumes the model outputs have shape (B, num_classes, H, W).
    For each pixel, argmax is used to determine the predicted class.
    """

    def inference(self, model, inputs):
        """
        Runs inference for a semantic segmentation task.

        Args:
            model (nn.Module): A trained PyTorch model that outputs a score map for each class.
            inputs (torch.Tensor): Input images of shape (B, C, H, W).
        
        Returns:
            torch.Tensor: Segmentation masks of shape (B, H, W), 
                          where each pixel is assigned a class index.
        """
        with torch.no_grad():
            outputs = model(inputs)              # (B, num_classes, H, W)
            preds = torch.argmax(outputs, dim=1) # (B, H, W)
        return preds


class ObjectDetectionTask(BaseTask):
    """
    A class performing object detection.
    The model is assumed to output bounding boxes and class scores 
    (or similar structures).
    This is a simplified example. Real detection pipelines often 
    require more complex post-processing (NMS, thresholding, etc.).
    """

    def inference(self, model, inputs):
        """
        Runs inference for an object detection task.

        Args:
            model (nn.Module): A trained detection model.
            inputs (torch.Tensor): Input images of shape (B, C, H, W).
        
        Returns:
            List[Dict[str, torch.Tensor]]: A list of detection results for each image. 
            Each item might contain:
                - 'boxes': (num_boxes, 4) bounding box coordinates
                - 'labels': (num_boxes,) predicted class labels
                - 'scores': (num_boxes,) confidence scores
        """
        model.eval()
        with torch.no_grad():
            # Typically, many detection models (like torchvision's fasterrcnn_resnet50_fpn)
            # directly return a list of dict, each containing boxes, labels, scores, etc.
            detections = model(inputs)  
        
        return detections


class TimeSeriesForecastingTask(BaseTask):
    """
    A class performing time series forecasting.
    Assumes the model outputs future predictions for a given sequence input.
    """

    def inference(self, model, inputs):
        """
        Runs inference for a time series forecasting task.

        Args:
            model (nn.Module): A trained forecasting model.
            inputs (torch.Tensor): Input time series data of shape (B, sequence_length, features).
        
        Returns:
            torch.Tensor: Forecasted values, e.g. (B, future_length) or (B, future_length, features).
        """
        with torch.no_grad():
            outputs = model(inputs)
        return outputs


class GenerationTask(BaseTask):
    """
    A class performing text or sequence generation (e.g., language modeling, text generation).
    This class can be used for any generative model that produces sequences/token outputs.
    """

    def inference(self, model, inputs):
        """
        Runs inference for a generative model.

        Args:
            model (nn.Module): A trained generative model.
            inputs (torch.Tensor): Context or prompt (e.g., token IDs, shape depends on the model).
        
        Returns:
            torch.Tensor or List[int]: The generated sequence, 
                                       which could be token IDs or raw text (depending on your logic).
        """
        model.eval()
        with torch.no_grad():
            # The actual generation might involve loops or beam search, etc.
            # This is a simplistic placeholder:
            outputs = model(inputs)  
        return outputs
